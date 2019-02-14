import json
from flask import Flask, request, make_response, jsonify

import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
log = app.logger

@app.route('/', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhook
    This is meant to be used in conjunction with the Banking Dialogflow agent
    """
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('result').get('action')
    except AttributeError:
        return 'json error'

    if action == 'check_balance':
        res = check_balance(req)

    elif action == 'get_transactions':
        res = get_transactions(req)

    
    return make_response(jsonify({"speech": res}))


def check_balance(req):
    parameters = req['result']['parameters']

    print('Dialogflow parameters:')
    print(json.dumps(parameters, indent=4))

    if parameters.get('account'):
        if str(parameters.get('account')) == str('savings'):
            records = MySQL("select Balance from account where AccountType='Savings';'")

            for row in records:
                bal = row[0]
                return 'Your Savings balance is: %s' % bal

        elif str(parameters.get('account')) == str('current'):
            records = MySQL("select Balance from account where AccountType='Current';")

            for row in records:
                bal = row[0]
                return 'Your Current balance is: %s' % bal

def MySQL(querry):
    try:
        mySQLconnection = mysql.connector.connect(host='203.88.129.243',
                    database='banking',
                    user='jaydeep',
                    password='jaydeep',
                    port='1234')
        sql_select_Query = querry
        cursor = mySQLconnection .cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        return records

    except Error as e :
        print ("Error while connecting to MySQL", e)

    finally:
        if(mySQLconnection .is_connected()):
            mySQLconnection.close()
            print("MySQL connection is closed")

def get_transactions(req):
    records = MySQL("select * from transaction order by TranscationDate DESC LIMIT 10 ;")
    miniStatement = []
    for row in records:
        miniStatement.append('TransactionID: %s ' %row[0] + 'AccountID: %s '% row[1] + 'Credit: %s ' %row[2] + 'Debit: %s ' %row[3] + 'balance: %s ' %row[4] + 'TransactionType: %s ' %row[5] + 'TranscationDate: %s' %row[6])
    return miniStatement
if __name__ == '__main__':
    app.run()