from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.models.fallback import FallbackModel
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
import os
from dotenv import load_dotenv


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

provider = GoogleProvider(api_key=GOOGLE_API_KEY)

main_model = GoogleModel('gemini-2.0-flash', provider=provider)

alt_model = GoogleModel('gemini-2.0-flash-lite', provider=provider)

fallback_model = FallbackModel(main_model, alt_model)


testing_model = OpenAIChatModel(
    model_name='llama3.2:latest', 
    provider=OllamaProvider(base_url="http://localhost:11434/v1")
    )