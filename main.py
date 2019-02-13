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
        return make_response(jsonify({"speech": res}))

"""    if parameters.get('account'):
        if str(parameters.get('account')) == str('savings'):
            try:
                mySQLconnection = mysql.connector.connect(host='203.88.129.243',
                    database='banking',
                    user='jaydeep',
                    password='jaydeep',
                    port='1234')
                sql_select_Query = "select balance from account where account_type='savings'"
                cursor = mySQLconnection .cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()

                for row in records:
                    ful = row[0]
                    ful_send = str(ful)
                    print("Your savings balance is = ", row[0])
            except Error as e:
                print ("Error while connecting to MySQL", e)
            finally:
                if(mySQLconnection .is_connected()):
                    mySQLconnection.close()

        if parameters.get('account') == 'current':
            try:
                mySQLconnection = mysql.connector.connect(host='203.88.129.243',
                    database='banking',
                    user='jaydeep',
                    password='jaydeep',
                    port='1234')
                sql_select_Query = "select balance from account where account_type='current'"
                cursor = mySQLconnection .cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()
                
                for row in records:
                    response = row[0]
                    print("Your current balance is = ", row[0])
            except Error as e:
                print ("Error while connecting to MySQL", e)
            finally:
                if(mySQLconnection .is_connected()):
                    mySQLconnection.close()
                    print("MySQL connection is closed")"""
    


def check_balance(req):
    parameters = req['result']['parameters']

    print('Dialogflow parameters:')
    print(json.dumps(parameters, indent=4))

    if parameters.get('account'):
        if str(parameters.get('account')) == str('savings'):
            try:
                mySQLconnection = mysql.connector.connect(host='203.88.129.243',
                    database='banking',
                    user='jaydeep',
                    password='jaydeep',
                    port='1234')
                sql_select_Query = "select Balance from account where AccountType='Savings';'"
                cursor = mySQLconnection .cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()

                for row in records:
                    bal = row[0]
                    bal = json.dumps("Your Current balance is: {}".format(bal))
                    

            except Error as e:
                print ("Error while connecting to MySQL", e)

        elif str(parameters.get('account')) == str('current'):
            try:
                mySQLconnection = mysql.connector.connect(host='203.88.129.243',
                    database='banking',
                    user='jaydeep',
                    password='jaydeep',
                    port='1234')
                sql_select_Query = "select Balance from account where AccountType='Current';"
                cursor = mySQLconnection .cursor()
                cursor.execute(sql_select_Query)
                records = cursor.fetchall()

                for row in records:
                    bal = row[0]
                    bal = str(json.dumps('Your Current balance is:', bal))

            except Error as e:
                print ("Error while connecting to MySQL", e)

    return bal



if __name__ == '__main__':
    app.run()