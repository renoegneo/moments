from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Разрешаем фронтенду обращаться к бэку
origins = [
    "http://localhost:3000",  # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Разрешённые источники
    allow_credentials=True,
    allow_methods=["*"],            # Разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*"],            # Разрешаем все заголовки
)

@app.get("/")
def root():
    return {"message": "Backend работает и готов принимать запросы 🚀"}
