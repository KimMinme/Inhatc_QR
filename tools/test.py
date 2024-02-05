from urllib.parse import quote, unquote

original_string = "http://jwjung.kro.kr:20000/?data=eHQrR5S8GvvQOcQJmhdY+g=="

url_safe_string = quote(original_string)
print(url_safe_string)
print(unquote(url_safe_string))