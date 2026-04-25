from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
import requests
import os
import uuid

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# Initialize LLM
llm = ChatMistralAI(model="mistral-small-2506", temperature=0.7)

# System prompt for better formatting
SYSTEM_PROMPT = """You are a helpful City Intelligence Agent that provides weather and news information.

IMPORTANT FORMATTING RULES:
- Always format your responses with proper structure and spacing
- Use bullet points (•) for lists
- Add line breaks between sections for readability
- Use emojis sparingly and appropriately (weather emoji for weather, news emoji for news)
- Keep responses clear, organized, and easy to read

When providing NEWS:
1. Start with a brief 1-2 sentence overview about the city's current news situation
2. Then list each news item with bullet points
3. Include clickable links for each news source
4. Format like this:

📰 Current News in [City]:
[Brief overview sentence about what's happening]

• **[Headline]**
  🔗 Source: [URL]
  [Brief 1-line description]

• **[Headline]**
  🔗 Source: [URL]
  [Brief 1-line description]

When providing WEATHER:
- Use weather emoji (☀️🌤️⛅🌦️🌧️⛈️❄️)
- Format clearly with temperature and conditions
- Keep it concise

Always be helpful, friendly, and well-formatted!
"""

# Get API keys
weather_api_key = os.getenv("OPENWHEATHER_API_KEY")
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Store pending approvals
pending_approvals = {}


# ============================================
# TOOLS
# ============================================

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={weather_api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'could not fetch weather')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    return f"Weather in {city}: {desc}, {temp}°C"


@tool
def get_news(city: str) -> str:
    """Get latest news about a city"""
    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="advanced",
        max_results=5
    )

    results = response.get("results", [])
    if not results:
        return f"No news found for {city}"

    # Format news nicely with longer descriptions
    news_items = []
    for i, r in enumerate(results, 1):
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")[:500]  # Increased from 150 to 300 chars for 3-4 lines

        news_items.append(
            f"{i}. {title}\n"
            f"   Link: {url}\n"
            f"   Summary: {snippet}..."
        )

    return f"Latest news about {city}:\n\n" + "\n\n".join(news_items)


# Create tools list
tools = [get_weather, get_news]

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)


# ============================================
# ROUTES
# ============================================

@app.route('/chat', methods=['POST'])
def chat():
    """
    Receives user message, sends to LLM with tools.
    If LLM wants to use a tool, we ask for approval first.
    """
    try:
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Create messages with system prompt
        messages = [
            HumanMessage(content=SYSTEM_PROMPT + "\n\nUser: " + user_message)
        ]

        # Send to LLM with tools
        ai_response = llm_with_tools.invoke(messages)

        # Check if LLM wants to use a tool
        if ai_response.tool_calls:
            # LLM wants to use a tool! Ask for approval
            tool_call = ai_response.tool_calls[0]  # Get first tool call

            approval_id = str(uuid.uuid4())

            # Store everything needed for later
            pending_approvals[approval_id] = {
                "user_message": user_message,
                "ai_message": ai_response,
                "tool_call": tool_call
            }

            return jsonify({
                "needs_approval": True,
                "approval_id": approval_id,
                "tool_name": tool_call["name"],
                "tool_args": tool_call["args"]
            })

        else:
            # No tool needed, just return the response
            return jsonify({
                "response": ai_response.content
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/approve', methods=['POST'])
def approve_tool():
    """
    Handles user's approval decision.
    """
    try:
        data = request.json
        approval_id = data.get('approval_id')
        approved = data.get('approved', False)

        if approval_id not in pending_approvals:
            return jsonify({"error": "Invalid approval ID"}), 400

        approval_data = pending_approvals[approval_id]
        user_message = approval_data["user_message"]
        ai_message = approval_data["ai_message"]
        tool_call = approval_data["tool_call"]

        if approved:
            # User approved! Execute the tool
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # Find and execute the tool
            tool_result = None
            for tool in tools:
                if tool.name == tool_name:
                    tool_result = tool.invoke(tool_args)
                    break

            if tool_result is None:
                return jsonify({"error": f"Tool {tool_name} not found"}), 500

            # Create tool message
            tool_message = ToolMessage(
                content=tool_result,
                tool_call_id=tool_call["id"]
            )

            # Now ask LLM to respond with the tool result (with system prompt)
            messages = [
                HumanMessage(content=SYSTEM_PROMPT + "\n\nUser: " + user_message),
                ai_message,
                tool_message
            ]

            final_response = llm_with_tools.invoke(messages)

            # Clean up
            del pending_approvals[approval_id]

            return jsonify({
                "response": final_response.content
            })

        else:
            # User denied! Tell LLM the tool was denied
            tool_message = ToolMessage(
                content=f"User denied the use of {tool_call['name']} tool.",
                tool_call_id=tool_call["id"]
            )

            messages = [
                HumanMessage(content=SYSTEM_PROMPT + "\n\nUser: " + user_message),
                ai_message,
                tool_message
            ]

            final_response = llm_with_tools.invoke(messages)

            # Clean up
            del pending_approvals[approval_id]

            return jsonify({
                "response": final_response.content
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Simple health check"""
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    print("Backend server starting on http://localhost:5000")
    app.run(debug=True, port=5000)
