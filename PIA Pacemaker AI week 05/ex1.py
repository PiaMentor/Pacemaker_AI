from flask import Flask

app = Flask(__name__)
@app.route('/')
def index():
    return '''<!DOCTYPE html>
    <html>
        <head>
            <title>PIA</title>
        </head>
        <body>
            <div>Hello World 123</div>
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)