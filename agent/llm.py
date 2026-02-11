import os

# Lightweight wrapper to produce an LLM with OpenAI-compatible endpoint support (e.g., OpenRouter)
# Tries to use langchain.chat_models.ChatOpenAI if available; otherwise falls back to a simple HTTP wrapper.

try:
    from langchain.chat_models import ChatOpenAI
    LANGCHAIN_AVAILABLE = True
except Exception:
    LANGCHAIN_AVAILABLE = False


class LangChainLLM:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0):
        self.model = model
        self.temperature = temperature
        # langchain's ChatOpenAI will read OPENAI_API_KEY and OPENAI_API_BASE if provided
        if not LANGCHAIN_AVAILABLE:
            raise RuntimeError("langchain not available in environment")
        self.client = ChatOpenAI(model=self.model, temperature=self.temperature)

    def generate(self, prompt: str) -> str:
        # Use the ChatOpenAI interface to produce a single string
        resp = self.client.generate([{"role": "user", "content": prompt}])
        # langchain's return shape may vary by version; handle common cases
        try:
            # new ChatOpenAI .generate returns an object with generations
            return resp.generations[0][0].text
        except Exception:
            try:
                return str(resp)
            except Exception:
                return ""


# Fallback simple HTTP wrapper if langchain is not installed
import requests

class OpenAPIFallbackLLM:
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0):
        self.model = model
        self.temperature = temperature
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set for OpenAPIFallbackLLM")

    def generate(self, prompt: str) -> str:
        url = f"{self.api_base.rstrip('/')}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": 512,
        }
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        # Try common response shapes
        if "choices" in data and len(data["choices"]) > 0:
            c = data["choices"][0]
            if "message" in c and "content" in c["message"]:
                return c["message"]["content"]
            if "text" in c:
                return c["text"]
        return str(data)


def make_llm(model: str = "gpt-4o-mini", temperature: float = 0.0):
    """Factory: return a langchain-backed LLM if available, otherwise a direct HTTP fallback.
    Requires OPENAI_API_KEY (and optionally OPENAI_API_BASE) in environment for fallback.
    """
    if LANGCHAIN_AVAILABLE:
        try:
            return LangChainLLM(model=model, temperature=temperature)
        except Exception:
            pass
    return OpenAPIFallbackLLM(model=model, temperature=temperature)
