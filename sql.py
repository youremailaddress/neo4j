from py2neo import Node, Relationship,Graph,NodeMatcher,RelationshipMatcher,Subgraph
from datastructure import *
from spiderfunc import *
import time,math
from queue import Queue
import os

class SQL:
    def __init__(self):
        self.graph,self.match,self.rmatch = self.getconnect()
        
    def init(self):
        self.vipwait = Queue(maxsize=0)
        self.wait = Queue(maxsize=0)
        self.wait.put(("jianggua",False))

    def run(self):
        while True:
            try:
                self.getvip()
                if not self.vipwait.empty():
                    m,n = self.vipwait.get_nowait()
                else:
                    m,n = self.wait.get_nowait()
                print(m,n)
                if n!= True:
                    self.allhandle(m)
                else:
                    self.allhandle(m,force=True)
            except Exception as e:
                print(e.with_traceback())
                continue

    def getconnect(self):
        graph = Graph('http://localhost:7474', auth=("database","password"))
        match = NodeMatcher(graph)
        rmatch = RelationshipMatcher(graph)
        return graph,match,rmatch
    
    def checkid(self,_id,_type):
        a= self.graph.run('Match (n:{type}) where n["id"]=$_id return count(n)'.format(type=_type),parameters={"_id":_id}).data()[0]['count(n)']
        if a!=0:
            return True
        else:
            return False

    def checknode(self,node):
        nodetype = str(node.labels)[1:]
        nodeid = node.get("id")
        a = self.match.match(nodetype,id=nodeid)
        if len(a.all()) != 0:
            return a.first()
        else:
            return False

    def allhandle(self,_id,force=False):
        m = self.checkid(_id,"Id")
        if m != False and not force:#有、不强制
            return True
        elif m == False:#没有
            self.handleone(_id)
            self.batchaddnode([Node("Id",id=_id)], "Id")
        elif force:#有、强制
            self.handleone(_id)

    def batchcheck(self,lis,_type):#批量查找_type中没有id的lis中成员
        lis = list(lis)
        a= self.graph.run('Match (n:{type}) where n["id"] in $_id return n["id"]'.format(type=_type),parameters={"_id":lis}).data()
        rlis = lis[::]
        for i in a:
            rlis.remove(i['n["id"]'])
        return rlis

    def handleone(self,_id):
        ppl = Person(_id)
        if ppl.fulfilled() == False:
            return
        mynode = Node("Person",**ppl.getdata())
        print(mynode.items())
        nods = {_id:mynode}
        groupnods = {}
        gamesnods = {}
        fri = friend(_id)
        grop = ingroup(_id)
        games = play(_id)
        cmt = comment(_id)
        for frien in self.batchcheck(self.batchcheck(fri.listfriends(),"Id"),"Person"):#既不在Id结点里也不在person节点里
            m = Node("Person",id=frien)
            nods[frien] = m
        for cm in self.batchcheck(self.batchcheck(cmt.listcommentsperson(),"Id"),"Person"):
            m = Node("Person",id=cm)
            nods[cm] = m
            #简而言之，Id里是完全扩展的结点，Person里是扩展+涉及的结点，这里只添加没涉及的结点
        for gm in self.batchcheck(games.listgames(),"Game"):
            m = Game()
            m.fulfilled(gm)
            if m.appid == None:
                continue
            gamesnods[gm] = Node("Game",**m.getdata())
            #只添加没涉及的游戏
        for gr in self.batchcheck(grop.listgroups(), "Group"):
            m = Group()
            m.fulfilled(gr,grop.getnum(gr))
            groupnods[gr] = Node("Group",**m.getdata())
            #只添加没涉及的组 游戏和组涉及即扩展
        fn = list(nods.values())
        gm = list(gamesnods.values())
        gp = list(groupnods.values())
        self.batchaddnode(fn, "Person")
        self.batchaddnode(gm, "Game")
        self.batchaddnode(gp, "Group")
        self.batchaddrela(fri.generate(), "FRIENDS")
        self.batchaddrela(cmt.generate(), "COMMENTS")
        self.batchaddrela(games.generate(), "PLAY")
        self.batchaddrela(grop.generate(), "IN")
        for i in fri.listfriends():
            self.wait.put((i,False))
        print(11111)

    def batchaddnode(self,nodes,labels):
        appendlis = []
        pushlis = []
        for node in nodes:
            node['updatetime'] = str(int(time.time()))
            for k,v in node.items():
                if isinstance(v, list):
                    node[k] = [str(d) for d in v]
            m = self.checknode(node)
            if m != False:
                for k,v in node.items():
                    if labels == "Person" and k in ['level','oldname','loc','personaname','summary','images']:
                        #如果是person，要append更新的一些
                        if m.get(k) == None:#可能是未展开结点，m[k]没定义会报错
                            m[k] = []
                        m[k].extend(v)
                        if k == "images":
                            m[k] = list(set(m[k]))
                        else:
                            filtered = []
                            mark = []
                            for g in m[k]:
                                print(g)
                                t,_ = eval(g)
                                if t not in filtered:
                                    filtered.append(t)
                                    mark.append(g)
                            m[k] = mark
                        continue
                    m[k] = v
                pushlis.append(m)
            else:
                appendlis.append(node)
        s = Subgraph(appendlis)
        p = Subgraph(pushlis)
        self.graph.create(s)
        self.graph.push(p)    

    def checkrelationship(self,id1,id2,type1,type2,relationtype):
        a = self.graph.run("match (n:{type1})-[r:{rtype}]-(m:{type2}) where n['id'] = $id1 and m['id'] = $id2 return r".format(type1=type1,rtype=relationtype,type2=type2),parameters={"id1":id1,"id2":id2}).data()
        if len(a) == 0:
            return False
        a = a[0]['r']
        return a

    def fetchnode(self,_id,_type):
        a = self.graph.run("match (n:{type}) where n['id'] = $id return n".format(type=_type),parameters={"id":_id}).data()
        if len(a) == 0:
            return False
        else:
            return a[0]['n']

    def batchaddrela(self,lis,labels):
        appendlis = []
        pushlis = []
        type1 = "Person"
        if labels in ["FRIENDS","COMMENTS"]:
            type2 = "Person"
        if labels == "PLAY":
            type2 = "Game"
        if labels == "IN":
            type2 = "Group"
        for item in lis:
            dic,kwargs = item
            kwargs['updatetime'] = str(int(time.time()))
            a = self.checkrelationship(dic[0], dic[1], type1, type2, labels)
            if a != False:
                for k,v in kwargs.items():
                    a[k] = v
                a["updatetime"] = str(int(time.time()))
                pushlis.append(a)
            else:
                m = self.fetchnode(dic[0], type1)
                n = self.fetchnode(dic[1], type2)
                # print(m,n,dic,type1,type2)
                if m == False or n== False:
                    continue
                r = Relationship(m,labels,n,**kwargs)
                appendlis.append(r)
        s = Subgraph(relationships=appendlis)
        p = Subgraph(relationships=pushlis)
        self.graph.create(s)
        self.graph.push(p)

    def getstatus(self):
        # expandednum = self.graph.run("Match (n:Id) return count(n)").data()[0]['count(n)']
        allpplnum = self.graph.run("Match (n:Person) return count(n)").data()[0]['count(n)']
        gamenum = self.graph.run("Match (n:Game) return count(n)").data()[0]['count(n)']
        groupnum = self.graph.run("Match (n:Group) return count(n)").data()[0]['count(n)']
        relanum = self.graph.run("Match ()-[r]-() return count(r)").data()[0]['count(r)']
        return allpplnum,gamenum,groupnum,relanum
    
    def checkpersonstatus(self,_id):
        a = self.graph.run("Match (n:Person) where n.id=$id return n",parameters={'id':_id}).data()
        if len(a) == 0:
            return 0 #如果没被涉及，返回0
        else:
            b = self.graph.run("Match (n:Id) where n.id=$id return n",parameters={'id':_id}).data()
            if len(b) == 0:
                return 1#如果只是被涉及，返回1
            return 2#如果完全展开，返回2

    def addvip(self,_id):
        # self.vipwait.put((_id,True))
        try:
            with open("1.txt",'a') as f:
                f.write(_id+"\n")
        except:
            pass
    
    def getvip(self):
        try:
            with open("1.txt","r") as f:
                a = f.readlines()
            os.remove("./1.txt")
            for i in a:
                self.vipwait.put_nowait((i.strip(),True))
        except FileNotFoundError:
            pass
        
    def getnode(self,_id):
        a = self.graph.run("match (n:Person) where n.id=$id return n",parameters={"id":_id}).data()[0]['n']
        data = {}
        data["steamid"] = a.get("steamid") if a.get("steamid") != None else ""
        data["oldname"] = [(eval(i)[0],int(eval(i)[1])) for i in a.get("oldname")] if a.get("oldname") != None else []
        data["loc"] = [(eval(i)[0],int(eval(i)[1])) for i in a.get("loc")] if a.get("loc") != None else []
        data["images"] = a.get("images") if a.get("images")!=None else []
        data['level'] = [(int(eval(i)[0]),int(eval(i)[1])) for i in a.get("level")] if a.get("level")!=None else []
        data['id'] = a.get("id") if a.get("id")!=None else ""
        data["personaname"] = [(eval(i)[0],int(eval(i)[1])) for i in a.get("personaname")] if a.get("personaname")!= None else []
        data["updatetime"] = int(a.get("updatetime")) if a.get("updatetime")!= None else 0
        data["regestertime"] = a.get("regestertime") if a.get("regestertime") != None else ""
        data["summary"] = [(eval(i)[0],int(eval(i)[1])) for i in a.get("summary")] if a.get("regestertime")!= None else []
        return data

    def getdraft(self,_id):
        data = {}
        for m in self.graph.run("match (n:Person)-[r:PLAY]-(m:Game) where n.id=$id return r.forevertime,m.tags",parameters={"id":_id}).data():
            if m["r.forevertime"] != 0:
                for t in m["m.tags"]:
                    if t not in data.keys():
                        data[t] = m["r.forevertime"]
                    else:
                        data[t] += m["r.forevertime"]
        sigma = sum(data.values())
        for k,v in data.items():
            data[k] = v/sigma
        data = sorted(data.items(),key =lambda kv:kv[1],reverse=True)
        return data

    def getgamelist(self,_id):
        a = self.graph.run("match(n:Person)-[r:PLAY]-(m) where n.id=$id return m.name,m.id",parameters={"id":_id}).data()
        return a

    def getgrouplist(self,_id):
        a = self.graph.run("match(n:Person)-[r:IN]-(m) where n.id=$id return m.num,m.id",parameters={"id":_id}).data()
        return a

    def getfriends(self,_id):
        lis = []
        for i in self.graph.run("match(n:Person)-[r:FRIENDS]-(m) where n.id=$id return m.id",parameters={"id":_id}).data():
            lis.append(i["m.id"])
        return lis
        
    def dotmutiply(self,list1,list2):
        assert len(list1) == len(list2)
        return sum([list1[i]*list2[i] for i in range(len(list1))])
            
    def distance(self,list1):
        return math.sqrt(self.dotmutiply(list1, list1))

    def getmostfamilar(self,_id):
        '''同款游戏+(m)*(时间内积)
           每条留言+2
           同个群组+(1-groupnum/1000)
        '''
        friendlis = self.getfriends(_id)
        dic = {}
        gm = {}
        for i in friendlis:
            dic[i] = 0
        for i in self.graph.run("match (n:Person)-[r:FRIENDS]-(m:Person),(n:Person)-[r1:COMMENTS]-(m:Person) where n.id=$id return m.id,count(r1.pubtime)",parameters={"id":_id}).data():
            dic[i['m.id']] += 2*i['count(r1.pubtime)']
        for i in self.graph.run("match (n:Person)-[r:FRIENDS]-(m:Person)-[r1:IN]-(G:Group)-[r2:IN]-(n:Person) where n.id=$id return G.num,m.id",parameters={"id":_id}).data():
            dic[i['m.id']] += (2-i['G.num']/1000) if i['G.num'] < 1000 else 0
        for i in self.graph.run("match (n:Person)-[r:FRIENDS]-(m:Person)-[r1:PLAY]-(G:Game)-[r2:PLAY]-(n:Person) where n.id=$id and r1.forevertime<>0 and r2.forevertime<>0 return r1.forevertime,r2.forevertime,m.id",parameters={"id":_id}).data():
            if i['m.id'] not in gm.keys():
                gm[i['m.id']] = [[i['r2.forevertime']],[i['r1.forevertime']]]
            else:
                gm[i['m.id']][0].append(i['r2.forevertime'])
                gm[i['m.id']][1].append(i['r1.forevertime'])
        for k,v in gm.items():
            dotnorm = self.dotmutiply(v[0],v[1])/(self.distance(v[0])*self.distance(v[1]))
            dic[k] += len(v[0])*dotnorm
        data = sorted(dic.items(),key =lambda kv:kv[1],reverse=True)
        data = data[:10]
        data = [(i[0],i[1]) for i in data if i[1] != 0 ]
        return data

    def probablyknow(self,_id):
        a = self.graph.run("match (n:Person)-[r:FRIENDS]-(m:Person)-[r1]-(p:Person) where n.id=$id and not (n)-[:FRIENDS]-(p) and (n)-[:PLAY|IN*2]-(p) return not p.id <> p.steamid,p.id",parameters={"id":_id}).data()
        return [i.values() for i in a]

    def randomselect(self):
        _id = self.graph.run("match (n:Id) return n,rand() as r Order by r limit 1").data()[0]['n'].get("id")
        return _id
    
    def nodelink(self,_id):
        m = self.graph.run('''match (n:Person)-[r1:FRIENDS|COMMENTS*1..2]-(m:Person)
                where n.id=$id
                with r1,n,m,m as e
                match (m)-[r2:FRIENDS|COMMENTS*1..2]-(e)
                with m,r1,r2,reduce(temp=null,data in r2 | data) as label2,reduce(temp=null,data in r1 | data) as label1
                WITH collect(label1)+collect(label2) as nodez
                UNWIND nodez as label
                match (p1)-[label]-(p2)
                return distinct p1.id,type(label),p2.id''',parameters={"id":_id}).data()
        person = []
        check = []
        returnlis = []
        for i in m:
            if i["p1.id"] not in person:
                person.append(i["p1.id"])
            if i["p2.id"] not in person:
                person.append(i["p2.id"])
            if set(i.values()) not in check:
                check.append(set(i.values()))
                returnlis.append(i)
        return person,returnlis

    def friendchain(self,id1,id2):
        if id1 == id2:
            return []
        m = self.graph.run('''MATCH p = ShortestPath((m:Person)-[:FRIENDS*..15]-(n:Person))
            WHERE m.id = $my AND n.id = $his
            RETURN nodes(p)''',parameters={"my":id1,"his":id2}).data()
        if len(m) == 0:
            return []
        return [(i['id'],int(i['id']==i['steamid'])) for i in m[0]['nodes(p)']]
        
if __name__ == '__main__':
    a = SQL()
    a.init()
    a.run()

