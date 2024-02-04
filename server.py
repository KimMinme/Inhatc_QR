from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel  

app = FastAPI()
templates = Jinja2Templates(directory="./")




class Input(BaseModel):
    tmp: str


@app.get("/register")
async def register_get(request: Request):
    return templates.TemplateResponse("register.html",{"request":request})


@app.post("/register")
def postRequest(data : Input): 
    return str(data.tmp)




# CORS 문제 해결, 일단 무시할 것
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, # cookie 포함 여부를 설정한다. 기본은 False
    allow_methods=["*"],    # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
    allow_headers=["*"],	# 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
)