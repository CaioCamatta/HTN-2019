from flask import Flask, request, render_template
import firebase_admin
from firebase_admin import credentials,firestore

app = Flask(__name__, template_folder='assets')
cred = credentials.Certificate("./ServiceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)

def submit_firebase(id, data):
    
    db = firestore.client()
    doc_ref = db.collection(u'HackTheNorth').document(f'questions-{id}')

    doc_ref.set({
        u'name': f"{id}",
        u'answers': {
            "1":u"",
            "2":u"",
            "3":u"",
            "4":u"",
            "5":u"",
            "6":u"",
            "7":u"",
            "8":u"",
            "9":u"",
            "10":u"",
        },
    })

def check_done(id):
    
    db = firestore.client()
    doc_ref = db.collection(u'HackTheNorth').document(f'questions-{id}-done')
    data = doc_ref.get().to_dict()
    print("data: ",data)

    if data['done'] == "True":
        return True

    else:
         return False

@app.route('/')
def hello_world():
    return 'Hello Hack the North!'


@app.route('/questions/N77G', methods=['GET', 'POST'])
def questions():
    page_code = str(request.path[-4:])

    if request.method == 'POST':
        data = request.json
        print(data)
        print(request.path[-4:])
        submit_firebase(page_code, data)
        return render_template("index.html")
    
    elif check_done(page_code):
        return "DONE"

    return render_template("index.html")


@app.route('/questions/N77G/done', methods=['GET'])
def questions_done():
    page_code = str(request.path[-9:-5])
    print(page_code)

    db = firestore.client()
    doc_ref = db.collection(u'HackTheNorth').document(f'questions-{page_code}-done')

    doc_ref.set({
        u'done': "True",
    })

    return "Changed to DONE"

@app.route('/questions/N77G/notdone', methods=['GET'])
def questions_notdone():
    page_code = str(request.path[-12:-8])
    print(page_code)

    db = firestore.client()
    doc_ref = db.collection(u'HackTheNorth').document(f'questions-{page_code}-done')

    doc_ref.set({
        u'done': "False",
    })

    return "Changed to NOT DONE"

if __name__ == '__main__':

    app.run()
