from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace, fields
from util.commUtil import CommUtil
from datetime import datetime, date

Task = Namespace(
    name="Task",
    description="Task API",
)

task_model = Task.model('Tasks', {
    'datetime': fields.String(description='a Task Time', example='20231211150000'),
    'taskContent': fields.String(description='a Task', example='퀴즈풀기'),
})

task_model_with_seniorId = Task.inherit('Tasks with id', task_model , {
    'seniorId': fields.String(description='a Senior User ID', required=True, example='123456'),
})

commUtil = CommUtil()

@Task.route("")
class TaskMain(Resource):

    @Task.expect(task_model_with_seniorId)
    def post(self):
        req = request.get_json()

        commUtil.insert(commUtil.col_task, {
            'seniorId': int(req['seniorId']),
            'datetime': req['datetime'],
            'taskContent': req['taskContent']
        })

        return make_response({
            'isSuccess': True
        }, 201)

@Task.route("/<int:seniorId>")
class TaskListInqr(Resource):
    """Task Sender"""

    @Task.response(201, 'Success', [task_model])
    def get(self, seniorId):
        taskList = commUtil.findList(commUtil.col_task, {
            'seniorId': seniorId,
        })

        return make_response(taskList, 201)