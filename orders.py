import sqlite3
from typing import List, Dict
from datetime import datetime
from userClass import con, cur

'''
Canon: instead of self.conn and the created cur you could just use con and cur that were imported if you want
'''

class Order:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.conn = con
        self.order_id = None
        self.items = []
        self.total_price = 0.0
        self.timestamp = ""

    def add_order(self, items: List[Dict], total_price: float) -> None:
        self.items = items
        self.total_price = total_price
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur = self.conn.cursor()
        cur.execute("INSERT INTO orders (userID, total_price, timestamp) VALUES (?, ?, ?)",
                    (self.user_id, self.total_price, self.timestamp))
        self.order_id = cur.lastrowid
        self.conn.commit()

        for item in items:
            cur.execute("INSERT INTO order_items (orderID, itemName, itemID, quantity, price) VALUES (?, ?, ?, ?, ?)",
                        (self.order_id, item['itemName'], item['item_id'] ,item['quantity'], item['price']))
            

        self.conn.commit()

    def view_order(self) -> List[Dict]:
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print("|         ORDER HISTORY         |")
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM orders WHERE userID = ?", (self.user_id,))
        orders = cur.fetchall()

        if(orders):
            print("|      Number of Orders: ",len(orders),"    |")
            print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            for order in orders:

                cur.execute("SELECT * FROM order_items WHERE orderID = ?", (order[0],))
                order_items = cur.fetchall()

                # Print the order details
                print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
                print(f"Order ID: {order[0]}")
                print(f"Total Price: ${order[2]}")
                print(f"Timestamp: {order[3]}")
                print("\nItems: ")

                for item in order_items:
                    print(f"Name: {item[1]}")
                    print(f"Quantity: {item[4]}")
                    print(f"Price: {item[5]}")
                print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")

        else:
            print("No order found.")
        return None
