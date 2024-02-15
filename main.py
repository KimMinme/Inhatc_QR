# 학번, 이름, 전화번호 입력
# 분실시 개인 책임을 명시, 동의받기
# 졸업자 명단과 대조 후 qr 링크 발급

# 해당 링크로 접속시 유효한 qr 코드 사진 제공
# 전화번호로 링크가 포함된 안내 문자메시지 전송

# 학사복 대여, 반납시 담당자는 개개인의 qr을 스캔.
# 누가 언제 빌려가고 반납했는지 DB에 기록


from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from tools import tool_csv, tool_aes, tool_qr, tool_signature, tool_sms
from urllib.parse import quote, unquote

from datetime import datetime
from uuid import UUID, uuid4

app = FastAPI()
app.mount("/page", StaticFiles(directory="page"), name="page")
templates = Jinja2Templates(directory="./")

airmore_service = tool_sms.init()

graduates = tool_csv.get_graduates("전공심화 csv", "졸업자 csv")
graduates.append('202345123')  # admin
graduates.append('202346123')

sessions_rental = []  # 발급된 렌탈 관리자 세션
sessions_return = []  # 발급된 반납 관리자 세션
users = []  # 현재 대여중인 사람 명단

class Input(BaseModel):
    studentId: str  # 202345123
    studentName: str  # 카리나
    studentPhoneNumber: str  # 010-1234-5678
    URL: str  # image 

class Password(BaseModel):
    password: str


@app.get("/register")
async def register_get(request: Request):
    return templates.TemplateResponse("./page/form.html",{"request":request})

# @app.get("/register")
# async def register_get(request: Request):
#     return templates.TemplateResponse("register.html",{"request":request})

@app.post("/register") 
def register(data : Input):
    if len(data.studentId) == 9 and len(data.studentPhoneNumber) == 11:
        # 졸업자 명단에 있는지 확인
        if not(data.studentId in graduates):
            return {'isIn':False}
        # CSV 저장 
        tool_csv.make(data.studentId, data)

        # Signature 저장
        tool_signature.make(data.studentId, data.URL)

        # 학번 암호화
        key = tool_aes.get_key("AES.key")
        encrypted_code = tool_aes.encrypt(data.studentId, key)
        print(encrypted_code)

        # QR 코드 생성 (암호화된 학번)
        url_safe_code = quote(encrypted_code)
        veryfy_url = "http://jwjung.kro.kr:20000/qr/rental/?data=" + url_safe_code
        tool_qr.make(data.studentId, veryfy_url)

        # 문자메시지 전송
        private_url = "http://jwjung.kro.kr:20000/qr/show/?data=" + url_safe_code
        print(private_url)

        is_sended = tool_sms.send(airmore_service, data.studentPhoneNumber, data.studentName, private_url)
        print(is_sended)

        return {'isIn':True}
    else:
        return "Invalid Student ID"


@app.get("/qr/show/")
def show(data:str = "0"):
    data = unquote(data)
    if len(data) == 24:
        try:
            key = tool_aes.get_key("AES.key")
            student_id = tool_aes.decrypt(data, key)

            image_path = "./qr/" + str(student_id) + ".png"

            return FileResponse(image_path, media_type="image/png")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        return "Invalid Student ID"



@app.get("/qr/verify/")
def getRealInfo(data: str = "0"):
    data = unquote(data)
    print(data)
    if data == "0":
        return "Not Found"
    else:
        key = tool_aes.get_key("AES.key")
        code = tool_aes.decrypt(data, key)

        mylist = tool_csv.get(code)

        return mylist

# ---------------------------------------------------------------------------------------

@app.get("/qr/rental")
def rental_(request: Request, data: str = "0"):
    if data == "0":
        return "Not Found"
    
    cookies = request.cookies
    try:
        print(cookies['SESSIONID'])
    except:
        return {"Result":"허가받지 않은 사용자의 접근입니다."}

    key = tool_aes.get_key("AES.key")
    code = tool_aes.decrypt(data, key)

    mylist = tool_csv.get(code)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 현재시간

    if cookies['SESSIONID'] in sessions_rental:
        users.append(code)
        if code[0:4] == '2023':
            category = '컴퓨터시스템공학'
            tool_csv.append("2024 학위수여식 학위복 대여_컴퓨터시스템공학", current_time, mylist[0], mylist[1])
        else:
            category = "컴퓨터시스템"
            tool_csv.append("2024 학위수여식 학위복 대여_컴퓨터시스템", current_time, mylist[0], mylist[1])

        print(str(mylist[1]) +" 님의 학위복 대여가 시작되었습니다.")
        return {'Result':str(mylist[1]) +" 님의 학위복 대여가 시작되었습니다."}
    
    elif cookies['SESSIONID'] in sessions_return:
        users.remove(code)
        if code[0:4] == '2023':
            category = '컴퓨터시스템공학'
            tool_csv.append("2024 학위수여식 학위복 반납_컴퓨터시스템공학", current_time, mylist[0], mylist[1])
        else:
            category = "컴퓨터시스템"
            tool_csv.append("2024 학위수여식 학위복 반납_컴퓨터시스템", current_time, mylist[0], mylist[1])

        print(str(mylist[1]) +" 님의 학위복 반납 처리를 완료했습니다.")
        return {'Result':str(mylist[1]) +" 님의 학위복 반납 처리를 완료했습니다."}


# @app.get("/admin/")
# def password(data: str = "0"):
#     print(data)
#     if data.password == '1111':
#         return {'url':"http://jwjung.kro.kr/admin/rental/코드"}
#     else:
#         return {'url':"notFound"}

@app.get("/session/rental")  # 렌탈 관리자 세션 발급
def password(data: str = "0"):
    session_id = str(uuid4())
    sessions_rental.append(session_id)
    content = {'SESSIONID': session_id}
    response = JSONResponse(content=content)
    response.set_cookie(key="SESSIONID", value=session_id, path='/qr/rental', domain=None, max_age=43200, expires=43200)

    return response

@app.get("/session/return")  # 반납 관리자 세션 발급
def password(data: str = "0"):
    session_id = str(uuid4())
    sessions_return.append(session_id)
    content = {'SESSIONID': session_id}
    response = JSONResponse(content=content)
    response.set_cookie(key="SESSIONID", value=session_id, path='/qr/rental', domain=None, max_age=43200, expires=43200)

    return response






@app.post("/admin")  # QR코드 내의 AES 암호화된 문자열을 담은 POST 요청이 오면 //아직 사용안함
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
    allow_origins=["http://jwjung.kro.kr:20000"],
    allow_credentials=True, # cookie 포함 여부를 설정한다. 기본은 False
    allow_methods=["*"],    # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
    allow_headers=["*"],	# 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
)