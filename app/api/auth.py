from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace, fields
from util.commUtil import CommUtil
from random import randint

Auth = Namespace(
    name="Auth",
    description="Auth API",
)

auth_model = Auth.model('Users', {
    'id': fields.String(description='a User ID', required=True, example='root'),
    'password': fields.String(description='a Password', required=True, example='pass'),
})

auth_model_for_senior = Auth.model('Senior', {
    'id': fields.String(description='a Senior User ID', required=True, example='123456'),
})

user_model_for_guardian = Auth.model('Guadian', {
    'guardianName': fields.String(description='a Guardian Name', required=True, example='guardianNm'),
    'seniorName': fields.String(description='a Seinor Name', required=True, example='seniorNm'),
})

user_model_by_login = Auth.inherit('UserByLogin', user_model_for_guardian, {
    'isLogin': fields.Boolean(description='User Login Status', required=True, example=True)
})

register_model = Auth.model('RegisterReq', {
    'id': fields.String(description='a User ID', required=True, example='root'),
    'password': fields.String(description='a Password', required=True, example='pass'),
    'guardianName': fields.String(description='a Guardian Name', required=True, example='guardianNm'),
    'seniorName': fields.String(description='a Seinor Name', required=True, example='seniorNm'),
})

register_res_model = Auth.model('RegisterResponse', {
    'isRegister': fields.Boolean(description='User Register Status', required=True, example=True),
    'seniorId': fields.String(description='a Seinior ID', required=True, example='123456'),
})

commUtil = CommUtil()

@Auth.route("/senior")
class AuthSenior(Resource):
    """Auth Main"""

    @Auth.expect(auth_model_for_senior)
    @Auth.response(201, 'Success', user_model_by_login)
    def post(self):
        req = request.get_json()

        user = commUtil.findOne(commUtil.col_user, {
            'seniorId': int(req['id']),
        })

        print(user)

        return make_response({
            'seniorName': user['seniorName'],
            'isLogin': True
        }, 201)

@Auth.route("/guardian")
class AuthGuardian(Resource):
    """Auth Main"""

    @Auth.expect(auth_model)
    @Auth.response(201, 'Success', user_model_by_login)
    def post(self):
        req = request.get_json()

        user = commUtil.findOne(commUtil.col_user, {
            'guardianId': req['id'],
            'password': req['password']
        })

        return make_response({
            'guardianName': user['guardianName'],
            'seniorName': user['seniorName'],
            'isLogin': True
        }, 201)

@Auth.route("/register")
class RegisterAuth(Resource):

    @Auth.expect(register_model)
    @Auth.response(201, 'Success', register_res_model)
    def post(self):
        req = request.get_json()

        # 보호자 번호 생성
        seniorId = randint(100000, 999999)

        commUtil.insert(commUtil.col_user, {
            'guardianId': req['id'],
            'guardianName': req['guardianName'],
            'seniorId': seniorId,
            'seniorName': req['seniorName'],
            'password': req['password'],
        })

        return make_response({
            'isRegister': True,
            'seniorId': seniorId
        }, 201)