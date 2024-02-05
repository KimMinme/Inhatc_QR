import pyairmore
from ipaddress import IPv4Address # for your IP address
from pyairmore.request import AirmoreSession # to create an AirmoreSession
from pyairmore.services.messaging import MessagingService # to send messages

def init():
    print("Airemore 서비스 실행됨")
    try:
        ip = IPv4Address("192.168.1.8")
        session = AirmoreSession(ip, 2333)
        service = MessagingService(session)

        if session.is_server_running:
            tmp = session.request_authorization()
            print(tmp)
            print("Connected with phone")
        return service
    except:
        print("Connect Failed")
        exit()

def send(service, phone_number, name, url):

    data = f"[2024 컴퓨터시스템과 학생회]\n학위복 대여/반납 개인 QR코드 안내\n\nURL : {url}\n{name}님의 졸업을 진심으로 축하드립니다 !"
    # data = "2024-02-05 pyAirmore Test"
    
    try:
        service.send_message(str(phone_number), data)
        print(f"{phone_number} 번호로 메시지 전송이 완료되었습니다.")
        return 1

    except:
        print("메시지 전송 실패")
        return 0
    
if __name__ == "__main__":
    service = init()
    phone_number = "01027075860"
    url = "http://jwjung.kro.kr/qr/show/?data=w08oaDZTs530oTtvmf1cug=="
    print(send(service, phone_number, url))