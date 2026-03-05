from langchain_groq import ChatGroq
import os

# Groq API key - REPLACE WITH YOUR KEY
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"

# Using Groq with Llama 3.1 8B (faster, still good quality)
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=GROQ_API_KEY,
    max_tokens=500  # Limit response length for speed
)

# Database configuration
DB_CONFIG = {
    "dbname": "ecommerce_support",
    "user": "postgres",
    "password": "YOUR_PASSWORD_HERE",
    "host": "localhost"
}
