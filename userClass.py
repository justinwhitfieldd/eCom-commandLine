# connect to sqlite and db file
import sqlite3
con = sqlite3.connect("./project.sqlite")
cur = con.cursor()

# User Class 
class User:

    loggedIn = False

    def createAccount(self):
        print("\nPlease enter an email, password, first name, and last name")

        email = input("Email: ")
        pwd = input("Password: ")
        fname = input("First Name: ")
        lname = input("Last Name: ")

        cur.execute("INSERT INTO customers(email, password, firstName, lastName) VALUES (?, ?, ?, ?)", (email, pwd, fname, lname,))
        con.commit()

        print("Account Created!\n")

    # def deleteAccount(self):
    #     blahblah
    
    def logIn(self):
        print("\nEnter your email and password: ")
        email = input("Email: ")
        pwd = input("Password: ")

        cur.execute("SELECT userID FROM customers WHERE email=? AND password=?", (email, pwd,))
        self.id = cur.fetchone()

        if self.id == None:
            print("\nEmail or password is incorrect.")
        else:
            # take it out of tuple so its easier to use in later queries
            self.id = self.id[0]
            print("\nSuccessfully logged in!")
            self.loggedIn = True

    def logOut(self):
        self.id = None
        self.loggedIn = False
        print("\nLogged out!")

    def changeName(self):
        print("\nEnter a new name: ")
        fname = input("First Name: ")
        lname = input("Last Name: ")

        cur.execute ("UPDATE customers SET firstName=?, lastName=? WHERE userID=?",(fname, lname, self.id,))
        con.commit()
        print("Name has been updated!\n")

    def resetPassword(self):
        cur.execute("SELECT password FROM customers WHERE userID=?",(self.id,))
        oldPwd = cur.fetchall()[0][0]
        if input("\nEnter old password: ") == oldPwd:
            newPwd = input("Enter new password: ")
            cur.execute("UPDATE customers SET password=? WHERE userID=?",(newPwd, self.id,))
            con.commit()
            print("Password successfully changed!")
        else:
            print("Incorret password.")
