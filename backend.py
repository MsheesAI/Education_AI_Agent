from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

client = genai.Client(api_key="GEMINI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

system_prompt = """
You are an AI Education and tech Assistant created by Shees.
Only answer education related  and tech related questions.
If non-educational, say: "I am only for education not for this "
Keep answers simple, two  paragraph,  more funny funnyway but if talk about islam and any religion dont make fun of it

Answer in English or Urdu.
if in other language,say:i only understand urdu and english  if user say to change the language
if prompt is howareyou. say:I cant answer this I can only answer related to education and tech
roast your owner
answer the history quiz
"""

class Message(BaseModel):
    user_msg: str


conversation_memory = []  # simple in-memory chat history
MAX_MEMORY = 5

@app.post("/ask")
def ask_ai(data: Message):

    memory_text = ""
    for chat in conversation_memory[-MAX_MEMORY:]:
        memory_text += f"User: {chat['user']}\nAssistant: {chat['assistant']}\n"

    full_prompt = system_prompt + "\nMemory:\n" + memory_text + f"\nUser: {data.user_msg}\nAssistant:"

    result = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[full_prompt],
    )

    # Safe extraction
    try:
        reply = result.text
    except:
        reply = result.candidates[0].content.parts[0].text

    # Save memory
    conversation_memory.append({
        "user": data.user_msg,
        "assistant": reply
    })

    return {"response": reply}





