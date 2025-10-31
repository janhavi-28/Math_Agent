# app/guardrails_wrapper.py
import re

class GuardrailsWrapper:
    """
    Lightweight substitute for 'guardrails-ai' that safely cleans input and output.
    """

    def apply_input_guard(self, text: str) -> str:
        # Basic sanitization to prevent prompt injection or malicious content
        text = re.sub(r"[{}<>]", "", text)  # Remove braces and angle brackets
        text = text.strip()
        return text

    def apply_output_guard(self, response):
        # If response is a dict, ensure it doesn't contain unsafe text
        if isinstance(response, dict):
            response = {k: self._sanitize(str(v)) for k, v in response.items()}
        elif isinstance(response, str):
            response = self._sanitize(response)
        return response

    def _sanitize(self, text: str) -> str:
        # Prevent output of system prompts or credentials
        forbidden = ["apikey", "password", "system prompt", "sudo", "rm -rf"]
        for f in forbidden:
            text = re.sub(f, "[REDACTED]", text, flags=re.IGNORECASE)
        return text
