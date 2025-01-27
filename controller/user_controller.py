from app import app
from model.user_model import User
from model.auth_model import Auth
from flask import request, send_file
from datetime import datetime

user = User()
auth = Auth()

@app.route('/user/')
@auth.token_auth()
def getAllUsers():
   return user.getAllUsers()

@app.route('/user/add', methods=['POST'])
@auth.token_auth()
def addUser():
   # print(request.form)
   return user.addUser(request.form)

@app.route('/user/update', methods=['PUT'])
@auth.token_auth()
def updateUser():
   # print(request.form)
   return user.updateUser(request.form)

@app.route('/user/delete/<id>', methods=['DELETE'])
@auth.token_auth()
def deleteUser(id):
   # print(request.form)
   return user.deleteUser(id)

@app.route('/user/patch/<id>', methods=['PATCH'])
@auth.token_auth()
def patchUser(id):
   # print(request.form)
   return user.patchUser(id, request.form)

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