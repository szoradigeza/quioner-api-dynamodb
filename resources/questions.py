from helpers.request_check import *
from helpers.json_resp import json_response
from helpers.dynamodb import ddb
from datetime import datetime
from flask import jsonify
from boto3.dynamodb.conditions import Key
import uuid
from models.question import QuestionModel
from flask import send_file


def handle_add_question(request):
    try:
        questions_table = ddb.Table('question')
        answers_table = ddb.Table('answer')
        description = request.form['description']
        name = request.form['name']
        difficulty = request.form['difficulty']
        
        category = request.form['category_id']
        image = request.form['image']

        correctAnswerNum = request.form.getlist('correctAnswerNum')
        correctAnswerNum = list(map(int, correctAnswerNum))
        
        answers = request.form.getlist('answers')
        question = QuestionModel(name, description, difficulty, image, answers, correctAnswerNum)
        question.save_question_and_answers()
        return jsonify({"response" : "Succesfull!"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 200


def handle_edit_question(request):
    try:
        #data = request.get_json(force=True)
        data = request.get_json(force=True)
        question_id = data['question_id']
        edited_question = data['question']
        edited_answers = edited_question['answers']
        
        #delete question and answer
        QuestionModel.delete_question_and_answers_by_question_id(question_id)

        #save modified question
        answers = []
        for answer in edited_question['answers']:
            answers.append(answer['answer']) 
        question = QuestionModel(
            edited_question['name'],
            edited_question['description'],
            edited_question['difficulty'],
            edited_question['image'],
            answers,
            edited_question['correctAnswerNum'],
            edited_question['reviewed'],
            question_id
            )
        question.save_question_and_answers()

        return json_response({"message": answers})
    except Exception as e:
        return jsonify({"message": str(e)}), 200


def handle_delete_question(request):
    try:
        data = request.get_json(force=True)
        question_id = data['question_id']
        QuestionModel.delete_question_and_answers_by_question_id(question_id)
        return json_response({"message": "question has been deleted!"})
    except Exception as e:
        print(e)


def handle_get_all_questions():
    questions = QuestionModel.get_all_question()
    return json_response(questions)


def handle_diff_by_num(request):
    pass

def handle_generate_test(request):
    pass

def handle_get_question_categories():
    try:
        category_table = ddb.Table('category')
        categories = category_table.scan()['Items']
        return json_response(categories)
    except Exception as e:
        return json_response({"message": e})


def handle_create_new_question_category(request):
    categoryname = request.get_json(force=True)['categoryname']
    #Check that category not exist    
    table = ddb.Table('category')
    key = {'name': categoryname}
    is_category = table.get_item(Key=key)
    if is_category.get('Item'):
        return json_response({"message": "Category already exist!"})

    table = ddb.Table('category')
    table.put_item(Item={
        'id': str(uuid.uuid1()),
        'name': categoryname
    })
    return json_response({"message": "category has been added!"})

def handle_add_question_image(request):
    #TODO maybe need to rework
    try:
      static_file = request.files['image']
      fileName = secure_filename(static_file.filename)
      if os.path.exists('image/' + fileName):
        i = 1
        splitName = fileName.split('.')
        fileName = splitName[0] + str(i) + '.' + splitName[1]
        while os.path.exists('image/' + fileName):
          fileName = splitName[0] + str(i) + '.' + splitName[1]
          i += 1
        static_file.save(os.path.join('Image', fileName))
      else:
        static_file.save(os.path.join('Image', fileName))
      return {'fileName': fileName}
    except Exception as e:
        return json_response({"message": e})

def handle_get_question_image(request):
    return send_file('Image/' + filename)

def handle_post_similar_question(request):
    #TODO maybe don't necessary
    pass

def handle_sort_questions_by_category(request):
    #TODO maybe don't necessary
    pass

def handle_get_reviewed_questions():
    questions = QuestionModel.get_all_question()
    reviewed_questions = []
    for question in questions:
        if question['reviewed'] == 1:
            reviewed_questions.append(question)
    return json_response(reviewed_questions) 

def handle_get_unreviewed_questions(request):
    questions = QuestionModel.get_all_question()
    unreviewed_questions = []
    for question in questions:
        if question['reviewed'] == 0:
            unreviewed_questions.append(question)
    return json_response(reviewed_questions) 

