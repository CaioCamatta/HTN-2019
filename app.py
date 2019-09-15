from flask import Flask, request, render_template
import firebase_admin
from firebase_admin import credentials,firestore
import random

app = Flask(__name__, template_folder='static')
cred = credentials.Certificate("./ServiceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)

def submit_firebase(id, data):
    index = random.randrange(0, 999999)
    
    db = firestore.client()
    doc_ref = db.collection(u'HackTheNorth').document(f'questions-{id}')

    print("here")
    doc_ref.update({
        f'name_{index}': f"{data[10]}",
        f'answers_{index}': {
            "1":f"{data[0]}",
            "2":f"{data[1]}",
            "3":f"{data[2]}",
            "4":f"{data[3]}",
            "5":f"{data[4]}",
            "6":f"{data[5]}",
            "7":f"{data[6]}",
            "8":f"{data[7]}",
            "9":f"{data[8]}",
            "10":f"{data[9]}",
        },
    })

def check_done(id):
    
    db = firestore.client()
    doc_ref = db.collection(u'HackTheNorth').document(f'questions-{id}-done')   
    data = doc_ref.get().to_dict()

    if data['done'] == "True":
        return True

    else:
         return False

@app.route('/')
def hello_world():
        return render_template("intro.html")


@app.route('/questions/N77G', methods=['GET', 'POST'])
def questions():
    page_code = str(request.path[-4:])

    if request.method == 'POST':
        data = request.json
        submit_firebase(page_code, data)
        return render_template("index.html")
    
    elif check_done(page_code):
        all_answers_given = [[],[],[],[],[],[],[],[],[],[]]
        
        db = firestore.client()
        participant_ref = db.collection(u'HackTheNorth').document(u"questions-N77G") 
        actual_ref = db.collection(u'HackTheNorth').document(u"questions-N77G-correct")
        
        participant_doc = participant_ref.get()
        actual_doc = actual_ref.get()
        # print(participant_doc.to_dict())
        
        length_of_doc = len(actual_doc.to_dict()['answers'])
        # print(participant_doc.to_dict()['answers_2'])
        
        answer_list = []
        
        correct_answers = [
            actual_doc.to_dict()['answers']['1'],
            actual_doc.to_dict()['answers']['2'], 
            actual_doc.to_dict()['answers']['3'],
            actual_doc.to_dict()['answers']['4'],
            actual_doc.to_dict()['answers']['5'],
            actual_doc.to_dict()['answers']['6'],
            actual_doc.to_dict()['answers']['7'],
            actual_doc.to_dict()['answers']['8'],
            actual_doc.to_dict()['answers']['9'],
            actual_doc.to_dict()['answers']['10']
        ]
        
        for key in participant_doc.to_dict().keys():
            # print(key)
            try:
                if key[:6] == 'answer':
                    answer_list.append(key)
            except:
                pass
            
        # print(answer_list)
        
        for key in answer_list: 
            
            guesses = [
                participant_doc.to_dict()[key]['1'],
                participant_doc.to_dict()[key]['2'], 
                participant_doc.to_dict()[key]['3'],
                participant_doc.to_dict()[key]['4'],
                participant_doc.to_dict()[key]['5'],
                participant_doc.to_dict()[key]['6'],
                participant_doc.to_dict()[key]['7'],
                participant_doc.to_dict()[key]['8'],
                participant_doc.to_dict()[key]['9'],
                participant_doc.to_dict()[key]['10']
            ]
            
            for i in range(0, len(correct_answers)):
                if guesses[i] == correct_answers[i]:
                    all_answers_given[i].append('True')
                else:
                    all_answers_given[i].append('False')
                    
        
        individual_average_mark = 0
        final_average_mark = []
        
        for i in all_answers_given:
            for j in i:
                if j == 'True':
                    individual_average_mark += 1
                    
            final_average_mark.append(float(individual_average_mark)/len(i) *100)
            individual_average_mark = 0
            
        return render_template("results.html", data=[int(i) for i in final_average_mark])
        
    return render_template("index.html")


@app.route('/questions/<page_id>/done', methods=['GET'])
def questions_done(page_id):
    db = firestore.client()
    doc_ref = db.collection(u'HackTheNorth').document(f'questions-{page_id}-done')

    doc_ref.set({
        u'done': "True",
    })

    return "Changed to DONE"

@app.route('/questions/<page_id>/notdone', methods=['GET'])
def questions_notdone():
    db = firestore.client()
    doc_ref = db.collection(u'HackTheNorth').document(f'questions-{page_id}-done')

    doc_ref.set({
        u'done': "False",
    })

    return "Changed to NOT DONE"

if __name__ == '__main__':

    app.run()
