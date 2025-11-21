from fastapi import FastAPI, Request, HTTPException
import os
import requests

app = FastAPI()

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
RUNPOD_POD_ID = os.getenv("RUNPOD_POD_ID")
SECRET_KEY = os.getenv("SECRET_KEY")


@app.get("/")
def home():
    return {"status": "Webhook running"}


@app.get("/start")
def start_pod(key: str):
    if key != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid Key")

    query = """
    mutation PodStart($podId: String!) {
      podStart(input: {podId: $podId}) {
        id
        status
      }
    }
    """

    response = requests.post(
        "https://api.runpod.io/graphql",
        headers={"Authorization": f"Bearer {RUNPOD_API_KEY}"},
        json={
            "query": query,
            "variables": {"podId": RUNPOD_POD_ID}
        }
    )

    return response.json()
