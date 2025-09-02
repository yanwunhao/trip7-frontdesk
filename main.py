from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from client import generate_response

app = FastAPI(title="trip7-hotel-frontdesk-service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://yuzawamd.com",
        "https://yuzawamd.com",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://localhost:8000",
        "https://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

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
