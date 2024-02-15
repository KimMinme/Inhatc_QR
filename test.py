from tools import tool_csv
from datetime import datetime

code = '202345047'
mylist = tool_csv.get(code)


current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 현재시간

if code[0:4] == '2023':
    category = '컴퓨터시스템공학'
    tool_csv.append("2024 학위수여식 학위복 대여_컴퓨터시스템공학", current_time, mylist[0], mylist[1])
else:
    category = "컴퓨터시스템"
    tool_csv.append("2024 학위수여식 학위복 대여_컴퓨터시스템", current_time, mylist[0], mylist[1])