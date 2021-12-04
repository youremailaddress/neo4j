from flask import Flask, request, abort,jsonify,render_template,copy_current_request_context
from sql import *
import json,time
app = Flask(__name__)
sql = SQL()

@app.template_filter('ctime')
def timectime(s):
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(s))

@app.route('/',methods=['GET',"POST"])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        data = request.form['data']
        if data == "":
            return json.dumps({"type":sql.randomselect()})
        t = sql.checkpersonstatus(data)
        if t == 0:
            sql.addvip(data)
        return json.dumps({"type":t})

@app.route('/dashboard.html',methods=["GET"])
def dashboard():
    allppl,allgame,allgroup,allrela = sql.getstatus()
    return render_template("dashboard.html",allppl=allppl,allgame=allgame,allgroup=allgroup,allrela=allrela)

@app.route("/add",methods=["POST"])
def add():
    m = request.form['data']
    sql.addvip(m)
    return '''{"msg":"OK"}'''

@app.route('/<steamid>',methods=["GET"])
def getsteam(steamid):
    m = sql.checkpersonstatus(steamid)
    if m == 0:
        return render_template("404.html")
    elif m==1:
        return render_template("vip.html")
    else:
        data = sql.getnode(steamid)
        gamedata = sql.getgamelist(steamid)
        groupdata = sql.getgrouplist(steamid)
        draft = sql.getdraft(steamid)
        intimacy = sql.getmostfamilar(steamid)
        person,relation = sql.nodelink(steamid)
        pbknow = sql.probablyknow(steamid)
        return render_template("steam.html",data=data,gamedata=gamedata,groupdata=groupdata,draftkey=[i[0] for i in draft],draftvalue=[i[1] for i in draft],intimacy=intimacy,person=person,relation=relation,pbknow=pbknow)

@app.route("/check",methods=["POST"])
def check():
    my = request.form['my']
    his = request.form['his']
    if sql.checkpersonstatus(his)>0 and sql.checkpersonstatus(my)>0:
        g = sql.friendchain(my, his)
        if g == []:
            return '''{"msg":1,"data":"在15度内找不到关系或者起始账户和结束账户相同！"}'''
        else:
            return json.dumps({"msg":0,"data":g})
    else:
        return '''{"msg":1,"data":"不好意思您输入的节点未收录！"}'''

if __name__ == '__main__':
    app.run(debug=True)