import qrcode

def make(file_name, data):
    myQR = qrcode.make("http://jwjung.kro.kr:20000/qr/verify/?data=" + str(data))
    myQR.save("./qr/" + str(file_name) + ".png")