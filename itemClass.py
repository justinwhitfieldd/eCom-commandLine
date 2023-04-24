# connect to sqlite and db file
import sqlite3
from userClass import con, cur

# Item Class 
class Item:
    itemID = int
    itemName = str
    quantity = int
    price = float
    desc = str


    def __init__(self, id, name, q, p, str):
        self.itemID = id
        self.itemName = name
        self.quantity = q
        self.price = p
        self.desc = str

    def __str__(self):
        nl = '\n'
        return f"{nl}ID: {self.itemID}{nl}Name: {self.itemName}{nl}{self.desc}{nl}{nl}In Stock: {self.quantity}{nl}Price: ${self.itemID}"

    def setName(self, name):
        self.itemName = name
        cur.execute ("UPDATE Inventory SET itemName=? WHERE userID=?",(self.itemName, self.itemID,))
        con.commit()

    def setQuan(self, num):
        self.quantity = num
        cur.execute ("UPDATE Inventory SET quantity=? WHERE userID=?",(self.quantity, self.itemID,))
        con.commit()

    def incQuan(self, num):  
        self.quantity += num     
        cur.execute ("UPDATE Inventory SET quantity=? WHERE userID=?",(self.quantity, self.itemID,))
        con.commit()

    def decQuan(self, num):
        self.quantity -= num
        cur.execute ("UPDATE Inventory SET quantity=? WHERE userID=?",(self.quantity, self.itemID,))
        con.commit()

    def setPrice(self, p):
        self.price = p
        cur.execute ("UPDATE Inventory SET price=? WHERE userID=?",(self.price, self.itemID,))
        con.commit()

    def setDesc(self, str):
        self.desc = str
        cur.execute ("UPDATE Inventory SET desc=? WHERE userID=?",(self.desc, self.itemID,))
        con.commit()
    