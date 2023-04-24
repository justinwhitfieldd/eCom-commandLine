import sqlite3
from userClass import con


class ShoppingCart():
    def __init__(self, user_id):
        self.conn = con  # connect to db, what is db?
        self.c = self.conn.cursor()
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

    def removeItem(self, item_id, quantity):
        # check if the item exists in the cart
        self.c.execute(
            'SELECT quantity FROM cart WHERE item_id=? AND user_id=?', (item_id, self.user_id))
        result = self.c.fetchone()
        if result is not None:
            current_quantity = result[0]
            # update the quantity of the existing item
            if current_quantity > quantity:
                self.c.execute(
                    'UPDATE cart SET quantity=quantity-? WHERE item_id=? AND user_id=?', (quantity, item_id, self.user_id))
            else:
                self.c.execute(
                    'DELETE FROM cart WHERE item_id=? AND user_id=?', (item_id, self.user_id))
            self.conn.commit()

    def clearCart(self):
        self.c.execute('DELETE FROM cart WHERE user_id=?', (self.user_id,))
        self.conn.commit()

    def getItemCount(self):
        self.c.execute(
            'SELECT SUM(quantity) FROM cart WHERE user_id=?', (self.user_id,))
        result = self.c.fetchone()
        return result[0] if result[0] is not None else 0

    def getTotalPrice(self):
        self.c.execute(
            'SELECT SUM(items.price * cart.quantity) FROM cart INNER JOIN items ON cart.item_id=items.id WHERE cart.user_id=?', (self.user_id,))
        result = self.c.fetchone()
        return result[0] if result[0] is not None else 0

    def checkout(self):
        # add order to order history
        self.c.execute('INSERT INTO orders (user_id, total_price) VALUES (?, ?)',
                       (self.user_id, self.getTotalPrice()))
        order_id = self.c.lastrowid

        # remove items from cart and add them to order items
        self.c.execute(
            'SELECT item_id, quantity FROM cart WHERE user_id=?', (self.user_id,))
        items = self.c.fetchall()
        for item in items:
            self.c.execute('INSERT INTO order_items VALUES (?, ?, ?)',
                           (order_id, item[0], item[1]))
            self.c.execute(
                'UPDATE items SET stock=stock-? WHERE id=?', (item[1], item[0]))
        self.conn.commit()

    def displayCart(self):
        self.c.execute(
            'SELECT items.id, items.name, items.price, cart.quantity FROM cart INNER JOIN items ON cart.item_id=items.id WHERE cart.user_id=?', (self.user_id,))
        items = self.c.fetchall()
        print('Shopping Cart:')
        for item in items:
            print(f'{item[0]} - {item[1]} - ${item[2]} - Quantity: {item[3]}')
