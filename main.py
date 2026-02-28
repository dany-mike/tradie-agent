from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Tradie Agent is running"}

@app.post("/sms")
def receive_sms():
    return {"message": "SMS received"}
