import mysql.connector

class GetBTSDB:
    def __init__(self):
        self.db = mysql.connector.connect(host="localhost", database="iitk_db", user="root", password="password")

class Customer_Module(GetBTSDB):
    def __init__(self):
        super().__init__()
        self.custLoginId = ""
        self.custPassword = ""
        self.custName = ""
        self.custAge = 0
        self.custPhone = ""
        self.custEmail = ""

    def Login_customer(self):
        self.custLoginId = input("Enter custLoginId: ")
        custpassword = input("Enter custPassword: ")

        mycursor = self.db.cursor()

        sql = "SELECT * FROM customer WHERE custLoginId = %s"
        value = (self.custLoginId,)

        mycursor.execute(sql, value)

        row = mycursor.fetchone()

        if row is not None:
            dbPass = row[1]
            if custpassword == dbPass:
                print("Login authentication success")
                print("Welcome", self.custLoginId)
            else:
                print("Login authentication failed")
        else:
            print("Invalid id. Retry...")

        mycursor.close()

    def Update_customer(self):
        what_update = input("Press key for update: custPassword (p/P), custName (n/N), custAge (a/A), custPhone (ph/PH), custEmail (e/E): ")

        mycursor = self.db.cursor()

        if what_update.lower() == 'p':
            update = input("Enter new password: ")
            sql = "UPDATE customer SET custPassword = %s WHERE custLoginId = %s"
        elif what_update.lower() == 'n':
            update = input("Enter new name: ")
            sql = "UPDATE customer SET custName = %s WHERE custLoginId = %s"
        elif what_update.lower() == 'a':
            update = int(input("Enter new age: "))
            sql = "UPDATE customer SET custAge = %s WHERE custLoginId = %s"
        elif what_update.lower() == 'ph':
            update = input("Enter new phone: ")
            sql = "UPDATE customer SET custPhone = %s WHERE custLoginId = %s"
        elif what_update.lower() == 'e':
            update = input("Enter new email: ")
            sql = "UPDATE customer SET custEmail = %s WHERE custLoginId = %s"
        else:
            print("Press correct key...")
            return

        value = (update, self.custLoginId)
        mycursor.execute(sql, value)

        self.db.commit()

        if mycursor.rowcount == 1:
            print("Old record deleted...")
            print("New", what_update, "successfully updated")
        else:
            print("Update failed.")

        mycursor.close()

    def Post_New_bug(self):
        print("")
        mycursor = self.db.cursor()

        product_name = input("Enter your product name (e.g., laptop, phone): ")
        bug_Description = input("Enter the bug description: ")

        select_query = "SELECT custLoginId FROM customer WHERE custLoginId = %s"
        mycursor.execute(select_query, (self.custLoginId,))
        result = mycursor.fetchone()

        if result:
            update_insert = input("Choose 'U' for update or 'I' for insert: ")

            if update_insert.lower() == "u":
                # Retrieve the customer's bugs from the bug table
                bugs_query = "SELECT bugId, productName, bugDesc FROM bug WHERE custLoginId = %s"
                mycursor.execute(bugs_query, (self.custLoginId,))
                bugs = mycursor.fetchall()

                if bugs:
                    print("Existing bugs:")
                    for bug in bugs:
                        print("Bug ID:", bug[0])
                        print("Product Name:", bug[1])
                        print("Bug Description:", bug[2])
                        print()

                    bug_id = int(input("Enter the Bug ID of the bug you want to update: "))
                    bug_exists = False

                    for bug in bugs:
                        if bug[0] == bug_id:
                            bug_exists = True
                            break

                    if bug_exists:
                        new_product_name= product_name
                        new_description = bug_Description
                        update_query = "UPDATE bug SET productName = %s, bugDesc = %s WHERE bugId = %s"
                        values = (new_product_name, new_description, bug_id)
                        mycursor.execute(update_query, values)
                        self.db.commit()
                        print("Bug description updated successfully.")
                    else:
                        print("Bug ID not found.")
                else:
                    print("No bugs found for the customer.")
            elif update_insert.lower() == "i":
                insert_query = "INSERT INTO bug (productName, custLoginId, bugDesc) VALUES (%s, %s, %s)"
                values = (product_name, self.custLoginId, bug_Description)
                mycursor.execute(insert_query, values)
                self.db.commit()
                print("Bug posted successfully by customer ID:", self.custLoginId)
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Customer ID not found.")

        mycursor.close()

    def View_all_bug(self):
        print("")
        mycursor = self.db.cursor()

        # customer_id = input("Enter your customer ID: ")

        select_query = "SELECT custLoginId FROM customer WHERE custLoginId = %s"
        mycursor.execute(select_query, (self.custLoginId,))
        result = mycursor.fetchone()

        if result:
            print("searching...")
            bugs_query = "SELECT bugId, productName, bugDesc FROM bug WHERE custLoginId = %s"
            mycursor.execute(bugs_query, (self.custLoginId,))
            bugs = mycursor.fetchall()

            if bugs:
                print("Existing bugs:")
                for bug in bugs:
                    print("Bug ID:", bug[0])
                    print("Product Name:", bug[1])
                    print("Bug Description:", bug[2])
                    print()

            else:
               print("No bugs found for the customer.")

            self.db.close()

    def Search_Bug(self):
        print("")

        mycursor = self.db.cursor()

        # customer_id = input("Enter your customer ID: ")
        bug_status = input("Press 'N' for New bugs or 'S' for Solved bugs: ")

        select_query = "SELECT custLoginId FROM customer WHERE custLoginId = %s"
        mycursor.execute(select_query, (self.custLoginId,))
        result = mycursor.fetchone()

        if result:
            if bug_status.lower() == "n":
                search_bug_status = "New Bug"
            elif bug_status.lower() == "s":
                search_bug_status = "Solved Bug"
            else:
                print("Invalid choice. Please try again.")
                return

            bugs_query = "SELECT bugId, productName, bugDesc FROM bug WHERE custLoginId = %s AND bugStatus = %s"
            values = (self.custLoginId, search_bug_status)
            mycursor.execute(bugs_query, values)
            bugs = mycursor.fetchall()

            if bugs:
                print("Existing bugs:")
                for bug in bugs:
                    print("Bug ID:", bug[0])
                    print("Product Name:", bug[1])
                    print("Bug Description:", bug[2])
                    print()
            else:
                print("No bugs found for the customer.")
        else:
            print("Customer ID not found.")

        self.db.close()


    def View_Bug_solution(self):
        print("")

        mycursor = self.db.cursor()

        # customer_id = input("Enter your customer ID: ")
        bug_status = input("Press 'S' for Solved bugs: ")

        select_query = "SELECT custLoginId FROM customer WHERE custLoginId = %s"
        mycursor.execute(select_query, (self.custLoginId,))
        result = mycursor.fetchone()

        if result:
            if bug_status.lower() == "s":
                search_bug_status = "Solved Bug"

                bugs_query = "SELECT bugId, productName, bugDesc, solution FROM bug WHERE custLoginId = %s AND bugStatus = %s"
                values = (self.custLoginId, search_bug_status)
                mycursor.execute(bugs_query, values)
                bugs = mycursor.fetchall()

                if bugs:
                    print("Existing bugs:")
                    for bug in bugs:
                        print("Bug ID:", bug[0])
                        print("Product Name:", bug[1])
                        print("Bug Description:", bug[2])
                        print("solution:", bug[3])
                        print()
                else:
                    print("No bugs found for the customer.")
            else:
                print("Customer ID not found.")

        self.db.close()


cm = Customer_Module()

cm.Login_customer()

# cm.Update_customer()
what_user_want = input("what do you want here: \n Nothing (none)\n Update (u/U) \n post new bug (p/P) \n view all bug(v/V) \n view bug solution(vs/VS) ")
if what_user_want.lower() == "u":
    cm.Update_customer()
elif what_user_want.lower() == "p":
    cm.Post_New_bug()
elif what_user_want.lower() == "v":
    cm.View_all_bug()
elif what_user_want.lower() == "s":
    cm.Search_Bug()
elif what_user_want.lower() == "vs":
    cm.View_Bug_solution()
else:
    print(":)")