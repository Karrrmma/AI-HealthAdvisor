import pandas as pd
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API")

if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set 'OPENAI_API' in your .env file.")

# Load NHS dataset
df = pd.read_csv('nhs_conditions_batch_data.csv')

# Print OpenAI API key and dataframe columns for verification
print(f"Loaded OpenAI API Key: {openai.api_key[:5]}...")  # Print the first few characters for security
print("Dataframe Columns:", df.columns)
