from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace, fields
from util.commUtil import CommUtil
from datetime import datetime, date
from random import randint

Quiz = Namespace(
    name="Quiz",
    description="Quiz API",
)

quiz_model = Quiz.model('Quiz', {
    'seniorId': fields.String(description='a Senior User ID', required=True, example='123456'),
    'question': fields.String(description='a Task', example='전일 운동을 간 시간은?'),
    'choices': fields.List(fields.String(description='a answer', example='2시'), required=True),
})

quiz_model_with_answer = Quiz.model('Quiz', {
    'answer': fields.String(description='a Answer', example='8시'),
})


commUtil = CommUtil()

@Quiz.route("/<int:seniorId>")
class QuizMain(Resource):

    @Quiz.response(201, 'Success', quiz_model)
    def get(self, seniorId):
        try:
            quizList = commUtil.findList(commUtil.col_quiz, {
                'seniorId': seniorId,
            })

            rtn_list = []

            for quiz in quizList:
                rtn_list.append({
                    'question': quiz['question'],
                    'choices': quiz['choices'],
                    'answer': quiz['answer']
                })
            if len(quizList) != 0:
                return make_response(rtn_list, 201)
        except Exception as e:
            print(e)
        
        return make_response({
            'isSuccess': False
        }, 201)