from fastapi import FastAPI
from app.routers.router import api_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from app.database.db import init_db
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()


origins = [
    "*",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)




@app.on_event("startup")
async def startup_event():
    await init_db()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
   errors={}
   for error in exc.errors():
       field = error['loc'][-1]
       message = error['msg']
       errors[field] = message

   return JSONResponse(
       status_code=422,
       content={"error": errors},
   )


@app.get("/")
async def read_root():
    return {"Hello": "World","message":os.environ.get('APP_NAME')}
