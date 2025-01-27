import mysql.connector
import json
from flask import make_response
from datetime import datetime, timedelta
import jwt
from config.config import dbconfig

class User:

   def __init__(self):
      # Initialize database connection
      try:
         self.con = mysql.connector.connect(
         host=dbconfig['host'],
         user=dbconfig['user'],
         password=dbconfig['password'],
         database=dbconfig['database']
         )
         self.con.autocommit = True
         print("Database connection established")

      except:
         print("Database connection failed")

      self.cur = self.con.cursor(dictionary=True)

   def getAllUsers(self):
      self.cur.execute("SELECT * FROM users")
      rows = self.cur.fetchall()
      # print(rows)
      if len(rows)>0:
         result = make_response({'payload': rows}, 200)
         result.headers['Access-Control-Allow-Origin'] = '*'
         return result
      else:
         return make_response({'message': "No users found"}, 204)
      
   def addUser(self, data):
      self.cur.execute(f"INSERT INTO users(name, email, phoneNumber, role_id, password) VALUES('{data['name']}', '{data['email']}', '{data['phoneNumber']}', '{data['role_id']}', '{data['password']}')")
      return make_response({'message': "User added successfully"}, 201)
   
   def updateUser(self, data):
      self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phoneNumber='{data['phoneNumber']}', role_id='{data['role_id']}', password='{data['password']}' WHERE id={data['id']}")
      if self.cur.rowcount>0:
         return make_response({'message': "User updated"}, 201)
      else:
         return make_response({'message': "User not found"}, 202)
      
   def deleteUser(self, id):
      self.cur.execute(f"DELETE FROM users WHERE id={id}")
      if self.cur.rowcount>0:
         return make_response({'message': "User deleted"}, 200)
      else:
         return make_response({'message': "User not found"}, 202)
      
   def patchUser(self, id, data):
      
      query = "UPDATE users SET "

      for key in data:
         query += f"{key}='{data[key]}',"

      query = query[:-1] + f" where id={id}"
      
      self.cur.execute(query)

      if self.cur.rowcount>0:
         return make_response({'message': "User updated"}, 201)
      else:
         return make_response({'message': "User not found"}, 202)
      
   def getPageUser(self, limit, page):

      limit = int(limit)
      page = int(page)

      start = (limit * page) - limit

      query = f"SELECT * FROM users LIMIT {start}, {limit}"

      self.cur.execute(query)

      rows = self.cur.fetchall()
      # print(rows)
      if len(rows)>0:
         result = make_response({'payload': rows, 'page_no': page, 'page_limit': limit}, 200)
         return result
      else:
         return make_response({'message': "No users found"}, 204)
      
   def uploadAvatarFile(self, id, filePath):
      self.cur.execute(f"UPDATE users SET avatar='{filePath}' WHERE id={id}")
      if self.cur.rowcount>0:
         return make_response({'message': "File Uploaded"}, 201)
      else:
         return make_response({'message': "User not found"}, 202)
      
   def loginUser(self, data):
      self.cur.execute(f"SELECT name, email, phoneNumber, avatar, role_id FROM users WHERE email='{data['email']}' AND password='{data['password']}'")

      result = self.cur.fetchall()

      userData = result[0]

      expTime = datetime.now() + timedelta(minutes=15)
      epochExpTime = int(expTime.timestamp())

      payload = {
         'payload': userData,
         'exp': epochExpTime
      }

      token = jwt.encode(payload, 'secret-key', algorithm='HS256')

      return make_response({'token': token}, 200)
      # return str(userData)