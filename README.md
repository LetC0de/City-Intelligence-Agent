# 🌆 City Intelligence Agent – Multi-Tool AI City Assistant

City Intelligence Agent is a **full-stack AI-powered city assistant** built using LangChain, Flask, and a modern frontend UI. It provides real-time city insights like weather and news, with a **human-in-the-loop approval system** for safe tool execution.

🔗 **Live Project:** https://city-intelligence-agent.vercel.app/

---

## 🚀 Features

* 🌦️ Real-time weather information for any city
* 📰 Latest news fetching using Tavily Search API
* 🤖 AI-powered responses using Mistral LLM
* 🛠️ Tool-based architecture with LangChain
* 👤 Human approval before tool execution (safety layer)
* 💬 Interactive chat UI (frontend + backend integration)
* 🔗 Clickable links for news sources
* 📱 Responsive UI with smooth chat experience
* 🔐 Secure API key management using `.env`

---

## 🧠 Tech Stack

### 🔹 Backend

* Python
* Flask (API server)
* LangChain (agent + tools)
* Mistral AI (LLM)
* Tavily API (news search)
* OpenWeather API (weather data)
* dotenv, requests

### 🔹 Frontend

* HTML
* CSS
* JavaScript (Vanilla JS)
* Fetch API (for backend communication)

### 🔹 Deployment

* Frontend → Vercel
* Backend → Render

---

## ⚙️ How It Works

1. User sends a message via the chat UI
2. Backend (Flask) sends it to the LLM
3. LLM decides:

   * Direct response OR
   * Tool call (weather/news)
4. If tool is needed:

   * ⛔ System asks for **user approval (frontend modal)**
5. After approval:

   * Tool executes
   * Final response is generated and displayed

---

## 🖥️ Live Demo

👉 https://city-intelligence-agent.vercel.app/

Try:

```
what's the weather in delhi
latest news in mumbai
```

---

## 📁 Project Structure

```
Agent/
│
├── backend/
│   ├── main.py
│   ├── .env
│   ├── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│
└── README.md
```

---

## 🔐 Environment Variables

Create a `.env` file in backend:

```env
OPENWHEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
MISTRAL_API_KEY=your_mistral_api_key
```

---

## ▶️ Run Locally

### 1. Clone repo

```bash
git clone https://github.com/LetC0de/City-Intelligence-Agent.git
cd Agent
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate environment

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run backend

```bash
python main.py
```

---

## 🌐 API Configuration

Frontend connects to deployed backend:

```javascript
const API_BASE_URL = "https://city-intelligence-agent.onrender.com";
```

---

## 🧩 Key Features Explained

### 🔹 Human-in-the-Loop Tool Approval

Before executing tools like weather or news:

* User gets a **popup approval modal**
* Prevents unwanted API calls
* Makes system safer and controllable

---

### 🔹 Smart Response Formatting

LLM ensures:

* Clean structured output
* Bullet points
* Emojis for clarity
* Clickable links for news

---

### 🔹 Tool Integration

#### 🌦️ Weather Tool

Uses OpenWeather API to fetch:

* Temperature
* Weather condition

#### 📰 News Tool

Uses Tavily API to fetch:

* Latest headlines
* Source links
* Brief summaries

---

## ⚠️ Notes

* Do NOT push `.env` file to GitHub
* Ensure API keys are valid
* Backend may take time to wake up (Render free tier)

---

## 👨‍💻 Author

**Abhishek Nishad**

---

## ⭐ Support

If you like this project:

* ⭐ Star the repo
* 🔁 Share it
* 💬 Give feedback

