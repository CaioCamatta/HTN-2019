from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Hack the North!'

@app.route('/questions/N77G')
def questions():
    return 'Questions page!'

if __name__ == '__main__':
    app.run()
