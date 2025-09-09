from flask import Flask, jsonify, request
import psycopg2
import mysql.connector



mydb = mysql.connector.connect(
  database = "",
    host= "",
    user="",
    password="",
    port=0
)

cursor = mydb.cursor()

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def home():
    cursor.execute("SELECT * FROM authorities")
    response = cursor.fetchall()
    print(response)
    if(request.method == 'GET'):
        data = "Hello world"
        return jsonify({'data': response})


@app.route('/getPolicy/<string:policy>', methods = ['GET'])
def getPolicy(policy:str):
    
    return jsonify({'data': policy, 'someOtherInfo':'whichIsRelevant'})


@app.route('/addPolicy/<string:policy>', methods = ['POST'])
def addPolicy(policy:str):
    
    data = "Attempt to add "
    return jsonify({'data': data+policy})



if __name__ == '__main__':
    app.run(debug=False)