from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html') # index.html 에 위의 html이 담겨있음

if __name__ == '__main__':
    app.run(debug=True)