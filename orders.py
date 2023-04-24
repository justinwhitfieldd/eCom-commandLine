import sqlite3
from typing import List, Dict
from datetime import datetime
from userClass import User, con, cur

'''
Canon: I recommend using the below to utilize the userID generated in user class upon login,
and instead of self.conn and the created cur you could just use con and cur that were imported if you want

class Order(User):
    def __init__(self):
        self.user_id = User.id
'''

class Order:
    def __init__(self, user_id: int, conn: con):
        self.user_id = user_id
        self.conn = conn
        self.order_id = None
        self.items = []
        self.total_price = 0.0
        self.timestamp = ""
        self.create_tables()

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
            cur.execute("INSERT INTO order_items (orderID, itemID, quantity, price) VALUES (?, ?, ?, ?)",
                        (self.order_id, item['item_id'], item['quantity'], item['price']))
            cur.execute("UPDATE items SET stock = stock - ? WHERE itemID = ?",
                        (item['quantity'], item['item_id']))

        self.conn.commit()

    def view_order(self) -> List[Dict]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM orders WHERE orderID = ?", (self.order_id,))
        order = cur.fetchone()
        if order:
            cur.execute("SELECT * FROM order_items WHERE orderID = ?", (self.order_id,))
            order_items = cur.fetchall()

            items = []
            for item in order_items:
                item_id, quantity, price = item[2], item[3], item[4]
                cur.execute("SELECT name FROM items WHERE itemID = ?", (item_id,))
                item_name = cur.fetchone()[0]
                items.append({"item_id": item_id, "name": item_name, "quantity": quantity, "price": price})

            return {"order_id": order[0], "total_price": order[2], "timestamp": order[3], "items": items}

        return None

    def create_tables(self) -> None:
        cur = self.conn.cursor()

        # Create orders table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                orderID INTEGER PRIMARY KEY AUTOINCREMENT,
                userID INTEGER NOT NULL,
                total_price REAL NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (userID) REFERENCES customers (userID)
            )
        """)

        # Create order_items table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                orderItemID INTEGER PRIMARY KEY AUTOINCREMENT,
                orderID INTEGER NOT NULL,
                itemID INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (orderID) REFERENCES orders (orderID),
                FOREIGN KEY (itemID) REFERENCES items (itemID)
            )
        """)

        self.conn.commit()