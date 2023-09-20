
from fastapi import FastAPI
import uvicorn
from sockets import sio_app

app = FastAPI()

app.mount("/", app = sio_app)

@app.get("/")
async def root():
    return {"test": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":

    # main.py를 실행할 때만 FastAPI 서버를 시작
    uvicorn.run('main:app', reload = True)