# pip install flask
from flask import Flask, session, render_template, redirect, request, url_for
import sys
import json
import pymysql #pip install flask-mysql
import requests #pip install requests
 
app = Flask(__name__)
app.secret_key='flaskkk!'

class Row:
  def __init__(self, index, row):
    self.index = index
    self.row = row
  def encode(self):
    return self.__dict__
#print(Row(1, ('test1','test2')).encode())

class User:
  def __init__(self, id, name, useYn):
    self.id = id
    self.name = name
    self.useYn = useYn
  def encode(self):
    return self.__dict__
#print(User('jico', 'jermain', 'Y').encode())

systemName = 'myFirstFlask'

'''
    my first flask api
'''
@app.route('/', methods=['GET'])
def main():
    reqMth = sys._getframe().f_code.co_name
    id = None
    session['login_user'] = 'meme'
    #session.clear()
    if session: id = session['login_user']
    print('login_user:', id)
    return render_template('home.html', system=systemName, menu=reqMth)

def conn(): 
    conn = pymysql.connect( charset='utf8',
        host='', port=3306, 
        db='', user='', passwd='',
    )
    return conn

def select(cond1): 
    conn = conn()
    reqMth = sys._getframe().f_code.co_name
    sql = "SELECT * FROM `users`" 
    if cond1: 
        sql = sql+" WHERE id LIKE '%s'" % (cond1)
    print(str(reqMth)+': select by (', cond1, '):', sql)
    cursor = conn.cursor()
    queryResult = cursor.execute(sql)
    dataResult = cursor.fetchall()
    dataCount = len(dataResult) 
    cursor.close()
    #conn.close()
    #dataResult = None

    resultArray = []
    for idx in range(dataCount):
        resultArray.append(
            Row(idx, dataResult[idx])
        )
    
    return [resultArray, sql]

def dump(toDump, indent): 
    validIndent =(
        indent
            if(type(indent).__name__ == 'int') else
        None
    )
    return json.dumps(toDump, default=lambda o: o.encode(), indent=validIndent)

@app.route('/select', methods=['GET', 'POST'])
def getAllData():
    reqMth = sys._getframe().f_code.co_name
    queryResult = None 
    resultMsg = None
    if request.method == 'GET':

        queryResult = select(None)
        if not queryResult: resultMsg = (str(reqMth)+': '+str(queryResult[1])+' has no data!')
        else: resultMsg = (str(reqMth)+': '+str(queryResult[1])+' got '+dump(queryResult[0],None))
        print(resultMsg)

    return (
        json.dumps(queryResult[0], default=lambda o: o.encode(), indent=4)
            if(len(queryResult[0])>0) else 
        resultMsg
    )

@app.route('/select/<userId>', methods=['GET', 'POST'])
def getaDataBy_Id(userId):
    reqMth = sys._getframe().f_code.co_name
    queryResult = None
    resultMsg = None
    if request.method == 'GET':

        queryResult = select(userId)
        if not queryResult: resultMsg = (str(reqMth)+': '+str(queryResult[1])+' has no data!')
        else: resultMsg = (str(reqMth)+': '+str(queryResult[1])+' got '+dump(queryResult[0],None))
        print(resultMsg)

    return (
        json.dumps(queryResult[0], default=lambda o: o.encode(), indent=4)
            if(len(queryResult[0])>0) else 
        resultMsg
    )
 
#http://localhost:5000/insert?id=userID&name=userNAME
@app.route('/insert', methods=['GET', 'POST'])
def registerUserBy_IdName():
        reqMth = sys._getframe().f_code.co_name
        queryResult = None
    #if request.method == 'POST':
        id = request.args.get('id')
        name = request.args.get('name')
        if id and name: 
            
            conn = conn()
            sql = "INSERT INTO users VALUES ('%s', '%s', 'Y')" % (id, name)
            print(str(reqMth)+': insert by:', sql)
            cursor = conn.cursor()
            queryResult = cursor.execute(sql)
            print(queryResult)
            conn.commit()
            cursor.close()
            #conn.close()

        return str('insert success' if(queryResult==1) else 'insert failed')

@app.route('/any', methods=['GET', 'POST'])
def goToAnyMain():
    reqMth = sys._getframe().f_code.co_name
    import os,time
    names = os.listdir(os.path.join(app.template_folder, 'any'))
    return 'we have '+str(names)

@app.route('/any/<page>', methods=['GET', 'POST'])
def getAnyOther(page):
    reqMth = sys._getframe().f_code.co_name
    param = request.args.get('param')
    print(str(reqMth)+' page by (', page, '):')
    return render_template('any/'+page, param=param, system=systemName, menu=reqMth)

from werkzeug.exceptions import HTTPException
app.config['TRAP_HTTP_EXCEPTIONS']=True

@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(error):
    return render_template('sub/pageError.html')

'''
@app.errorhandler(HTTPException)
def http_error_handler(error):
    return str('HTTPException')

@app.errorhandler(Exception)
def http_error_handler(error):
    return str('Exception')
'''

if __name__ == '__main__':
    app.run()

