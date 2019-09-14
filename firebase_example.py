import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate("./ServiceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

def getQuote(): 
    return {
        'question': "Would you tap your employee's shoulder?",
        'answer': "no"
    }

response = getQuote()
question = response['question']
answer = response['answer']

doc_ref = db.collection(u'HackTheNorth').document(u'questions-N77G')
doc_ref.set({
    u'name': u"",
    u'id': u"",
    u'page':u"",
    u'answers': {
        1:u"",
        2:u"",
        3:u"",
        4:u"",
        5:u"",
        6:u"",
        7:u"",
        8:u"",
        9:u"",
        10:u"",
    },
})


print(question + ' by ' + answer)