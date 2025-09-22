from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.models.fallback import FallbackModel
import os
from dotenv import load_dotenv


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

provider = GoogleProvider(api_key=GOOGLE_API_KEY)

main_model = GoogleModel('gemini-2.0-flash', provider=provider)

alt_model = GoogleModel('gemini-2.0-flash-lite', provider=provider)

fallback_model = FallbackModel(main_model, alt_model)