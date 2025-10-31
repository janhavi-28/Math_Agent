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
