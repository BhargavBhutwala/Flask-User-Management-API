from functools import wraps
import mysql.connector
import json
from flask import make_response, request
from datetime import datetime, timedelta
import jwt
import re
from config.config import dbconfig

class Auth:

   def __init__(self):
      # Initialize database connection here
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

   def token_auth(self, endpoint=""):
      
      def inner1(func):

         @wraps(func)

         def inner2(*args):

            endpoint = request.url_rule

            print(endpoint)

            authorization = request.headers.get('Authorization')

            if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
            
               token = authorization.split(' ')[1]

               try:
                  jwtdecoded = jwt.decode(token, 'secret-key', algorithms="HS256")

               except jwt.ExpiredSignatureError:
                  return make_response({'message': 'Token Expired'}, 401) 

               role_id = jwtdecoded['payload']['role_id']

               self.cur.execute(f"SELECT roles from accessibility_view where endpoint = '{endpoint}'")

               row = self.cur.fetchall()

               if len(row)>0:
                  allowed_roles = json.loads(row[0]['roles'])
                  if role_id in allowed_roles:
                     # print('allowed')
                     return func(*args)
                  else:
                     return make_response({'message': 'Unauthorized Access'}, 403)
               else:
                  return make_response({'message': 'Unknown Endpoint'}, 404)
            
            else:
               return make_response({'message': 'Invalid Token'}, 401)

         return inner2
      return inner1
