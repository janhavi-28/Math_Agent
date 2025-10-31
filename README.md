Math Agent 🤖  
An intelligent math-solving agent combining Tavily API (LLM reasoning) and SerpAPI (web search).  

## 🚀 Features
- Hybrid LLM pipeline (Tavily + SerpAPI)
- Streamlit front-end UI
- Math reasoning with examples
- Dynamic web retrieval for factual support

## ⚙️ Setup
1. Clone the repo:
   \`\`\`bash
   git clone https://github.com/janhavi-28/Math_Agent.git
   cd Math_Agent
   \`\`\`
2. Create virtual environment:
   \`\`\`bash
   python -m venv venv
   venv\Scripts\activate
   \`\`\`
3. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
4. Add your API keys in a new .env file:
   \`\`\`
   TAVILY_API_KEY=your_key_here
   SERPAPI_KEY=your_key_here
   \`\`\`
5. Run the Streamlit app:
   \`\`\`bash
   streamlit run app.py --server.port 8503
   \`\`\`

## 📦 Tech Stack
- **Backend:** Python, FastAPI
- **Frontend:** Streamlit
- **AI:** Tavily API + SerpAPI
- **Version Control:** Git & GitHub


