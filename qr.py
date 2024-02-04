import qrcode

myQR = qrcode.make("https://www.naver.com")
myQR.save("filename_temp01.png")