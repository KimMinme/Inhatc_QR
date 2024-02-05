from urllib.parse import quote, unquote

original_string = "eHQrR5S8GvvQOcQJmhdY+g=="

url_safe_string = quote(original_string)
print(url_safe_string)
print(unquote(url_safe_string))
print(len(unquote(url_safe_string)))