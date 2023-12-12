from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace, fields
from util.commUtil import CommUtil

Notice = Namespace(
    name="Notice",
    description="Notice API",
)

notice_model = Notice.model('notice', {
    'seniorId': fields.String(description='a Senior User ID', required=True, example='123456'),
    'msg': fields.String(description='a Msg', required=True, example='약 챙겨 먹어!!'),
})

response_model = Notice.model('Comm Response', {
    'isSuccess': fields.Boolean(description='is Success', example=True)
})

commUtil = CommUtil()

@Notice.route("/send")
class NoticeSender(Resource):
    """Notice Sender"""

    @Notice.expect(notice_model)
    @Notice.response(201, 'Success', response_model)
    def post(self):
        req = request.get_json()

        commUtil.insert(commUtil.col_notice, {
            'seniorId': int(req['seniorId']),
            'msg': req['msg']
        })

        return make_response({
            'isSuccess': True
        }, 201)

@Notice.route("/receive/<int:seniorId>")
class NoticeReceiver(Resource):
    """Notice Receiver"""

    def get(self, seniorId):

        try:
            notice = commUtil.findOne(commUtil.col_notice, {
                'seniorId': seniorId,
            })
            
            commUtil.delete_many(commUtil.col_notice, {
                'seniorId': seniorId,
            })

            return make_response({
                'isSuccess': True,
                'msg': notice['msg'],
            }, 201)
        except:
            pass
        return make_response({
            'isSuccess': False,
            'msg': '',
        }, 201)