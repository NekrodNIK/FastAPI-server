from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from datetime import datetime
from time import time
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
	username: str
	password: str
	text: str


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

@app.get("/send_message")
@app.post("/send_message")
async def send_message(item:Item):
	botegtext = ""
	r = item
	username = item.username
	password = item.password
	text = item.text
	if username in users:
		if users[username] != password:
			return {"ok": "false"}
	else:
		users[username] = password
	messages.append({
					"username": username,
					"text": text,
					"timestamp": time(),
					})
	return {"ok": "true"}

@app.get("/get_messages")
async def get_messages(after: float = 0):
	result = []
	for message in messages:
		if message["timestamp"] > after:
			result.append(message)
	return{
		"messages": result
	}


if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)