# 입력 폼
# DB 저장
# 문자 발송

# qr 발급


from pydantic import BaseModel

import tool_csv
import tool_aes
import tool_qr

class Input(BaseModel):
    code: int
    name: str
    phone: str


def register(data : Input):
    tmp = {}
    tmp['학번'] = data.code
    tmp['이름'] = data.name
    tmp['전화번호'] = data.phone

    # CSV 저장 
    tool_csv.make(data.code, tmp)

    # 학번 암호화
    key = tool_aes.get_key("AES.key")
    encrypted_code = tool_aes.encrypt(data.code, key)

    # QR 코드 생성 (암호화된 학번)
    tool_qr.make(data.code, encrypted_code)


    return tmp


def rq_by_admin(data):
    # QR Data 복호화 (학번)
    key = tool_aes.get_key("AES.key")
    code = tool_aes.decrypt(data, key)

    # 해당 학번 CSV 파일 조회
    mylist = tool_csv.get(code)

    return mylist



if __name__ == "__main__":
    register(Input(code=202345123, name='카리나', phone='010-1234-5678'))

    qr_data = "eHQrR5S8GvvQOcQJmhdY+g=="
    result = rq_by_admin(qr_data)

    print(result)