import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (optional for local dev, not needed for Streamlit Cloud Secrets)
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv() # Fallback to current dir or environment

class LLMEngine:
    def __init__(self, provider="deepseek"):
        self.provider = provider.lower()
        self.api_key = None
        self.base_url = None
        self.model = None
        
        self._configure()
        
        if not self.api_key:
            raise ValueError(f"API Key for {self.provider} not found in .env")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def _configure(self):
        if self.provider == "deepseek":
            self.api_key = os.getenv("DEEPSEEK_API_KEY")
            self.base_url = "https://api.deepseek.com"
            self.model = "deepseek-chat" # or deepseek-reasoner
        elif self.provider == "kimi":
            self.api_key = os.getenv("KIMI_API_KEY")
            self.base_url = "https://api.moonshot.cn/v1"
            self.model = "moonshot-v1-8k" # Standard Kimi model
        else:
            raise ValueError("Unsupported provider. Choose 'deepseek' or 'kimi'.")

    def generate(self, prompt, system_role="You are a helpful assistant."):
        """
        Generate a response from the LLM.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling {self.provider}: {str(e)}"

    def set_provider(self, provider):
        self.provider = provider
        self._configure()
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
