import sqlite3


class ShoppingCart:
    def __init__(self, user_id):
        self.conn = sqlite3.connect('store.db')  # connect to db, what is db?
        self.c = self.conn.cursor()
<<<<<<< Updated upstream
        self.user_id = user_id

    def addItem(self, item_id, quantity):
        # check if the item already exists in the cart
        self.c.execute(
            'SELECT quantity FROM cart WHERE item_id=? AND user_id=?', (item_id, self.user_id))
        result = self.c.fetchone()
        if result is not None:
            # update the quantity of the existing item
            self.c.execute('UPDATE cart SET quantity=quantity+? WHERE item_id=? AND user_id=?',
                           (quantity, item_id, self.user_id))
        else:
            # insert the new item into the cart
            self.c.execute('INSERT INTO cart VALUES (?, ?, ?)',
                           (item_id, quantity, self.user_id))
        self.conn.commit()
=======
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

        itemName, inventoryQuantity, itemPrice = item

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

        # Update cart total
        cur.execute("UPDATE cart SET total=? WHERE cartID=?",
                    (cartTotal + itemTotalPrice, cartID))

        con.commit()
>>>>>>> Stashed changes

    def removeItem(self, item_id, quantity):
        # check if the item exists in the cart
        cur.execute(
            'SELECT quantity FROM cart WHERE item_id=? AND user_id=?', (item_id, self.user_id))
        result = self.c.fetchone()
        if result is not None:
            current_quantity = result[0]
            # update the quantity of the existing item
            if current_quantity > quantity:
                cur.execute(
                    'UPDATE cart SET quantity=quantity-? WHERE item_id=? AND user_id=?', (quantity, item_id, self.user_id))
            else:
                cur.execute(
                    'DELETE FROM cart WHERE item_id=? AND user_id=?', (item_id, self.user_id))
            con.commit()

    def clearCart(self):
        cur.execute('DELETE FROM cart WHERE user_id=?', (self.user_id,))
        con.commit()

    def getItemCount(self):
        cur.execute(
            'SELECT SUM(quantity) FROM cart WHERE user_id=?', (self.user_id,))
        result = self.c.fetchone()
        return result[0] if result[0] is not None else 0

    def getTotalPrice(self):
        cur.execute(
            'SELECT SUM(items.price * cart.quantity) FROM cart INNER JOIN items ON cart.item_id=items.id WHERE cart.user_id=?', (self.user_id,))
        result = self.c.fetchone()
        return result[0] if result[0] is not None else 0

    def checkout(self):
        # add order to order history
        cur.execute('INSERT INTO orders (user_id, total_price) VALUES (?, ?)',
                    (self.user_id, self.getTotalPrice()))
        order_id = self.c.lastrowid

        # remove items from cart and add them to order items
        cur.execute(
            'SELECT item_id, quantity FROM cart WHERE user_id=?', (self.user_id,))
        items = self.c.fetchall()
        for item in items:
            cur.execute('INSERT INTO order_items VALUES (?, ?, ?)',
                        (order_id, item[0], item[1]))
            cur.execute(
                'UPDATE items SET stock=stock-? WHERE id=?', (item[1], item[0]))
        con.commit()

    def displayCart(self):
        cur.execute(
            'SELECT items.id, items.name, items.price, cart.quantity FROM cart INNER JOIN items ON cart.item_id=items.id WHERE cart.user_id=?', (self.user_id,))
        items = self.c.fetchall()
        print('Shopping Cart:')
        for item in items:
            print(f'{item[0]} - {item[1]} - ${item[2]} - Quantity: {item[3]}')
