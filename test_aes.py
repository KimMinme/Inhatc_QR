from tools import tool_aes

def test(data):
    key = tool_aes.get_key("AES.key")
    output = tool_aes.decrypt(data, key)

    return output

tmp = test("IesUSwKgd3tKbsgwglTorw==")
print(tmp)