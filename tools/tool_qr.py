import qrcode

def make(file_name, url):
    myQR = qrcode.make(str(url))
    myQR.save("./qr/" + str(file_name) + ".png")