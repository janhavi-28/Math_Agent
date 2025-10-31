# TODO: Fix SerpAPI Error in Math Routing Agent

## Steps to Complete
- [x] Update SerpAPI import in app/llm.py to use GoogleSearch
- [x] Fix web_search method to instantiate GoogleSearch and call get_dict()
- [x] Fix web_hits extraction in get_solution method to use GoogleSearch
- [x] Test backend API with uvicorn
- [x] Test frontend with streamlit
- [x] Test full application flow with a sample query
