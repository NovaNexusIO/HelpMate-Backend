from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI(title="User Database API")

DB_FILE = "db.json"

# ---------- Database helpers ----------
def load_data():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Data model ----------
class User(BaseModel):
    name: str
    email: str
    phoneno: str
    password: str

# ---------- Routes ----------
@app.post("/users")
def add_user(user: User):
    data = load_data()

    # Check for duplicate email
    if any(u["email"] == user.email for u in data):
        raise HTTPException(status_code=400, detail="User with this email already exists")

    data.append(user.dict())
    save_data(data)
    return {"message": f"User {user.name} added successfully"}

@app.get("/users")
def get_users():
    data = load_data()
    return data

@app.get("/users/{email}")
def get_user_by_email(email: str):
    data = load_data()
    for user in data:
        if user["email"] == email:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{email}")
def delete_user(email: str):
    data = load_data()
    new_data = [u for u in data if u["email"] != email]
    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="User not found")
    save_data(new_data)
    return {"message": f"User with email {email} deleted"}

# Run this API with:
# uvicorn api:app --reload

