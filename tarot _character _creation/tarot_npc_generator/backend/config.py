import os

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-86e300e5fa8b456f9e8211ae6559ae8c")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")