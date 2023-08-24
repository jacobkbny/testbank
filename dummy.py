import mysql.connector
from faker import Faker
import random
fake = Faker()
dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="jacob0322",
)
cursorObject = dataBase.cursor()

cursorObject.execute("create DataBase Toss")

# create table Trxs(
# 	ID int NOT NULL auto_increment,
#     sender_index int,
#     sender_bank varchar(255),
#     receiver_index int,
#     receiver_bank varchar(255),
#     amount int,
#     primary key (ID)
# );

dataBase.commit()

cursorObject.execute("use Toss")

class Bank:
    def __init__(self):
        self.name = None
        self.index = 0
        self.owner = None
        self.account = None
        self.activation = True
        self.balance = 0
        self.password = None
        
def generate_bank_account():
    first_part = str(random.randint(1000000, 1999999))
    second_part = str(random.randint(10, 99))
    last_part = str(random.randint(1000000, 1999999))
    return first_part + "-" + second_part + "-" + last_part

def create_table():
    all_bank = {
        1: "KB",
        2: "HANA",
        3: "IBK",
        4: "NH",
        5: "WR",
    }
    for i in range (1,6):
        sql = f"""
            create table {all_bank[i]}  (
                ID int NOT NULL AUTO_INCREMENT,
                Owner varchar(255),
                AccountNumber varchar(255),
                Password varchar(255),
                Balance int,
                PRIMARY KEY (ID)
            )
        """
        cursorObject.execute(sql)
        dataBase.commit()
        
def create_query(bank_name, bank):
    global cursorObject
    sql = f"""
    Insert into {bank_name} (Owner,AccountNumber,Password,Balance) values ('{bank.owner}','{bank.account}','{bank.password}','{bank.balance}')
    """
    cursorObject.execute(sql)
    return

    
def create_fake_users():
    bank = Bank()
    all_bank = {
        1: "KB",
        2: "HANA",
        3: "IBK",
        4: "NH",
        5: "WR",
    }
    bank_name = all_bank[random.randint(1, 5)]
    bank.owner = fake.name()
    bank.account = generate_bank_account()
    bank.activation = True
    bank.password = random.randint(1000, 9999)
    bank.balance = 0
    print("은행: ", bank_name, " 계좌번호: ", bank.account)
    create_query(bank_name, bank)
    dataBase.commit()
    
def update_balance(bank_name, amount, index):
    global cursorObject
    sql = f"""
    Update {bank_name} set Balance = {amount} WHERE ID = {index}
"""
    cursorObject.execute(sql)
    dataBase.commit()
    return

def save_transaction(sender_index, sender_bank, receiver_index, receiver_bank, amount):
    global cursorObject
    sql = f"""
        Insert into Trxs (sender_index , sender_bank , receiver_index , receiver_bank , amount) values ({sender_index},'{sender_bank}',{receiver_index},'{receiver_bank}',{amount})
        """
    cursorObject.execute(sql)
    dataBase.commit()
    return


def fetch_all_bank_total_index():
    all_bank = {
        1: "KB",
        2: "HANA",
        3: "IBK",
        4: "NH",
        5: "WR",
    }
    for i in range(1, 6):
        sql = f"""SELECT Count(*) from {all_bank[i]}"""
        cursorObject.execute(sql)
        result = cursorObject.fetchall()
        # bank_name , amount , index
        print("bank name:", all_bank[i], "result:", result[0][0])
        for j in range(1, result[0][0] + 1):
            update_balance(all_bank[i], 10000000, j)
    print("finish update all balance")
def fetch_client_detail(bank_name, index):
    global cursorObject
    number_index = int(index)
    sql = f"""
    SELECT * from {bank_name} where ID = {number_index}
        """
    cursorObject.execute(sql)
    result = cursorObject.fetchall()
    bank = Bank()
    bank.name = bank_name
    bank.index = result[0][0]
    bank.owner = result[0][1]
    bank.account = result[0][2]
    bank.password = result[0][3]
    bank.balance = result[0][4]
    return bank



def massive_fake_trxs():
    all_bank = {
        1: "KB",
        2: "HANA",
        3: "IBK",
        4: "NH",
        5: "WR",
    }
    total_bank_records = {"KB": 0, "HANA": 0, "IBK": 0, "NH": 0, "WR": 0}
    for i in range(1, 6):
        sql = f"""SELECT Count(*) from {all_bank[i]}"""
        cursorObject.execute(sql)
        result = cursorObject.fetchall()
        total_bank_records[all_bank[i]] = result[0][0]
    for i in range(10000):
        amount = random.randint(1000, 100000)  # 송금 가격 설정
        sender_bank_index = random.randint(1, 5)  # all_bank 에서 은행을 가져오기 위해 랜덤 숫자 생성
        sender_bank_name = all_bank[sender_bank_index]  # 랜덤으로 생성된 숫자 넣어서 은행 선택
        total_sender_bank_index = total_bank_records[
            sender_bank_name
        ]  # 선택된 은행을 넣고 토탈 인덱스 꺼내기
        sender_index = random.randint(
            2, total_sender_bank_index
        )  # 1 부터 토탈 인텍스중에 랜덤 숫자 하나 고르기
        sender_bank_detail = fetch_client_detail(
            sender_bank_name, sender_index
        )  # 송금자 정보 가져오기
        update_balance(
            sender_bank_detail.name,
            (sender_bank_detail.balance - amount),
            sender_bank_detail.index,
        )  # 송금 진행
        receiver_bank_index = random.randint(1, 5)  #
        receiver_bank_name = all_bank[receiver_bank_index]
        total_receiver_bank_index = total_bank_records[receiver_bank_name]
        receiver_index = random.randint(2, total_receiver_bank_index)
        receiver_bank_detail = fetch_client_detail(receiver_bank_name, receiver_index)
        update_balance(
            receiver_bank_detail.name,
            (receiver_bank_detail.balance + amount),
            receiver_bank_detail.index,
        )
        save_transaction(
            sender_bank_detail.index,
            sender_bank_detail.name,
            receiver_bank_detail.index,
            receiver_bank_detail.name,
            amount,
        )
        print(
            "sender: ",
            sender_bank_detail.owner,
            " receiver: ",
            receiver_bank_detail.owner,
            " amount: ",
            amount,
        )
    return





# create_table()
for i in range(1000):
        create_fake_users()
fetch_all_bank_total_index()
for i in range(10000):
    massive_fake_trxs()
