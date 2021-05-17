import requests

base_url = "http://127.0.0.1:5000/"

#r = requests.post(f"{base_url}/users", data={"id":"2", "name":"nikhil", "branch":"COE", "test":"test"})

#print(r.content)

"""
r = requests.post(f"{base_url}/login", data={"username": "test", "password":"test"})

print(r.json()['access_token'])
"""
"""
token = r.json()['access_token']

head = {'Authorization': 'Bearer {}'.format(token)}

r = requests.get(f"{base_url}/protected", headers=head)

print(r.content)
"""

r = requests.post(f"{base_url}/users/registration", data={"username": "test", "password":"test", "name": "Laci", "right": "admin"})
print(r.content)

"""
r = requests.post(f"{base_url}/question/addquestion", data={"description": "descT", "name": "question1", "difficulty": 1, "category_id": 1, "image": "/asd/asd", "answers": ['A1', 'A2', 'A3'], "correctAnswerNum" :["1","2"]})
print(r.content)
"""
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
"""
r = requests.post(f"{base_url}/question/editquestion", 
    json={
   "question_id": "0ac28bb0-ace4-11eb-bc3e-ca3fc8fc7c00",
   "question":{
      "correctAnswerNum":[
         1
      ],
      "name":"C-Test_Size_of_array",
      "description":"The total memory required for an array",
      "difficulty":"1",
      "answers":[
         {
            "id":"None",
            "question_id":"None",
            "answer":"Sizeof (datatype) * 2",
            "correct":"None"
         },
         {
            "id":"None",
            "question_id":"None",
            "answer":"Sizeof (datatype) * sizeof array",
            "correct":"None"
         },
         {
            "id":"None",
            "question_id":"None",
            "answer":"Size of (datatype) * size of used array elements",
            "correct":"None"
         },
         {
            "id":"None",
            "question_id":"None",
            "answer":"Size of (array) * datatype",
            "correct":"None"
         }
      ],
      "category_id":"2",
      "image":"None",
      "reviewed":1
   }
}, headers=headers)
print(r.content)
"""
r = requests.post(f"{base_url}/question/delete-question", 
    json={
      "question_id": "0ac28bb0-ace4-11eb-bc3e-ca3fc8fc7c00"
    }
, headers=headers)
print(r.content)

r = requests.get(f"{base_url}/question/getquestions")
print(r.content)

r = requests.post(f"{base_url}/question/newcategory", 
    json={
      "categoryname": "category1"
    }
, headers=headers)
print(r.content)