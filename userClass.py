# Create a singular connection to sqlite and db file to share with every other file
import sqlite3
con = sqlite3.connect("./project.sqlite")
cur = con.cursor()

# User Class 
class User:

    loggedIn = False
    id = None

    def createAccount(self):
        print("\nPlease enter an email, password, first name, and last name")

        # Loop until user creates account with email not in use
        while (True):
            email = input("Email: ")
            cur.execute("SELECT userID FROM customers WHERE email = ?", (email,))
            if cur.fetchone() == None:
                break
            else:
                print("Email already in use.")

        pwd = input("Passsord: ")
        fname = input("First Name: ")
        lname = input("Last Name: ")

        cur.execute("INSERT INTO customers(email, password, firstName, lastName) VALUES (?, ?, ?, ?)", (email, pwd, fname, lname,))
        con.commit()

        print("Account Created!")

    def deleteAccount(self):
        pwd = input("\nEnter password to confirm account deletion: ")
        cur.execute("SELECT password FROM customers WHERE userID = ?",(self.id,))
        if pwd == cur.fetchone()[0]:
            cur.execute("DELETE FROM customers WHERE userID = ?",(self.id,))
            cur.execute("DELETE FROM shipping WHERE userID = ?",(self.id,))
            cur.execute("DELETE FROM orders WHERE userID = ?",(self.id,))
            con.commit()
            self.id = None
            self.loggedIn = False
            print("Account has been deleted!")
        else:
            print("Incorrect password.")
    
    def logIn(self):
        print("\nEnter your email and password: ")
        email = input("Email: ")
        pwd = input("Password: ")

        # Sets the userID for the rest of the program to base queries off of
        cur.execute("SELECT userID FROM customers WHERE email=? AND password=?", (email, pwd,))
        self.id = cur.fetchone()

        if self.id == None:
            print("Email or password is incorrect.")
        else:
            # take it out of tuple so its easier to use in later queries
            self.id = self.id[0]
            print("Successfully logged in!")
            self.loggedIn = True

    def logOut(self):
        self.id = None
        self.loggedIn = False
        print("\nLogged out!")

    def changeName(self):
        print("\nEnter a new name: ")
        fname = input("First Name: ")
        lname = input("Last Name: ")

        cur.execute("UPDATE customers SET firstName=?, lastName=? WHERE userID=?",(fname, lname, self.id,))
        con.commit()
        print("Name has been updated!")

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

    def editShippingInfo(self):
        # Display current user shipping info if they have any
        cur.execute("SELECT address, city, state, zip FROM shipping WHERE userID = ?",(self.id,))
        shipList = cur.fetchone()
        if shipList == None:
            print("\nYou do not currently have any shipping info.")
        else:
            print("\nYour current shipping info:", shipList[0], ",", shipList[1], ",", shipList[2], shipList[3])

        # Prompt user to input new shipping info
        print("Please enter your new address, city, state, and zip in that order.")
        address = input("Address: ")
        city = input("City: ")
        state = input("State (e.g. 'MS'): ")
        zip = input("Zip code (e.g. 39759): ")
        
        # Insert or update users row in shipping info table
        cur.execute("SELECT userID FROM shipping WHERE userID = ?",(self.id,))
        if cur.fetchone() == None:
            cur.execute("INSERT INTO shipping(userID, address, city, state, zip) VALUES (?, ?, ?, ?, ?)",(self.id, address, city, state, zip,))
        else:
            cur.execute("UPDATE shipping SET address = ?, city = ?, state = ?, zip = ? WHERE userID = ?",(address, city, state, zip, self.id,))
        con.commit()
        
        print("Shipping info updated!")

    def editPaymentInfo(self):
        # Display current user payment info if they have any
        cur.execute("SELECT type, number, cvv FROM payment WHERE userID = ?",(self.id,))
        payList = cur.fetchone()
        if payList == None:
            print("\nYou do not currently have any paymentinfo.")
        else:
            print("\nYour current shipping info:", payList[0], payList[1], payList[2])

        # Prompt user to input new payment info
        print("Please enter your payment type, card number, and CVV")
        cardType = input("Card Type (Debit or Credit): ")
        cardNum = input("Card Number: ")
        cvv = input("CVV: ")

        # Insert or update users row in payment info table
        cur.execute("SELECT userID FROM payment WHERE userID = ?",(self.id,))
        if cur.fetchone() == None:
            cur.execute("INSERT INTO payment(userID, type, number, cvv) VALUES (?, ?, ?, ?)",(self.id, cardType, cardNum, cvv,))
        else:
            cur.execute("UPDATE payment SET type = ?, number = ?, cvv = ? WHERE userID = ?",(cardType, cardNum, cvv, self.id,))
        con.commit()
        
        print("Payment info updated!")
