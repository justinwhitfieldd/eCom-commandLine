# connection to sqlite is currently in userClass.py
# I wanted to do it in main but importing from main into other
# files causes an import loop where the files depend on each other

from userClass import User, con, cur

# Creating database tables if they do not exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS customers(
        userID integer PRIMARY KEY, 
        email text NOT NULL, 
        password text NOT NULL, 
        firstName text NOT NULL, 
        lastName text NOT NULL)
        ''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS shipping(
        userID integer, 
        address text NOT NULL, 
        city text NOT NULL, 
        state text NOT NULL, 
        zip integer NOT NULL, 
        FOREIGN KEY(userID) REFERENCES customers(userID))
        ''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS payment(
        userID integer, 
        type text NOT NULL,
        number integer NOT NULL,
        cvv integer NOT NULL,
        FOREIGN KEY(userID) REFERENCES customers(userID))
        ''')



exiting = False

# Menus
def startMenu():
    while (1):
        # Menu
        print("\nStart Menu: ")
        print("1) Login")
        print("2) Create Account")
        print("3) Exit")
        # User input
        try:
            sel = int(input("Enter your option: "))
        except ValueError:
            break
        # Selections
        if sel == 1:
            user.logIn()
            if (user.loggedIn):
                break
        elif sel == 2:
            user.createAccount()
        elif sel == 3:
            global exiting
            exiting = True
            break
        else:
            print("Invalid option")

def userSettings():
    while (user.loggedIn):
        # Menu
        print("\nSettings: ")
        print("1) Change name")
        print("2) Reset password")
        print("3) Edit Shipping Info")
        print("4) Edit Payment Info")
        print("5) Delete Account")
        print("6) View Order History")
        print("7) Back")
        # User Input
        try:
            sel = int(input("Enter your option: "))
        except ValueError:
            break
        # Selections
        if sel == 1:
            user.changeName()
        elif sel == 2:
            user.resetPassword()
        elif sel == 3:
            user.editShippingInfo()
        elif sel == 4:
            user.editPaymentInfo()
        elif sel == 5:
            user.deleteAccount()
        # elif sel == 6:
        #     blahblah
        elif sel == 7:
            break      
        else:
            print("Invalid option")

def mainMenu():
    while (user.loggedIn):
        # Menu
        print("\nMain Menu:")
        print("1) View Item Catalog")
        print("2) View Cart")
        print("3) Edit Settings")
        print("4) Log Out")
        # User Input
        try:
            sel = int(input("Enter your option: "))
        except ValueError:
            break
        # Selections
        # if sel == 1:
        #     blahblah
        # elif sel == 2:
        #     blahblah
        # change below to elif after setting selection 1
        if sel == 3:
            userSettings()
        elif sel == 4:
            user.logOut()
        else:
            print("Invalid option")

user = User()

# Main program loop until user exits from startmenu
while(1):
    if (exiting):
        break
    else:
        startMenu()

    # Main menu only loops while loggedIn = true
    mainMenu()


cur.close()
con.close()