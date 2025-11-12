from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bainiAi import executeBainiAi

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

# define expected JSON format
class UserInput(BaseModel):
    user_input: str

# accept JSON body
@app.post("/")
async def handleUserInput(data: UserInput):
    response = executeBainiAi(data.user_input)
    return {"response": response}
