from userClass import User, con, cur
from itemClass import Item
from orders import Order
from shoppingCart import ShoppingCart

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
cur.execute('''
    CREATE TABLE IF NOT EXISTS inventory(
	    itemID integer PRIMARY KEY,
	    itemName text NOT NULL,
	    quantity integer NOT NULL,
	    price real NOT NULL,
	    desc text NOT NULL)
        ''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS cart(
	    cartID integer PRIMARY KEY,
	    userID integer NOT NULL,
	    total integer,
        FOREIGN KEY(userID) REFERENCES customers(userID))
        ''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS items(
	    itemID integer,
        cartID integer,
	    itemQuantity integer,
	    price integer,
        userID integer,
        FOREIGN KEY(userID) REFERENCES customers(userID),
        FOREIGN KEY(cartID) REFERENCES cart(cartID),
        FOREIGN KEY(itemID) REFERENCES inventory(itemID))
        ''')

# create items if they do not already exist
# Sample nuts
sample_items = [
    {"id": 1, "name": "Almonds", "quantity": 100, "price": 5.99,
        "desc": "Delicious and healthy almonds."},
    {"id": 2, "name": "Cashews", "quantity": 80,
        "price": 6.99, "desc": "Crunchy and tasty cashews."},
    {"id": 3, "name": "Pistachios", "quantity": 120, "price": 7.99,
        "desc": "Nutritious and flavorful pistachios."},
    {"id": 4, "name": "Walnuts", "quantity": 60, "price": 8.99,
        "desc": "Fresh and high-quality walnuts."},
]

for item_data in sample_items:
    cur.execute("SELECT * FROM Inventory WHERE itemID=?", (item_data["id"],))
    item_exists = cur.fetchone()

    if not item_exists:
        item = Item(item_data["id"], item_data["name"],
                    item_data["quantity"], item_data["price"], item_data["desc"])
        cur.execute("INSERT INTO Inventory (itemID, itemName, quantity, price, desc) VALUES (?, ?, ?, ?, ?)",
                    (item.itemID, item.itemName, item.quantity, item.price, item.desc))
        con.commit()
        print(f"Sample item '{item.itemName}' created.")

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
                # cart = ShoppingCart(user.id)
                # order = Order(user.id)
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
        cart = ShoppingCart(user.id)
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
        if sel == 1:
            itemMenu()
        elif sel == 2:
            cart.displayCart()
            print("\nCart Actions: ")
            print("1) Remove items")
            print("2) Checkout")
            print("3) Exit cart")
            try:
                cartSel = int(input("Enter your option: "))
            except ValueError:
                break
            if cartSel == 1:
                cart.removeItem()
                continue
            elif cartSel == 2:
                cart.checkout()
                continue
            elif cartSel == 3:
                continue
            else:
                print("Invalid response, please try again. ")
        elif sel == 3:
            userSettings()
        elif sel == 4:
            user.logOut()
        else:
            print("Invalid option")


def itemMenu():
    for i in inventory:
        print(i)

    while (1):
        # Menu
        cart = ShoppingCart(user.id)
        print("\n---------------------")
        print("Item Menu:")
        print("1) Add Item to Cart")
        print("2) Go Back")
        # User Input
        try:
            sel = int(input("Enter your option: "))
        except ValueError:
            continue
        if sel == 1:
            cart.addItem()
            continue
        if sel == 2:
            break
        else:
            print("Invalid option")

# def addToCart():


user = User()
inventory = []

data = cur.execute('''SELECT * From inventory''')
# data = data.fetchall
for i in data:
    inventory.append(Item(i[0], i[1], i[2], i[3], i[4]))

# Main program loop until user exits from startmenu
while (1):
    if (exiting):
        break
    else:
        startMenu()

    # Main menu only loops while loggedIn = true
    mainMenu()


cur.close()
con.close()
