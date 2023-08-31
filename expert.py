import mysql.connector

class getBTSDB:
    def __init__(self):
        self.db = mysql.connector.connect(host="localhost", database="bts", user="root", password="")

class Expert_Module(getBTSDB):
    def __init__(self):
        super().__init__()
        print("")

    def View_assign_bug(self):
        print("")
        mycursor = self.db.cursor()

        expert_id = input("Enter your expert ID: ")
        select_query = "SELECT empLoginId FROM employee WHERE empLoginId = %s"
        mycursor.execute(select_query, [expert_id])
        result = mycursor.fetchone()

        if result:
            bugs_query = "SELECT bugId, custLoginID, productName, bugDesc FROM bug WHERE expertLoginId = %s"
            mycursor.execute(bugs_query, [expert_id])
            bugs = mycursor.fetchall()

            if bugs:
                print("Existing bugs:")
                for bug in bugs:
                    print("Bug ID:", bug[0])
                    print("customer ID:", bug[1])
                    print("Product Name:", bug[2])
                    print("Bug Description:", bug[3])
                    print()
            else:
                print("No bugs found for the expert.")
        else:
            print("Expert ID not found.")

        self.db.close()

    def Search_filter_Bug(self):
        print("")

        mycursor = self.db.cursor()

        expert_id = input("Enter your expert ID: ")
        bug_status = input("Press 'N' for New bugs or 'S' for Solved bugs: ")

        select_query = "SELECT empLoginId FROM employee WHERE empLoginId = %s"
        mycursor.execute(select_query, (expert_id,))
        result = mycursor.fetchone()

        if result:
            if bug_status.lower() == "n":
                search_bug_status = "New Bug"
            elif bug_status.lower() == "s":
                search_bug_status = "Solved Bug"
            else:
                print("Invalid choice. Please try again.")
                return

            bugs_query = "SELECT bugId, custLoginID, productName, bugDesc FROM bug WHERE expertLoginId = %s AND bugStatus = %s"
            values = (expert_id, search_bug_status)
            mycursor.execute(bugs_query, values)
            bugs = mycursor.fetchall()

            if bugs:
                print("Existing bugs:")
                for bug in bugs:
                    print("Bug ID:", bug[0])
                    print("customer ID:", bug[1])
                    print("Product Name:", bug[2])
                    print("Bug Description:", bug[3])
                    print()
            else:
                print("No bugs found for the customer.")
        else:
            print("expert ID not found.")

        self.db.close()

    def Solve_the_Bug(self):
        print("")
        mycursor = self.db.cursor()

        expert_id = input("Enter your expert ID: ")
        bug_status = input("Press 'N' for New bugs: ")

        select_query = "SELECT empLoginId FROM employee WHERE empLoginId = %s"
        mycursor.execute(select_query, (expert_id,))
        result = mycursor.fetchone()

        if result:
            if bug_status.lower() == "n":
                search_bug_status = "New Bug"
            else:
                print("Invalid choice. Please try again.")
                return

            bugs_query = "SELECT bugId, custLoginID, productName, bugDesc FROM bug WHERE expertLoginId = %s AND bugStatus = %s"
            values = (expert_id, search_bug_status)
            mycursor.execute(bugs_query, values)
            bugs = mycursor.fetchall()

            if bugs:
                print("Existing bugs:")
                for bug in bugs:
                    print("Bug ID:", bug[0])
                    print("Customer ID:", bug[1])
                    print("Product Name:", bug[2])
                    print("Bug Description:", bug[3])
                    print()

                    self.bug_solve_date(bug)  # Pass the bug row as an argument
            else:
                print("No bugs found for the customer.")
        else:
            print("Expert ID not found.")

        mycursor.close()
        self.db.close()

    def bug_solve_date(self, bug):
        mycursor = self.db.cursor()

        bug_solution = input("Write solution for the bug: ")
        bugId = bug[0]  # Fetch bug ID from the bug row

        sql = "UPDATE bug SET solution = %s WHERE bugId = %s"
        values = (bug_solution, bugId)

        mycursor.execute(sql, values)
        self.db.commit()

        if mycursor.rowcount == 1:
            print("Successfully updated.")
        else:
            print("Update failed.")

        mycursor.close()


em = Expert_Module()

# em.View_assign_bug()
# em.Search_filter_Bug()

em.Solve_the_Bug()
