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

## 📄 License
MIT License
" > README.md
# Math Routing Agent - Prototype v2

Enhancements in v2:
- Guardrails YAML for input/output validation (`guardrails/schema.yml`)
- OpenAI LLM wrapper to synthesize step-by-step solutions (set OPENAI_API_KEY)
- MCP prompt templates in `app/mcp_prompts.py`
- More detailed instructions

Run:
1. python -m venv venv
2. source venv/bin/activate  # Windows: venv\Scripts\activate
3. pip install -r requirements.txt
4. export OPENAI_API_KEY=sk-...
5. uvicorn app.main:app --reload --port 8000
6. streamlit run frontend/app.py --server.port 8501
