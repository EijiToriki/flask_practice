from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello world</h1>'

@app.route('/test')
def test():
    return '<h1>Hello Test Page</h1>'

@app.route('/user/<user_id>')
def userid(user_id):
    return '<h1>Your User ID is {0} {1} {2}</h1>'.format(user_id[0], user_id[1], user_id[2])


if __name__ == '__main__':
    app.run(debug=True)