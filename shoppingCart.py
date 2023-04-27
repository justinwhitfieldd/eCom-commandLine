import sqlite3
from userClass import con, cur


class ShoppingCart:
    def __init__(self, userID):
        self.userID = userID

    def addItem(self):
        itemID = int(input("What is the itemID? "))
        itemQuantity = int(input("How many? "))
        cur.execute('SELECT price FROM inventory WHERE itemID=?', (itemID,))
        itemPrice = cur.fetchone()[0]

        cur.execute(
            "SELECT itemName, quantity, price FROM inventory WHERE itemID=?", (itemID,))
        item = cur.fetchone()

        if not item:
            print("Item not found in inventory")
            return

        # Get or create the user's cart
        cur.execute(
            "SELECT cartID, total FROM cart WHERE userID=?", (self.userID,))
        cart = cur.fetchone()

        if not cart:
            cur.execute(
                "INSERT INTO cart (userID, total) VALUES (?, ?)", (self.userID, 0))
            con.commit()
            cartID = cur.lastrowid
            cartTotal = 0
        else:
            cartID, cartTotal = cart

        # Add item to items table
        itemTotalPrice = itemPrice * itemQuantity
        cur.execute("INSERT INTO items (itemID, cartID, itemQuantity, price, userID) VALUES (?, ?, ?, ?, ?)",
                    (itemID, cartID, itemQuantity, itemTotalPrice, self.userID))
        con.commit()

        # Update cart total
        cur.execute("UPDATE cart SET total=? WHERE cartID=?",
                    (cartTotal + itemTotalPrice, cartID))

        con.commit()

    def removeItem(self):
        itemID = int(input("Please input the itemID "))
        quantity = int(
            input("Enter the quantity of the item you want to remove: "))
        cur.execute('''
            UPDATE items
            SET itemQuantity = itemQuantity - ?
            WHERE itemID = ? AND cartID = (
                SELECT cartID FROM cart WHERE userID = ?
            )''', (quantity, itemID, self.userID))
        con.commit()

        cur.execute('''
            UPDATE items
            SET price = itemQuantity * (
                SELECT price FROM inventory WHERE itemID = ?
            )
            WHERE itemID = ? AND cartID = (
                SELECT cartID FROM cart WHERE userID = ?
            )''', (itemID, itemID, self.userID))
        con.commit()

        cur.execute('''
        UPDATE cart
        SET total = (
            SELECT SUM(price) FROM items
            WHERE cartID = (
                SELECT cartID FROM cart WHERE userID = ?
                )
            )
            WHERE userID = ?
        ''', (self.userID, self.userID))
        con.commit()

        print(
            f'{quantity} units of item with ID {itemID} have been removed from the cart.')
        cur.execute('''
            DELETE FROM items
            WHERE itemQuantity <= 0 AND cartID = (
                SELECT cartID FROM cart WHERE userID = ?
            )''', (self.userID,))
        con.commit()

    def checkout(self):
        # Check if cart is empty
        cur.execute("SELECT COUNT(*) FROM items WHERE userID=?",
                    (self.userID,))
        cart_size = cur.fetchone()[0]
        if cart_size == 0:
            print("Your cart is empty.")
            return

        # Get shipping information from user
        print("Please enter your shipping information:")
        address = input("Address: ")
        city = input("City: ")
        state = input("State: ")
        zip_code = input("Zip Code: ")
        cur.execute("INSERT INTO shipping(userID, address, city, state, zip) VALUES (?, ?, ?, ?, ?)",
                    (self.userID, address, city, state, zip_code))

        # Get payment information from user
        print("\nPlease enter your payment information:")
        payment_type = input(
            "Payment Type (e.g. Credit Card, Debit Card, PayPal): ")
        payment_number = input("Card Number: ")
        payment_cvv = input("CVV: ")
        cur.execute("INSERT INTO payment(userID, type, number, cvv) VALUES (?, ?, ?, ?)",
                    (self.userID, payment_type, payment_number, payment_cvv))

        # Update inventory and cart tables
        cur.execute(
            "SELECT itemID, itemQuantity FROM items WHERE userID=?", (self.userID,))
        items = cur.fetchall()
        for item in items:
            item_id, item_quantity = item
            cur.execute(
                "UPDATE inventory SET quantity=quantity-? WHERE itemID=?", (item_quantity, item_id))
            cur.execute("DELETE FROM items WHERE itemID=? AND userID=?",
                        (item_id, self.userID))
        cur.execute("UPDATE cart SET total=0 WHERE userID=?", (self.userID,))

        # Commit changes and print success message
        con.commit()
        print("Thank you for your purchase!")

    def displayCart(self):
        cur.execute('''
            SELECT items.itemID, inventory.itemName, inventory.price, items.itemQuantity, 
                   items.itemQuantity * inventory.price as itemTotal
            FROM items
            INNER JOIN inventory ON items.itemID = inventory.itemID
            WHERE items.cartID = (
                SELECT cartID FROM cart WHERE userID = ?
            )''', (self.userID,))
        items = cur.fetchall()
        print('\nShopping Cart:\n')
        total = 0
        for item in items:
            print(
                f'({item[0]}) {item[1]} - ${item[2]}/each - Quantity: {item[3]} - Item Total: ${item[4]}')
            total += item[4]
        print(f'------------------------')
        print(f'Total Price: ${total}')

        con.commit()
