from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/reset")
def reset():
    try:
        output = subprocess.getoutput("python inference.py")
        return {"output": output}
    except Exception as e:
        return {"error": str(e)}
