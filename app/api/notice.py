from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace, fields
from util.commUtil import CommUtil

Notice = Namespace(
    name="Notice",
    description="Notice API",
)

commUtil = CommUtil()

@Notice.route("/send")
class NoticeSender(Resource):
    """Notice Sender"""

    def post(self):
        req = request.get_json()

        commUtil.insert(commUtil.col_notice, {
            'seniorId': int(req['id']),
        })

        return make_response({
            'isLogin': True
        }, 201)