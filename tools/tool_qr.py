import qrcode

def make(file_name, url):
    myQR = qrcode.make(str(url))
    myQR.save("./qr/" + str(file_name) + ".png")

if __name__ == "__main__":
    make("register","http://jwjung.kro.kr:20000/register")