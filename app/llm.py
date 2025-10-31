import os
import re
import math
from tavily import TavilyClient
from serpapi import Client
from dotenv import load_dotenv

load_dotenv()

class HybridLLM:
    """Combines Tavily API (reasoning) + SerpAPI (factual web results)."""

    def __init__(self):
        tavily_key = os.getenv("TAVILY_API_KEY")
        serpapi_key = os.getenv("SERPAPI_API_KEY")

        if not tavily_key:
            raise ValueError("Missing TAVILY_API_KEY in .env file.")
        if not serpapi_key:
            raise ValueError("Missing SERPAPI_KEY in .env file.")

        self.tavily = TavilyClient(api_key=tavily_key)
        self.serpapi_client = Client(api_key=serpapi_key)

    def web_search(self, query: str):
        """Fetch web results via SerpAPI."""
        try:
            results = self.serpapi_client.search(q=query, num=5)
            snippets = []
            if "organic_results" in results:
                for item in results["organic_results"]:
                    title = item.get("title", "")
                    snippet = item.get("snippet", "")
                    if snippet:
                        snippets.append(f"{title}: {snippet}")
            return "\n".join(snippets[:3]) if snippets else "No web results found."
        except Exception as e:
            return f"Error fetching from SerpAPI: {e}"

    def generate_reasoning(self, query: str, web_context: str):
        """Generate reasoning from Tavily using web context."""
        try:
            # Truncate inputs to fit within Tavily's 400 character limit
            max_query_len = 50  # Reduced to ensure total prompt <= 400 chars
            max_context_len = 50  # Reduced to ensure total prompt <= 400 chars
            truncated_query = query[:max_query_len] + "..." if len(query) > max_query_len else query
            truncated_context = web_context[:max_context_len] + "..." if len(web_context) > max_context_len else web_context
            prompt = f"Question: {truncated_query}\n\nWeb Info:\n{truncated_context}\n\nProvide a clear, step-by-step solution in markdown format. Structure the answer as numbered steps (1., 2., 3., etc.), one step per line, with each step explaining the calculation or reasoning clearly. Use **bold** for key numbers and results. Keep it concise but complete."
            resp = self.tavily.search(prompt)
            if "answer" in resp and resp["answer"]:
                return resp["answer"].strip()
            elif "results" in resp and resp["results"]:
                return resp["results"][0].get("content", "No reasoning available.")
            return "No answer found from Tavily."
        except Exception as e:
            return f"Error generating reasoning via Tavily: {e}"

    def compute_circle_properties(self, question: str):
        """Detect and compute circle area or circumference if applicable."""
        question_lower = question.lower()
        # Check for circle-related keywords
        if not any(word in question_lower for word in ['circle', 'area', 'circumference', 'perimeter']):
            return None

        # Extract radius or diameter
        radius_match = re.search(r'radius\s*[=]\s*(\d+(?:\.\d+)?)', question_lower)
        diameter_match = re.search(r'diameter\s*[=]\s*(\d+(?:\.\d+)?)', question_lower)

        if radius_match:
            radius = float(radius_match.group(1))
            diameter = 2 * radius
        elif diameter_match:
            diameter = float(diameter_match.group(1))
            radius = diameter / 2
        else:
            return None  # No radius or diameter found

        # Determine what to compute
        if 'area' in question_lower:
            area = math.pi * radius ** 2
            solution = f"1. The radius (r) is {radius}.\n2. The formula for the area of a circle is A = πr².\n3. Substitute the radius: A = π × {radius}² = π × {radius**2}.\n4. Calculate the area: A ≈ {area:.2f}."
            return {
                "solution": solution,
                "web_context": "Direct calculation using math.pi",
                "source": "direct",
                "web_hits": []
            }
        elif 'circumference' in question_lower or 'perimeter' in question_lower:
            circumference = 2 * math.pi * radius
            solution = f"1. The radius (r) is {radius}.\n2. The formula for the circumference of a circle is C = 2πr.\n3. Substitute the radius: C = 2 × π × {radius}.\n4. Calculate the circumference: C ≈ {circumference:.2f}."
            return {
                "solution": solution,
                "web_context": "Direct calculation using math.pi",
                "source": "direct",
                "web_hits": []
            }
        return None

    def get_solution(self, question: str):
        """Combined pipeline."""
        # Check for circle calculations first
        circle_result = self.compute_circle_properties(question)
        if circle_result:
            return {
                "question": question,
                **circle_result
            }

        # Check if it's a simple math question that doesn't need web search
        if re.search(r'\d+\s*[\+\-\*\/]\s*\d+', question) and len(question.strip()) < 50:
            # For simple math, extract and evaluate the expression directly
            expr = re.sub(r'[^\d\+\-\*\/\(\)\.]', '', question.strip())
            try:
                result = eval(expr)
                reasoning = f"The result of {expr} is {result}."
            except Exception as e:
                reasoning = f"Unable to calculate: {e}"
            web_context = "Direct calculation"
        else:
            web_info = self.web_search(question)
            reasoning = self.generate_reasoning(question, web_info)
            web_context = web_info

        # Prepare web_hits for frontend
        web_hits = []
        if web_context != "Direct calculation":
            try:
                results = self.serpapi_client.search(q=question, num=5)
                if "organic_results" in results:
                    for item in results["organic_results"][:3]:  # Limit to 3 hits
                        web_hits.append({
                            "title": item.get("title", "No title"),
                            "snippet": item.get("snippet", "No snippet"),
                            "link": item.get("link", "#")
                        })
            except Exception as e:
                pass  # If web search fails, just skip web_hits

        return {
            "question": question,
            "web_context": web_context,
            "solution": reasoning,
            "source": "web" if web_hits else "direct",
            "web_hits": web_hits
        }
