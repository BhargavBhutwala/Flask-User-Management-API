from marshmallow import ValidationError
from app import app
from model.user_model import User
from model.auth_model import Auth
from flask import request, send_file, make_response, jsonify
from datetime import datetime
from schemas import UserSchema, UserPatchSchema

user = User()
auth = Auth()
user_schema = UserSchema()
user_patch_schema = UserPatchSchema()

@app.route('/user/')
@auth.token_auth()
def getAllUsers():
   return user.getAllUsers()

@app.route('/user/add', methods=['POST', 'OPTIONS'])
def addUser():
   # print(request.form)
   if request.method == 'OPTIONS':
      # Handling preflight request (OPTIONS)
      if request.method == 'OPTIONS':  # Handle preflight request
         response = jsonify({"message": "Preflight request handled"})
         response.headers.add("Access-Control-Allow-Origin", "http://localhost:4200")
         response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
         response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
         return response
   try:
      data = user_schema.load(request.json)
   except ValidationError as err:
      return make_response({"error": err.messages}, 400)
   return user.addUser(data)

@app.route('/user/update', methods=['PUT'])
@auth.token_auth()
def updateUser():
   # print(request.form)
   try:
      data = user_schema.load(request.form)
   except ValidationError as err:
      return make_response({"error": err.messages}, 400)
   return user.updateUser(data)

@app.route('/user/delete/<id>', methods=['DELETE'])
@auth.token_auth()
def deleteUser(id):
   # print(request.form)
   return user.deleteUser(id)

@app.route('/user/patch/<id>', methods=['PATCH'])
@auth.token_auth()
def patchUser(id):
   # print(request.form)
   try:
      data = user_patch_schema.load(request.form)
   except ValidationError as err:
      return make_response({"error": err.messages}, 400)
   return user.patchUser(id, data)

@app.route('/user/getall/limit/<limit>/page/<page>', methods=['GET'])
@auth.token_auth()
def getPageUser(limit, page):
   # print(request.form)
   return user.getPageUser(limit, page)

@app.route('/user/<id>/uploadAvatar', methods=['PUT'])
@auth.token_auth()
def uploadAvatarFile(id):
   # print(request.form)
   file = request.files['avatar']
   fileName = str(datetime.now().timestamp()).replace(".", "")
   nameSplit = file.filename.split(".")
   ext = nameSplit[len(nameSplit)-1]
   filePath = f"uploads/{fileName}.{ext}"
   file.save(filePath)
   # return user.uploadAvatarFile(id)
   return user.uploadAvatarFile(id, filePath)

@app.route('/uploads/<fileName>')
@auth.token_auth()
def getAvatarFile(fileName):
   return send_file(f"uploads/{fileName}")

@app.route('/user/login', methods=['POST'])
def loginUser():
   # print(request.form)
   return user.loginUser(request.form)