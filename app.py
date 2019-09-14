from flask import Flask, request, render_template
import firebase_admin
from firebase_admin import credentials,firestore

app = Flask(__name__, template_folder='assets')

def submit_firebase(id):
    cred = credentials.Certificate("./ServiceAccountKey.json")
    default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    doc_ref = db.collection(u'HackTheNorth').document(f'questions-{id}')
    doc_ref.set({
        u'name': u"",
        u'id': f"{id}",
        u'page':u"",
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

@app.route('/')
def hello_world():
    return 'Hello Hack the North!'


@app.route('/questions/N77G', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        asd = request.json
        print(asd)
        print(request.path[-4:])
        submit_firebase(str(request.path[-4:]))
        return render_template("index.html")

    return render_template("index.html")

if __name__ == '__main__':
    app.run()
