from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from client import generate_response

app = FastAPI(title="trip7-hotel-frontdesk-service")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/invoke")
async def invoke_frontdesk_service(request: Request):
    json_data = await request.json()

    conversation_history = json_data["data"]["conversation_history"]
    response = generate_response(conversation_history=conversation_history)

    return {"message": response}


@app.get("/test")
async def test_chatbot():
    return FileResponse("static/testpage.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
