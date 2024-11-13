from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = OPENAI_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

def generate_image(client, prompt, size="1024x1024", model="dall-e-3", n=1):
    response = client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        n=n
    )
    return response.data[0].url

class Prompt(BaseModel):
    text: str

@app.get('/')
def homepage():
    return {"message": "success"}

@app.post('/generate_image')
async def gen_image(input_text: Prompt):
    text_prompt = input_text.text
    response = generate_image(client, prompt=text_prompt)
    return {'response': response}
