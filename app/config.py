import os
import sys

REQUIRED_ENV_VARS = ["GROQ_API_KEY", "COMPOSIO_API_KEY"]

missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

if missing_vars:
    print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
    print("Please ensure .env file exists and all required variables are set.")
    sys.exit(1)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")