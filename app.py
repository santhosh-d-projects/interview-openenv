from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def run_env():
    result = subprocess.getoutput("python inference.py")
    return {"output": result}
