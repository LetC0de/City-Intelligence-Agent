# 🌆 City Intelligence Agent – Multi-Tool Intelligent City Assistant

City Intelligence Agent is a smart AI agent built using LangChain that provides real-time information about cities. It integrates multiple tools like weather APIs and news search, along with human-in-the-loop approval for safe and controlled execution.


## 🚀 Features

* 🌦️ Get real-time weather information for any city
* 📰 Fetch latest news using Tavily search
* 🤖 AI-powered responses using Mistral LLM
* 🛠️ Tool-based architecture using LangChain
* 👤 Human approval before executing tool calls
* 🔐 Secure API key handling using `.env`


## 🧠 Tech Stack

* Python
* LangChain
* Mistral AI (LLM)
* Tavily API (Search Tool)
* OpenWeather API
* dotenv
* requests



## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/LetC0de/City-Intelligence-Agent.git
cd Agent
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```


## 🔐 Environment Variables

Create a `.env` file in root directory:

```env
OPENWHEATHER_API_KEY=your_openweather_api_key
TAVILY_API_KEY=your_tavily_api_key
MISTRAL_API_KEY=your_mistral_api_key
```


## ▶️ Usage

Run the script:

```bash
python main.py
```

Then interact:

```
You: what's the weather in delhi
You: latest news in mumbai
```

The agent will ask for approval before executing tools.


## 📁 Project Structure

```
Agent/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚠️ Notes

* Make sure API keys are valid
* `.env` file is ignored using `.gitignore`
* Do NOT push secrets to GitHub



## 👨‍💻 Author

Abhishek Nishad


## ⭐ If you like this project

Give it a ⭐ on GitHub and share it!
