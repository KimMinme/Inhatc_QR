# 학번, 이름, 전화번호 입력
# 분실시 개인 책임을 명시, 동의받기
# 졸업자 명단과 대조 후 qr 링크 발급

# 해당 링크로 접속시 유효한 qr 코드 사진 제공
# 전화번호로 링크가 포함된 안내 문자메시지 전송

# 학사복 대여, 반납시 담당자는 개개인의 qr을 스캔.
# 누가 언제 빌려가고 반납했는지 DB에 기록


from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from tools import tool_csv
from tools import tool_aes
from tools import tool_qr

app = FastAPI()
templates = Jinja2Templates(directory="./")

class Input(BaseModel):
    studentId: str  # 202345123
    studentName: str  # 카리나
    studentPhoneNumber: str  # 010-1234-5678
    URL: str  # image 

class Verify(BaseModel):
    encrypted: str

app.mount("/page", StaticFiles(directory="page"), name="page")

@app.get("/seihoonlee")
async def register_get(request: Request):
    return templates.TemplateResponse("./page/form.html",{"request":request})

@app.get("/register")
async def register_get(request: Request):
    return templates.TemplateResponse("register.html",{"request":request})

@app.post("/register") 
def register(data : Input):
    tmp = {}
    tmp['학번'] = data.studentId
    tmp['이름'] = data.studentName
    tmp['전화번호'] = data.studentPhoneNumber
    tmp['Image'] = data.URL
    print(tmp)

    # CSV 저장 
    tool_csv.make(data.studentId, tmp)

    # 학번 암호화
    key = tool_aes.get_key("AES.key")
    encrypted_code = tool_aes.encrypt(data.studentId, key)
    print(encrypted_code)

    # QR 코드 생성 (암호화된 학번)
    tool_qr.make(data.studentId, encrypted_code)

    return tmp




@app.post("/admin")  # QR코드 내의 AES 암호화된 문자열을 담은 POST 요청이 오면,
def rq_by_admin(data):
    # QR Data 복호화 (학번)
    key = tool_aes.get_key("AES.key")
    code = tool_aes.decrypt(data, key)

    # 해당 학번 CSV 파일 조회
    mylist = tool_csv.get(code)

    return mylist


# CORS 문제 해결, 일단 무시할 것
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, # cookie 포함 여부를 설정한다. 기본은 False
    allow_methods=["*"],    # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
    allow_headers=["*"],	# 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
)