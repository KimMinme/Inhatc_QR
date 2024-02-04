import pyairmore
from ipaddress import IPv4Address # for your IP address
from pyairmore.request import AirmoreSession # to create an AirmoreSession
from pyairmore.services.messaging import MessagingService # to send messages
 
# Airmore 활성화
ip = IPv4Address("192.168.1.6")
 
session = AirmoreSession(ip, 2333)
service = MessagingService(session)

service.send_message("010-1234-5678", "pyairmore test message Made by Jiwon (2024-02-04)")
print("Clear")