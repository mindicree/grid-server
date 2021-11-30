from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#ROUTES
@app.route('/')
def index():
    return render_template('index.html')

#ROUTES
@app.route('/syslogs')
def syslogs():
    return render_template('syslogs.html')

#RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=True, port=5001)