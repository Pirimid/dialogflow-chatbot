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
    parameters = req['result']['parameters']
    if parameters.get('transaction') or parameters.get('last') or parameters.get('date') or parameters.get('number') or parameters.get('date-period'):
        if parameters.get('number'):
            number_days = parameters.get('number')
            querry_pre = "select Credit, Debit, Balance, DATE_FORMAT(TranscationDate, '%m/%d/%Y') from transaction order by TranscationDate DESC LIMIT {};".format(number_days)
            records = MySQL(querry_pre)
            st = ''
            for row in records:
                    st = st + 'Transaction was performed on %s'%row[3]+' with Credit: %s'%row[0]+', Debit: %s'%row[1]+' and Balance after that was: %s'%row[2]+ "\n" 
                    print(st)
            return st

        if parameters.get('transaction') and parameters.get('last'):
            type_of_transaction = parameters.get('transaction')
            querry_pre = "select Credit, Debit, Balance, DATE_FORMAT(TranscationDate, '%m/%d/%Y') from transaction where(TransactionType = '{}') order by TranscationDate DESC LIMIT 1;".format(type_of_transaction)
            records = MySQL(querry_pre)
            st = ''
            for row in records:
                    st = st + 'Your last %s'%type_of_transaction+' was performed on %s'%row[3]+' with Credit: %s'%row[0]+', Debit: %s'%row[1]+' and Balance after that was: %s'%row[2]+ "\n" 
                    print(st)
            return st

        elif parameters.get('last'):
            querry_pre = "select Credit, Debit, Balance, DATE_FORMAT(TranscationDate, '%m/%d/%Y') from transaction order by TranscationDate DESC LIMIT 1;"
            records = MySQL(querry_pre)
            st = ''
            for row in records:
                    st = st + 'Your last transaction was performed on %s'%row[3]+' with Credit: %s'%row[0]+', Debit: %s'%row[1]+' and Balance after that was: %s'%row[2]+ "\n" 
                    print(st)
            return st

    else:
        records = MySQL("select *,DATE_FORMAT(TranscationDate, '%m/%d/%Y') from transaction order by TranscationDate DESC LIMIT 10 ;")
        st = ''
        for row in records:
            st = st + 'You had performed %s ' %row[5] + 'Type of Transaction On %s ' %row[7] + 'And it was of Credit: %s ' %row[2] + '& Debit: %s ' %row[3] + ', after which the balance was: %s ' %row[4] + "\n" 
            #TransactionID: %s '%row[0] + 'AccountID: %s '% row[1] + 'Credit: %s ' %row[2] + 'Debit: %s ' %row[3] + 'balance: %s ' %row[4] + 'TransactionType: %s ' %row[5] + 'TranscationDate: %s' %row[6]
            print(st)
        return st

if __name__ == '__main__':
    app.run()