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
    print(req)
    try:
        action = req.get('result').get('action')
    except AttributeError:
        return 'json error'

    if action == 'check_balance':
        res = check_balance(req)
        

    elif action == 'get_transactions':
        res = get_transaction(req)
    
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

def get_transaction(req):
    parameters = req['result']['parameters']

   if parameters.get('branch'):
    records = MySQL("select * from transaction order by TranscationDate DESC LIMIT 10 ;")
    for row in records:
        return 'TransactionID: %s' %row[0]
        return 'AccountID: '% row[1]
        return 'Credit: ' %row[2]
        return 'Debit: ' %row[3]
        return 'balance: ' %row[4]
        return 'TransactionType: ' %row[5]
        return 'TranscationDate: ' %row[6] '\n'    
            """ 
           if str(parameters.get('branch')) == str('branch city'):
               records = MySQL("select Balance from account where AccountType='Savings';'")
               for row in records:
                   bal = row[0]
                   return 'Your Savings balance is: %s' % bal
   
           elif str(parameters.get('branch')) == str('branch area'):
               records = MySQL("select Balance from account where AccountType='Current';'")
               for row in records:
                   bal = row[0]
                   return 'Your Current balance is: %s' % bal
   
           elif str(parameters.get('branch')) == str('branch name'):
               records = MySQL("select Balance from account where AccountType='Current';'")
   
           elif str(parameters.get('branch')) == str('branch information'):
               records = MySQL("select Balance from account where AccountType='Current';'") """   


if __name__ == '__main__':
    app.run()