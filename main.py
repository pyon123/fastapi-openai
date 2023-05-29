from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import openai

class ContentType(Enum):
    title = "title"
    description = "description"
    about = "about"

class Action(Enum):
    rephrase = "rephrase"

class ProductDetails(BaseModel):
    name: str
    description: str

class RequestData(BaseModel):
    content_type: ContentType
    action: Action
    product_details: ProductDetails
    keywordList: list[str] = []

app = FastAPI()

openai.organization =  os.getenv("OPENAI_ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/rephrase")
async def rephrase(req: RequestData):
    try:
        user_messages = [
            {'role': 'system', 'content': f'You are a {req.content_type} generation system.'},
            {'role': 'user', 'content': f'Given the product details: {req.product_details} and keywords: {req.keywordList}, suggest a rephrased {req.content_type}.'}
        ]

        # Send a series of messages to the ChatGPT model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=user_messages,
            max_tokens=50,  # Adjust the max tokens based on the desired response length
            n=3,  # Adjust the number of suggestions you want to receive
            stop=None,  # Add a stop condition if needed
        )

        # Extract the generated suggestions from the model's responses
        suggestions = [message['message']['content'].replace("\"", "") for message in response['choices']]

        return { "choices": suggestions }
    except Exception as e:
        # Handle any other unexpected exceptions
        raise HTTPException(status_code=500, detail="An error occurred during division.")