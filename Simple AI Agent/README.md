# **Simple AI Agent**  

🚀 A minimal AI-powered assistant built using **LangChain** and **LLMs**. This AI agent can:  
- 🌍 **Search the Web** using DuckDuckGo  
- ⛅ **Fetch Weather Reports** via OpenWeatherMap API  
- 🧮 **Perform Mathematical Calculations**  

This is the first AI agent in the **AI Agents** repository, with more advanced AI agents to come.  

---

## **Overview**  

### **🔹 What is this AI Agent?**  
This AI Agent acts as a basic **retrieval-augmented generation (RAG)** system. It takes user queries, determines which tool to use, retrieves relevant information, and provides an answer.  

### **🔹 How Does It Work?**  
1. **User Input:** The agent receives a query (e.g., "What’s the weather in Mumbai?").  
2. **Tool Selection:** It selects an appropriate tool (Weather, Search, or Calculator) based on the query.  
3. **LLM Processing:** The query is passed to **Llama-3.1-8B-Instant** via **Groq API**, generating a structured response.  
4. **Final Response:** The agent returns a structured answer with confidence scores and sources (if applicable).  

---

## **Installation & Setup**  

### **🔹 Prerequisites**  
- Python 3.9+  
- API Keys for **Groq** (LLM) & **OpenWeatherMap**  

### **🔹 1️⃣ Clone the Repository**  
```bash
git clone https://github.com/dutta-sujoy/ai_agents.git
cd AI-Agents/Simple-AI-Agent
```

### **🔹 2️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **🔹 3️⃣ Set Up API Keys**  
Create a `.env` file inside the **Simple-AI-Agent** directory and add your API keys:  
```
GROQ_API_KEY=your_groq_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

### **🔹 4️⃣ Run the AI Agent**  
```bash
python main.py
```

---

## **Features & How It Works**  

### **🛠️ Tools Used by the AI Agent**  

| Tool          | Functionality |
|--------------|--------------|
| **Search** (DuckDuckGo) | Searches the web for general queries. |
| **WeatherInfo** (OpenWeatherMap) | Fetches live weather updates for a given city. |
| **Calculator** | Evaluates mathematical expressions dynamically. |

### **🧠 LangChain & AI Agent Logic**  
- **LLM Used:** `llama-3.1-8B-instant` (via Groq API)  
- **LangChain Components:**  
  - **AgentExecutor:** Manages tool invocation and result processing.  
  - **ChatPromptTemplate:** Defines the system's behavior.  
  - **PydanticOutputParser:** Ensures structured output.  

### **📌 Example Queries**  

| User Input | Tool Used | AI Response Example |
|------------|----------|----------------------|
| "Who is the CEO of Tesla?" | 🔍 Search | "The CEO of Tesla is Elon Musk. (Source: Wikipedia)" |
| "What’s the weather in New York?" | ⛅ WeatherInfo | "Current weather in New York: Clear sky, 22°C, Wind speed 5m/s" |
| "Calculate 15 * 9 + 6" | 🧮 Calculator | "Result: 141" |

---

## **Preview**  


https://github.com/user-attachments/assets/1e7603c1-3270-48a3-97f6-a20d5bea4091



---

🚀 Happy Coding! 🎯  
