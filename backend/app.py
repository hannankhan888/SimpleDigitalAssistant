from fastapi import FastAPI, WebSocket
import random

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            # Wait for any message from the client
            data = await websocket.receive_text()
            print(data)
            # Send message to the client
            resp = {'value': 1}
            await websocket.send_json(resp)
        except Exception as e:
            print('error:', e)
            break
    print('Hello..')