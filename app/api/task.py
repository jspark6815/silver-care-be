from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace, fields
from util.commUtil import CommUtil

Task = Namespace(
    name="Task",
    description="Task API",
)

commUtil = CommUtil()

@Task.route("")
class TaskMain(Resource):
    def post(self):
        req = request.get_json()

        commUtil.insert(commUtil.col_notice, {
            'seniorId': int(req['id']),
        })

        return make_response({
            'isLogin': True
        }, 201)

@Task.route("/<int:seniorId>")
class TaskListInqr(Resource):
    """Task Sender"""
    def get(self, seniorId):
        taskList = commUtil.findList(commUtil.col_task, {
            'seniorId': seniorId,
        })

        return make_response({
            'isLogin': True
        }, 201)