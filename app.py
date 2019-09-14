from flask import Flask, request, render_template

app = Flask(__name__, template_folder='assets')


@app.route('/')
def hello_world():
    return 'Hello Hack the North!'


@app.route('/questions/N77G', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        asd = request.json
        print(asd)
        return render_template("index.html")

    return render_template("index.html")

if __name__ == '__main__':
    app.run()
