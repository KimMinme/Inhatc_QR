import qrcode

def make(file_name, data):
    myQR = qrcode.make(str(data))
    myQR.save("./qr/" + str(file_name) + ".png")