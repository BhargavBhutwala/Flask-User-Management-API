from marshmallow import Schema, fields, validate

# For validating all fields when creating or updating a user
class UserSchema(Schema):
   name = fields.Str(required=True, validate=validate.Length(min=1))
   email = fields.Str(required=True, validate=validate.Email())
   phoneNumber = fields.Str(required=True, validate=validate.Length(min=10))
   role_id = fields.Int(required=True)
   password = fields.Str(required=True, validate=validate.Length(min=6))

# For validating optional fields when updating specific user data
class UserPatchSchema(Schema):
   name = fields.Str(validate=validate.Length(min=1))
   email = fields.Str(validate=validate.Email())
   phoneNumber = fields.Str(validate=validate.Length(min=10))
   role_id = fields.Int()
   password = fields.Str(validate=validate.Length(min=6))
