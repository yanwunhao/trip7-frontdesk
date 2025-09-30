import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from client import generate_response

from dsproxy import deepseek_response_proxy

load_dotenv(override=True)
ALLOWED_COMPANIES = os.getenv("ALLOWED_COMPANIES", "").split(",")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Loaded ALLOWED_COMPANIES: {ALLOWED_COMPANIES}")

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

        company = json_data["data"].get("company")

        if not company:
            raise HTTPException(status_code=500, detail="Company parameter is required")

        if company not in ALLOWED_COMPANIES:
            raise HTTPException(status_code=500, detail=f"Invalid company: {company}")

        # Handle additional_info based on company
        if company == "softusing":
            additional_info = json_data["data"].get("job_positions")
        else:
            additional_info = None

        lang = json_data["data"].get("lang", "jp")

        if lang not in ["cn", "jp", "en"]:
            lang = "jp"

        response = await deepseek_response_proxy(
            conversation_history,
            lang=lang,
            timeout=30,
            additional_info=additional_info,
            company=company,
        )

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

    # Extract content from response object
    if hasattr(response, "content"):
        response_content = response.content
    elif isinstance(response, str):
        response_content = response
    else:
        response_content = str(response)

    return {"message": response_content}


@app.get("/testfrontdesk")
async def test_chatbot():
    return FileResponse("static/testfrontdesk.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
