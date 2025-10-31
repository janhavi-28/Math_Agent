# MCP minimal: web search + prompt builder that enforces Model Context Protocol style prompts.
import os, requests
from .mcp_prompts import prompt_from_web, prompt_from_kb

SERPAPI_KEY = os.getenv('SERPAPI_API_KEY')
TAVILY_KEY = os.getenv('TAVILY_API_KEY')

class MCP:
    def __init__(self):
        pass

    def search_web(self, query):
        if SERPAPI_KEY:
            params = {'q': query, 'api_key': SERPAPI_KEY}
            try:
                r = requests.get('https://serpapi.com/search', params=params, timeout=8)
                j = r.json()
                hits = []
                for item in j.get('organic_results', [])[:5]:
                    hits.append({'title': item.get('title'), 'link': item.get('link'), 'snippet': item.get('snippet')})
                return hits
            except Exception as e:
                print('SerpAPI error', e)
        if TAVILY_KEY:
            headers = {'Authorization': f'Bearer {TAVILY_KEY}'}
            try:
                r = requests.post('https://api.tavily.ai/v1/search', json={'q':query}, headers=headers, timeout=8)
                j = r.json()
                hits = [{'title':it.get('title'), 'link':it.get('url'), 'snippet':it.get('excerpt')} for it in j.get('results',[])[:5]]
                return hits
            except Exception as e:
                print('Tavily error', e)
        return []

    def build_prompt_from_web(self, query, web_hits):
        return prompt_from_web(query, web_hits)

    def build_prompt_from_kb(self, query, kb_context):
        return prompt_from_kb(query, kb_context)
