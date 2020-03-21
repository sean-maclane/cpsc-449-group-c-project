from marshmallow import Schema, fields, pprint

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    userName = fields.Str()
    email = fields.Str()
    karma = fields.Int()
    # formatted_name = fields.Method("format_name", dump_only=True)

    def format_name(self, Users):
        return "{},{},{}".format(Users.userName, Users.email, Users.karma)

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    community = fields.Str()
    Username = fields.Str()

    def format_name(self, Posts):
        return "{},{},{}".format(Posts.title, Posts.community, Posts.Username)
