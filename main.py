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
        parameters = req['result']['parameters']
    except AttributeError:
        return 'json error'

    if parameters.get('account'):
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
                    response = row[0]
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
                    print("MySQL connection is closed")
    return make_response(jsonify({'fulfillmentText': response})


if __name__ == '__main__':
    app.run()