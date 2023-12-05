from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace, fields
from util.commUtil import CommUtil

Auth = Namespace(
    name="Auth",
    description="Auth API",
)

auth_model = Auth.model('Users', {
    'id': fields.String(description='a User ID', required=True, example='root'),
    'password': fields.String(description='a Password', required=True, example='pass'),
})

user_model_with_info = Auth.inherit('User', auth_model, {
    'name': fields.String(description='a User Name', required=True, example='js'),
})

user_model_by_login = Auth.inherit('UserByLogin', user_model_with_info, {
    'isLogin': fields.Boolean(description='user is logined', required=True, example=True)
})

commUtil = CommUtil()

@Auth.route("")
class AuthMain(Resource):
    """Auth Main"""

    @Auth.expect(auth_model)
    @Auth.response(201, 'Success', user_model_by_login)
    def post(self):
        print("init")
        req = request.get_json()

        user = commUtil.findOne(commUtil.col_user, {
            'id': req['id'],
            'password': req['password']
        })

        return make_response({
            'name': user['name'],
            'isLogin': True
        }, 201)

@Auth.route("/register")
class RegisterAuth(Resource):

    @Auth.expect(user_model_with_info)
    @Auth.response(201, 'Success', auth_model)
    def post(self):
        req = request.get_json()

        commUtil.insert(commUtil.col_user, {
            'id': req['id'],
            'password': req['password'],
            'name': req['name']
        })

        return make_response({
            'isRegister': True,
            'code': 201
        }, 201)