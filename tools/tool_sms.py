import pyairmore
from ipaddress import IPv4Address # for your IP address
from pyairmore.request import AirmoreSession # to create an AirmoreSession
from pyairmore.services.messaging import MessagingService # to send messages

def init():
    try:
        ip = IPv4Address("192.168.1.6")
        session = AirmoreSession(ip, 2333)
        service = MessagingService(session)

        if session.is_server_running:
            session.request_authorization()
            print("Connected with phone")
        return service
    except:
        print("Connect Failed")
        exit()

def send(service, phone_number, url):
    ip = IPv4Address("192.168.1.6")
        
    session = AirmoreSession(ip, 2333)
    service = MessagingService(session)


    data = '''[2024 컴퓨터시스템과 학생회]
학위복 대여/반납 개인 QR코드 안내

''' + url
    
    try:
        service.send_message(str(phone_number), data)
        print("Clear")
        return 1

    except:
        return 0
    
if __name__ == "__main__":
    phone_number = "01027075860"
    url = "http://jwjung.kro.kr/qr/show/?data=w08oaDZTs530oTtvmf1cug=="
    print(send(phone_number, url))
    print("clear")