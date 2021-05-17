from helpers.dynamodb import ddb
from datetime import datetime
from boto3.dynamodb.conditions import Key
import uuid


class QuestionModel:
    def __init__(self, name, description, difficulty, image, answers, correctAnswerNum, reviewed=0, id=0):
        if id == 0:
            question_id = str(uuid.uuid1())
        else:
            question_id = id
        self.id = question_id
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.reviewed = reviewed
        self.image = image
        self.answers = answers
        self.correctAnswerNum = correctAnswerNum

    def save_question_and_answers(self):
        questions_table = ddb.Table('question')
        answers_table = ddb.Table('answer')

        questions_table.put_item(Item={
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'difficulty': self.difficulty,
            'reviewed': self.reviewed,
            'image': self.image
        })

        counter = 0
        for answer in self.answers:
            correct = '0'
            if counter in self.correctAnswerNum:
                correct = '1'
            answers_table.put_item(Item={
                'id': str(uuid.uuid1()),
                'questionId': self.id,
                'answer': answer,
                'correct': correct
            })
            counter += 1

    @classmethod
    def delete_question_and_answers_by_question_id(cls, question_id):
        try:
            answers_table = ddb.Table('answer')
            answers = answers_table.scan(ProjectionExpression= 'id, questionId')['Items']
            for answer in answers:
                if str(answer['questionId']) == str(question_id):       
                    cls.delete_answer_by_id(answer['id'])
            cls.delete_question_by_id(question_id)
        except Exception as e:
            return json_response({"message": "Coudn't delete the question!"})
    @classmethod
    def delete_question_by_id(cls,question_id):
        questions_table = ddb.Table('question')
        response = questions_table.delete_item(
            Key={'id': question_id,}
        )
    @classmethod
    def delete_answer_by_id(cls,id):
        table = ddb.Table('answer')
        table.delete_item(
            Key={'id': id}
    )
    @classmethod
    def get_all_question(cls):
        questions_table = ddb.Table('question')
        return questions_table.scan()['Items']