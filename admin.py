import mysql.connector


class getBTSDB:
    db = mysql.connector.connect(host="localhost", database="bts", user="root", password="")


class customer_service(getBTSDB):
    def __init__(self):
        print("")

    def view_customer(self):
        print("--------------------customer_service_List---------------------")
        mycursor = self.db.cursor()

        sql = "SELECT * FROM customer ORDER BY custLoginId DESC"

        mycursor.execute(sql)
        print("LOGIN_ID-----NAME-----AGE")

        for row in mycursor:
            print("{0:<10s} {1:<30s} {2:>10s}".format(str(row[0]), str(row[2]), str(row[3])))

        self.db.commit()

    class customer_search():
        def __init__(self, db):
            self.db = db
            print("")

        def search_customer_by(self):
            mycursor = self.db.cursor()

            how = input("Type any one Keyword to search customer :LoginId /  Name  ")
            if how == "LoginId":
                login_id = input("enter customer LoginId to search: ")
                sql = "SELECT * FROM customer WHERE custLoginId LIKE '%{}%'".format(login_id)
            elif how == "Name":
                name = input("Enter customer name to search: ")
                sql = "SELECT * FROM customer WHERE custName LIKE '%{}%'".format(name)

            else:
                print("type valid:")

            mycursor.execute(sql)
            # Consume and discard any unread results from previous queries
            rows = mycursor.fetchall()

            if rows:
                print("Search results for customer name '{}':".format(how))
                print("LOGIN_ID-----NAME-----AGE")
                for row in rows:
                    print("{:<10s} {:<30s} {:>10s}".format(str(row[0]), str(row[2]), str(row[3])))
            else:
                print("No customers found with the name '{}'.".format(how))

            self.db.commit()
            self.db.close()


class employee_service(getBTSDB):
    def __init__(self):
        # self.A = A
        # self.D = D
        print("")

    def view_employee(self):
        print("--------------------employee_service_List---------------------")
        mycursor = self.db.cursor()

        sql = "SELECT * FROM employee ORDER BY empLoginId DESC"

        mycursor.execute(sql)

        for row in mycursor:
            print("{0:<10s} {1:<30s} {2:>10s}".format(str(row[0]), str(row[2]), str(row[3])))

        self.db.commit()

    def addnew_employee(self):
        print(" ")
        mycursor = self.db.cursor()

        empLoginId = input("enter login-id:")
        empPassword = input("enter password:")
        empType = input("enter type(ADMIN / EXPERT):")
        empName = input("enter name:")
        empPhone = input("enter phone no:")
        empEmail = input("enter email:")
        # empStatus = input("enter phone no:")

        sql = "insert into employee(empLoginId, empPassword, empType, empName, empPhone, empEmail)value('%s', '%s', '%s', '%s', '%s', '%s')"

        value = (empLoginId, empPassword, empType, empName, empPhone, empEmail)

        # 1st way------
        # print("sql", sql % value)
        # mycursor.execute(sql % value)

        # 2nd way -------
        complete_sql = sql % value
        print(complete_sql)
        mycursor.execute(complete_sql)

        print("Signup successfully for ", empLoginId)
        mycursor.close()
        self.db.commit()

    def change_status(self):
        mycursor = self.db.cursor()

        sql = "UPDATE employee SET empStatus = '%s' WHERE empLoginId = '%s'"

        loginID = input("Enter LoginId of the employee for Status change: ")
        newstatus = input("Choose Status an type:\n For ACTIVATE \n For DEACTIVATE: ")


        value = (newstatus, loginID)

        mycursor.execute(sql % value)

        self.db.commit()

        if mycursor.rowcount == 1:
            if newstatus == "ACTIVE":
                print("ACTIVE")
            elif newstatus == "DEACTIVE":
                print("DEACTIVE")
            else:
                print("Wrong keyword.")
        else:
            print("Status change failed.")

        self.db.close()

    def change_password(self):
        mycursor = self.db.cursor()

        sql = "UPDATE employee SET empPassword = '%s' WHERE empLoginId = '%s'"

        loginID = input("Enter LoginId of the employee for password updation: ")
        newpass = input("Enter new password: ")
        value = (newpass, loginID)

        mycursor.execute(sql % value)

        self.db.commit()

        if mycursor.rowcount == 1:
            print("Old password deleted...")
            print("New password successfully updated :)")
        else:
            print("Password update failed.")
        # self.db.commit()
        self.db.close()

    class employee_search():
        def __init__(self, db):
            self.db = db
            print("")

        def search_employee_by(self):
            mycursor = self.db.cursor()

            how = input("Type any one Keyword to search employee :LoginId / Type / Name  ")
            if how == "LoginId":
                login_id = input("enter employee LoginId to search: ")
                sql = "SELECT * FROM employee WHERE empLoginId LIKE '%{}%'".format(login_id)
            elif how == "Name":
                name = input("Enter employee name to search: ")
                sql = "SELECT * FROM employee WHERE empName LIKE '%{}%'".format(name)
            elif how == "Type":
                etype = input("Enter employee type to search: ")
                sql = "SELECT * FROM employee WHERE empType LIKE '%{}%'".format(etype)

            else:
                print("type valid:")

            mycursor.execute(sql)
            # Consume and discard any unread results from previous queries
            rows = mycursor.fetchall()

            if rows:
                print("Search results for employee '{}':".format(how))
                print("LOGIN_ID-----TYPE-----NAME")
                for row in rows:
                    print("{:<10s} {:<30s} {:>10s}".format(str(row[0]), str(row[2]), str(row[3])))
            else:
                print("No customers found with the'{}'.".format(how))

            self.db.commit()
            self.db.close()


class bug_service(getBTSDB):
    print("")

    def __init__(self):
        print("")

    def view_bug(self):
        print("--------------------bug_service_List---------------------")
        mycursor = self.db.cursor()

        sql = "SELECT * FROM bug ORDER BY bugId DESC"

        mycursor.execute(sql)

        for row in mycursor:
            print("{0:<10s} {1:<30s} {2:>10s}".format(str(row[0]), str(row[2]), str(row[3])))

        self.db.commit()


    def assign_expert(self):
        mycursor = self.db.cursor()

        bug_id = input("Enter the bug ID: ")
        expert_id = input("Enter the expert ID: ")
        select_query = "SELECT empLoginId FROM employee WHERE empLoginId = %s"
        mycursor.execute(select_query, (expert_id,))
        result = mycursor.fetchone()

        if result:
            # Assign the expert to the bug in the bug table
            update_query = "UPDATE bug SET expertLoginId = %s WHERE bugId = %s"
            mycursor.execute(update_query, (expert_id, bug_id))
            self.db.commit()

            print("Expert assigned successfully to bug ID:", bug_id)
        else:
            print("Expert ID not found.")

        self.db.close()


# Create objects/instance
c = customer_service()
e = employee_service()
b = bug_service()

# Create an instance of the nested class using the db attribute from the outer instance
ci = c.customer_search(c.db)
ei = e.employee_search(e.db)


# Call the  function of method
# View all list
c.view_customer()
e.view_employee()
b.view_bug()

# e.addnew_employee()
# e.change_password()
# e.change_status()

b.assign_expert()

# ci.search_customer_by()  # Call the search_customer_by() method on the customer_search_instance
# ei.search_employee_by()