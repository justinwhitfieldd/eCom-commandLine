import sqlite3
from userClass import con, cur
from orders import Order


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
        # Check if the item already exists in the user's cart
        cur.execute("SELECT itemQuantity, price FROM items WHERE itemID=? AND userID=?", (itemID, self.userID))
        existing_item = cur.fetchone()

        itemTotalPrice = itemPrice * itemQuantity

        if existing_item:
            # Update the existing item's quantity and price
            new_quantity = existing_item[0] + itemQuantity
            new_price = existing_item[1] + itemTotalPrice
            cur.execute("UPDATE items SET itemQuantity=?, price=? WHERE itemID=? AND userID=?",
                        (new_quantity, new_price, itemID, self.userID))
        else:
            # Add a new row for the item in the items table
            cur.execute("INSERT INTO items (itemID, cartID, itemQuantity, price, userID) VALUES (?, ?, ?, ?, ?)",
                        (itemID, cartID, itemQuantity, itemTotalPrice, self.userID))

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

        # Check if user already has shipping information
        cur.execute("SELECT COUNT(*) FROM shipping WHERE userID=?",
                    (self.userID,))
        shipping_count = cur.fetchone()[0]
        if shipping_count == 0:
            print("Please enter your shipping information:")
            address = input("Address: ")
            city = input("City: ")
            state = input("State: ")
            zip_code = input("Zip Code: ")
            cur.execute("INSERT INTO shipping(userID, address, city, state, zip) VALUES (?, ?, ?, ?, ?)",
                        (self.userID, address, city, state, zip_code))

        # Check if user already has payment information
        cur.execute("SELECT COUNT(*) FROM payment WHERE userID=?",
                    (self.userID,))
        payment_count = cur.fetchone()[0]
        if payment_count == 0:
            print("\nPlease enter your payment information:")
            payment_type = input(
                "Payment Type (e.g. Credit Card, Debit Card, PayPal): ")
            payment_number = input("Card Number: ")
            payment_cvv = input("CVV: ")
            cur.execute("INSERT INTO payment(userID, type, number, cvv) VALUES (?, ?, ?, ?)",
                        (self.userID, payment_type, payment_number, payment_cvv))

        # Create Order instance and populate it with cart items
        cur.execute(
            "SELECT itemID, itemQuantity FROM items WHERE userID=?", (self.userID,))
        items = cur.fetchall()
        order_items = []
        for item in items:
            item_id, item_quantity = item
            cur.execute(
                "SELECT itemName, price FROM inventory WHERE itemID=?", (item_id,))
            item_name, item_price = cur.fetchone()
            order_items.append({'item_id': item_id, 'itemName': item_name,
                               'quantity': item_quantity, 'price': item_price})

        order = Order(self.userID)
        order_total_price = sum(
            [item['price'] * item['quantity'] for item in order_items])
        order.add_order(order_items, order_total_price)

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
        print("\n*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print("|         SHOPPING CART         |")
        print("|       Holding your nuts       |")
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")

        total = 0
        for item in items:
            print(
                f'Item ID:{item[0]}\nItem Name: {item[1]}\nUnit Price: ${item[2]}/each\nQuantity: {item[3]} \n')
            total += item[4]
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print(f'Total Price: $','%.2f' % total)

        con.commit()
