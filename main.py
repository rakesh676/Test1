from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_db_connection

app = FastAPI()

# Allow frontend from Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-test-phi-seven.vercel.app/"],  # replace with Vercel URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "FastAPI + Railway MySQL running"}

@app.get("/users")
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

@app.post("/users")
def create_user(name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name) VALUES (%s)", (name,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User created"}

