import aes

def test(data):
    key = aes.get_key("AES.key")
    output = aes.decrypt(data, key)

    return output

tmp = test("IesUSwKgd3tKbsgwglTorw==")
print(tmp)