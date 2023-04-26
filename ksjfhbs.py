import sqlite3
from userClass import con, cur

'''
Canon: instead of self.conn and self.c you could just use con and cur that were imported if you want
'''


class ShoppingCart:
    itemQuantity = int

    def __init__(self, itemQuantity):
        self.itemQuantity = itemQuantity

    def addItem(self):
        # check if the item already exists in the cart
        itemID = input("Enter item ID: ")
        itemQuantity = int(input("Enter quantity: "))
        cur.execute(
            'SELECT itemQuantity FROM items WHERE itemID=? AND userID=?', (itemID, self.userID))
        result = cur.fetchone()
        if result is not None:
            # update the itemQuantity of the existing item
            cur.execute('UPDATE cart SET itemQuantity=itemQuantity+? WHERE itemID=? AND userID=?',
                        (itemQuantity, itemID))
        else:
            # insert the new item into the cart
            cur.execute('INSERT INTO items VALUES (?, ?, ?)',
                        (itemID, itemQuantity))
        con.commit()

    def removeItem(self, itemID, itemQuantity):
        # check if the item exists in the cart
        cur.execute(
            'SELECT itemQuantity FROM cart WHERE itemID=? AND userID=?', (itemID, self.userID))
        result = cur.fetchone()
        if result is not None:
            current_itemQuantity = result[0]
            # update the itemQuantity of the existing item
            if current_itemQuantity > itemQuantity:
                cur.execute(
                    'UPDATE cart SET itemQuantity=itemQuantity-? WHERE itemID=? AND userID=?', (itemQuantity, itemID, self.userID))
            else:
                cur.execute(
                    'DELETE FROM cart WHERE itemID=? AND userID=?', (itemID, self.userID))
            con.commit()

    def clearCart(self):
        cur.execute('DELETE FROM cart WHERE userID=?', (self.userID,))
        con.commit()

    def getItemCount(self):
        cur.execute(
            'SELECT SUM(itemQuantity) FROM cart WHERE userID=?', (self.userID,))
        result = cur.fetchone()
        return result[0] if result[0] is not None else 0

    def getTotalPrice(self):
        cur.execute(
            'SELECT SUM(items.price * cart.itemQuantity) FROM cart INNER JOIN items ON cart.itemID=items.id WHERE cart.userID=?', (self.userID,))
        result = cur.fetchone()
        return result[0] if result[0] is not None else 0

    def checkout(self):
        # add order to order history
        cur.execute('INSERT INTO orders (userID, total_price) VALUES (?, ?)',
                    (self.userID, self.getTotalPrice()))
        order_id = self.c.lastrowid

        # remove items from cart and add them to order items
        cur.execute(
            'SELECT itemID, itemQuantity FROM cart WHERE userID=?', (self.userID,))
        items = self.c.fetchall()
        for item in items:
            cur.execute('INSERT INTO order_items VALUES (?, ?, ?)',
                        (order_id, item[0], item[1]))
            cur.execute(
                'UPDATE items SET stock=stock-? WHERE id=?', (item[1], item[0]))
        con.commit()

    def displayCart(self):
        cur.execute(
            'SELECT items.id, items.name, items.price, cart.itemQuantity FROM cart INNER JOIN items ON cart.itemID=items.id WHERE cart.userID=?', (self.userID,))
        items = self.c.fetchall()
        print('Shopping Cart:')
        for item in items:
            print(
                f'{item[0]} - {item[1]} - ${item[2]} - itemQuantity: {item[3]}')
