from flask import Flask

app = Flask(__name__, static_folder='static')

if __name__ == '__main__':
    print('\n\n>> Running FRONTEND microservice at 8000 port <<\n\n')
    app.run(debug=True, port=8000)
