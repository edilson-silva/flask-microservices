from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    print('\n\n>> Running ORDER microservice at 5001 port <<\n\n')
    app.run(debug=True, port=5003)
