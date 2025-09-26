from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from client import generate_response

from dsproxy import deepseek_response_proxy

app = FastAPI(title="trip7-hotel-frontdesk-service")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/dsproxy")
async def deepseek_proxy(request: Request):
    try:
        json_data = await request.json()

        if "data" not in json_data or "conversation_history" not in json_data["data"]:
            raise HTTPException(status_code=400, detail="Invalid request format")

        conversation_history = json_data["data"]["conversation_history"]
        lang = json_data["data"].get("lang", "jp")

        if lang not in ["cn", "jp", "en"]:
            lang = "jp"

        response = await deepseek_response_proxy(conversation_history, lang=lang, timeout=30)

        return {"message": response}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/invoke")
async def invoke_frontdesk_service(request: Request):
    json_data = await request.json()

    conversation_history = json_data["data"]["conversation_history"]
    lang = json_data["data"].get("lang", "jp")

    if lang not in ["cn", "jp", "en"]:
        lang = "jp"

    response = generate_response(conversation_history=conversation_history, lang=lang)

    return {"message": response}


@app.get("/testfrontdesk")
async def test_chatbot():
    return FileResponse("static/testfrontdesk.html")


@app.get("/testdsproxy")
async def test_dsproxy():
    return FileResponse("static/testdsproxy.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
