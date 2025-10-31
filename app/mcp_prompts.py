# Templates for MCP prompts. These enforce the context, citation requirement, and style.
from textwrap import dedent

def prompt_from_web(query, hits):
    sources = '\n'.join([f"[{i+1}] {h['title']} - {h['link']}\nSnippet: {h.get('snippet','')}" for i,h in enumerate(hits)])
    p = dedent(f"""You are a math professor. A student asked: {query}

Use ONLY the information from the following web sources to construct a clear, step-by-step solution.
Cite the sources inline using [n] where n is the source number from the list below.

Sources:
{sources}

Instructions:
- If the sources are insufficient to compute an exact answer, say you cannot be certain and explain why.
- Show all steps and the final numeric result if applicable.
- Keep explanations simple for students.

Provide the solution now.
""")
    return p

def prompt_from_kb(query, kb_context):
    p = dedent(f"""You are a math professor. A student asked: {query}

Context from the internal knowledge base:
{kb_context}

Using only the KB context above, produce a step-by-step solution suitable for a student. If additional assumptions are needed, state them explicitly.
""")
    return p
