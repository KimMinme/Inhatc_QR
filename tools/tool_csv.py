import csv

def make(file_name, data):
    with open("./csv/" + str(file_name) + ".csv", mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        
        # 헤더를 쓰려면 필요하다면 아래 주석을 해제
        # writer.writerow(["거래일시", "의뢰인/수취인", "입금금액"])
        
        # 데이터 쓰기
        writer.writerow([data.studentId, data.studentName, data.studentPhoneNumber])

def get(file_name):
    with open("./csv/" + str(file_name) + ".csv", mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)  # Iterator
        
        return next(reader)
    
def get_graduates(file_name_1, file_name_2):
    mylist = []

    with open("./" + str(file_name_1) + ".csv", mode='r', newline='', encoding='cp949') as file:
        mydict = {}
        reader = csv.reader(file)  # Iterator

        # for row in reader:   학번이 key값인 딕셔너리
        #     mydict[row[0]] = row[1:]

        for row in reader:
            mylist.append(row[0])

    with open("./" + str(file_name_2) + ".csv", mode='r', newline='', encoding='cp949') as file:
        reader = csv.reader(file)  # Iterator
        for row in reader:
            mylist.append(row[0])

    return mylist


def append(file_name, *args):
    with open("./" + str(file_name) + ".csv", mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)

        writer.writerow(args)


if __name__ == "__main__":  # TEST 콘솔
    append('test', 'jwjung', '21', 2024)


    # 딕셔너리 합치기
    # dict(tmp2, **tmp)