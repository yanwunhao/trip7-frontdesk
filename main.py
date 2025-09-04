from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from util import load_hotel_introduction
from client import generate_response
from model import create_frontdesk_chain

app = FastAPI(title="trip7-hotel-frontdesk-service")

app.mount("/static", StaticFiles(directory="static"), name="static")

frontdesk_chain = create_frontdesk_chain(
    model_name="qwen3:32b",
    system_prompt_filepath="./prompts/system_prompt.md",
    bot_name="郑小飞",
    hotel_name="Trip7箱根仙石原温泉ホテル",
    hotel_description=load_hotel_introduction("./documents/hotel_introd.txt"),
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/invoke")
async def invoke_frontdesk_service(request: Request):
    json_data = await request.json()

    conversation_history = json_data["data"]["conversation_history"]
    response = generate_response(
        frontdesk_chain, conversation_history=conversation_history
    )

    return {"message": response}


@app.get("/test")
async def test_chatbot():
    return FileResponse("static/testpage.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
