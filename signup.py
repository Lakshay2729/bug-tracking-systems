import mysql.connector


class module_a:
    def __init__(self):
        print(" ")

    def getBTSDatabase(self):
        db = mysql.connector.connect(host="localhost", database="bts", user="root", password="")
        return db

    def login(self, empType=None):
        print("welcome to login page")
        who = input("who are you : customer / employee ")
        if who == "customer":
            custLogin = input("enter custLoginId: ")
            custpassword = input("enter  custPassword:")

            db = self.getBTSDatabase()
            mycursor = db.cursor()

            sql = "select * from customer where custLoginId= '%s'"
            value = custLogin

            mycursor.execute(sql % value)

            try:
                row = mycursor.fetchmany(1)[
                    0]  # here,  fetch me one row and give me first row,  i'll get one record or we not get one record which mean more than one.
                dbPass = row[1]
                if custpassword == dbPass:
                    print("login authentication success----")
                    Login = row[0]
                    if custLogin == Login :
                        print("welcome", custLogin)
                    else:
                        print('login authentication failed')

            except IndexError:
                print("Invalid id retry...")

            db.commit()
            db.close()
        elif who == "employee":
            empLogin = input("enter empLoginId: ")
            emppassword = input("enter  empPassword:")

            db = self.getBTSDatabase()
            mycursor = db.cursor()

            sql = "select * from employee where empLoginId= '%s'"
            value = empLogin

            mycursor.execute(sql % value)

            try:
                row = mycursor.fetchmany(1)[0]  # here,  fetch me one row and give me first row,  i'll get one record or we not get one record which mean more than one.
                dbPass = row[1]
                if emppassword == dbPass:
                    print("login authentication success----")
                    empType = row[2]
                    if empType == "Admin" or empType == "Expert":
                        print("welcome", empType)
                    else:
                        print('login authentication failed')

            except IndexError:
                print("Invalid id retry...")

            db.commit()
            db.close()

    def signup(self):
        print("welcome to signup page")
        db = self.getBTSDatabase()
        mycursor = db.cursor()

        custLoginId = input("enter login-id:")
        custPassword = input("enter password:")
        custName = input("enter name:")
        custAge = int(input("enter age"))
        custPhone = input("enter phone no:")
        custEmail = input("enter email:")
        # empStatus = input("enter phone no:")

        sql = "insert into customer(custLoginId, custPassword, custName, custAge, custPhone, custEmail)value('%s', '%s', '%s', %d, '%s', '%s')"

        value = (custLoginId, custPassword, custName, custAge, custPhone, custEmail)

        # 1st way------
        # print("sql", sql % value)
        # mycursor.execute(sql % value)

        # 2nd way -------
        complete_sql = sql % value
        print(complete_sql)
        mycursor.execute(complete_sql)

        print("Signup successfully for ", custLoginId)
        mycursor.close()
        db.commit()

    def type_correctly(self):
        print("press again correctly")


print("Welcome")
user = input("* If you have already account: For login = press l \n-For creating new account: Type signup = press s\n")

module_a = module_a()  # Create an instance of the ModuleA class

# Call the method on the instance
if user == "l":
    module_a.login()
elif user == "s":
    module_a.signup()
else:
    module_a.type_correctly()
