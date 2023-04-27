from fastapi import FastAPI, Body, HTTPException
import os
import openai

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_answer(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=question
    )
    return {
        "message": response['choices'][0]['message']['content'],
        "type": "INCOME",
        "create_at": ""
    }


@app.post("/send")
async def message(data=Body()):
    if len(data) >= 5:
        raise HTTPException(status_code=400, detail='Limit reached')
    messages = [{"role": "user" if el['type'] == "RECEIVED" else "assistant",
                 "content": el['message']
                 } for el in data]
    data.append(get_answer(messages))
    return data
