from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
from datetime import datetime
from time import time

app = FastAPI()

messages = [
	{
		"username": "Jack",
		"text": "hello",
		"timestamp": time(),
	},
	{
		"username": "Jack2",
		"text": "helloyyyyy",
		"timestamp": time(),
	}
		]

users = {
		"jack": "12345",
		"jack2": "123456"
		}


@app.get("/")
async def hello():
	return HTMLResponse(content="Hello,user! <a href=/status>Статус MoreliaTalk</a>", status_code=200)

@app.get("/status")
async def status():
	i = 0
	mi = 0
	# Не трогать!
	for user in users:i+=1
	for mes in messages:mi+=1
	return {
			"status": "true",
			"name": "Pocegram",
			"time": str(datetime.now().time())[:8],
			"current_time_seconds": time(),
			"count_users": i,
			"count_messages": mi
			}

@app.websocket("/send_message")
async def send_message(websocket: WebSocket):
	await websocket.accept()
	while True:
		r = await websocket.receive_json()
		username = r["username"]
		password = r["password"]
		text = r["text"]
		if username in users:
			if users[username] != password:
				await websocket.send_json({"ok": "false"})
				return ""
		else:
			users[username] = password
		messages.append({
						"username": username,
						"text": text,
						"timestamp": time(),
						})
		await websocket.send_json({"ok": "true"})

@app.websocket("/get_messages")
async def get_messages(websocket: WebSocket):
	await websocket.accept()
	while True:
		after = await websocket.receive_json()
		result = []
		for message in messages:
			if message["timestamp"] > after:
				result.append(message)
		await websocket.send_json({
			"messages": result
		})


if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)