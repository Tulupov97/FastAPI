from fastapi import FastAPI, status, Body, HTTPException
from pydantic import BaseModel
app = FastAPI()

class Message(BaseModel):
    id: int
    content: str

# Модель для входных данных (запросов: создание и обновление)
class MessageCreate(BaseModel):
    content: str

messages_db: list[Message] = [Message(id= 0, content= "First post in FastAPI")]

@app.get("/messages", response_model=list[Message])
async def read_messages() -> list[Message]:
    return messages_db

@app.get("/messages/{message_id}", response_model=Message)
async def read_message(message_id: int) -> Message:
    return messages_db[message_id]

@app.post("/messages", status_code=status.HTTP_201_CREATED, response_model=Message)
async def create_message(message: Message) -> Message:
    # Проверяем, что предоставленный ID уникален
    if any(msg.id == message.id for msg in messages_db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The message ID already exists")
    messages_db.append(message)
    return message

# PUT /messages/{message_id}: Обновление существующего сообщения
@app.put("/messages/{message_id}", response_model=Message)
async def update_message(message_id: int, updated_message: Message) -> Message:
    # Проверяем, что ID в теле запроса совпадает с ID в пути
    if updated_message.id != message_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The ID in the request body must match the ID in the path")
    for i, message in enumerate(messages_db):
        if message.id == message_id:
            messages_db[i] = updated_message
            return updated_message
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")


# DELETE /messages/{message_id}: Удаление одного сообщения
@app.delete("/messages/{message_id}", status_code=status.HTTP_200_OK)
async def delete_message(message_id: int) -> dict:
    for i, message in enumerate(messages_db):
        if message.id == message_id:
            messages_db.pop(i)
            return {"detail": f"Message ID={message_id} deleted!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")


# DELETE /messages: Удаление всех сообщений
@app.delete("/messages", status_code=status.HTTP_200_OK)
async def delete_messages() -> dict:
    messages_db.clear()
    return {"detail": "All messages deleted!"}


