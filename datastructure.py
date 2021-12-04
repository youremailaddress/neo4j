from spiderfunc import *
import time
#todo 写push到数据库的接口，要字典类型、要空出来需要再考虑的部分

class Person:
    def __init__(self,profilesorid):
        self.steamid = None #是唯一profiles、不是自定义id(是str型的)
        self.level = [] #1
        self.oldname = [] #5
        self.loc = [] #2
        self.personaname = [] #3
        self.summary = [] #4 1-5都是列表[(内容，时间戳(int))]
        self.regestertime = None #字符串
        self.images = [] #纯列表
        self.id = profilesorid
    def fulfilled(self):
        a = PersonAll(self.id)
        perhaps = a.getsomeinfo()
        if perhaps == False:
            return False
        self.steamid,personaname,summary,level,_,loc = perhaps
        if personaname not in [i[0] for i in self.personaname]:
            self.personaname.append((personaname,str(int(time.time()))))
        if summary not in [i[0] for i in self.summary]:
            self.summary.append((summary,str(int(time.time()))))
        if level not in [i[0] for i in self.level]:
            self.level.append((level,str(int(time.time()))))
        if loc not in [i[0] for i in self.loc]:
            self.loc.append((loc,str(int(time.time()))))
        self.oldname.extend(a.getoldname())
        self.oldname = list(set(self.oldname))
        self.regestertime = a.getregestertime()
        self.images.extend(a.getimages())
        self.images = list(set(self.images))

    def getdata(self):
        data = {}
        data['id'] = self.id
        data['steamid'] = self.steamid
        data['level'] = self.level
        data['oldname'] = self.oldname
        data['loc'] = self.loc
        data['personaname'] = self.personaname
        data['summary'] = self.summary
        data['regestertime'] = self.regestertime
        data['images'] = self.images
        # data['isexpand'] = isexpand
        # data['updatetime'] = int(time.time())
        return data

class Group:
    def __init__(self):
        self.num = 0
        # self.members = []
        self.summary = []
        self.foundtime = ''
        self.language = ''
        self.region = ''

    def fulfilled(self,groupid,num):
        a = GroupAll(groupid)
        self.id = groupid
        self.num = num
        self.summary,self.foundtime,self.language,self.region = a.getsomeinfo()
        # self.members.extend(a.getgroupmember())
        # self.members = list(set(self.members))

    def getdata(self):
        data = {}
        data['id'] = self.id
        data['num'] = self.num
        data['summary'] = self.summary
        data['foundtime'] = self.foundtime
        data['language'] = self.language
        data['region'] = self.region
        # data['updatetime'] = int(time.time())
        return data

class Game:
    def __init__(self):
        self.appid = ''
        self.name = ''
        self.timestamp = 0
        self.tags = []

    def fulfilled(self,appid):
        a = GameAll(str(appid))
        self.appid,self.name,self.timestamp,self.tags = a.getsomething()
    
    def getdata(self):
        data = {}
        data['id'] = self.appid
        data['name'] = self.name
        data['timestamp'] = str(self.timestamp)
        data['tags'] = self.tags
        # data['updatetime'] = int(time.time())
        return data

class friend:
    def __init__(self,_id):
        self.id = _id
        self.friends = PersonAll(self.id).getfriends()

    def listfriends(self):
        return self.friends

    def generate(self):
        relation = []
        for friend in self.friends:
            relation.append(((self.id,friend),{"heatednum":0}))
        return relation

class play:
    def __init__(self,_id):
        self.id = _id
        a = PersonAll(_id)
        t = a.getAllgames()
        self.games = [i[0] for i in t]
        self.info = [{"forevertime":i[1],"lastplaytime":i[2]} for i in t]

    def listgames(self):
        return self.games
    
    def generate(self):
        relation = []
        for i in range(len(self.info)):
            relation.append(((self.id,self.games[i]),self.info[i]))
        return relation

class ingroup:
    def __init__(self,_id):
        self.id = _id
        a = PersonAll(_id)
        self.groups = a.getAllgroups()
        
    def listgroups(self):
        return [i[0] for i in self.groups]
    
    def generate(self):
        relation = []
        for i,_ in self.groups:
            relation.append(((self.id,i),{}))
        return relation
    def getnum(self,gr):
        for i,_ in self.groups:
            if i == gr:
                return _
        return 0
        

class comment:
    def __init__(self,_id):
        self.id = _id
        a = PersonAll(_id)
        a.getsomeinfo()
        a.getAllComments()
        self.comment = a.comments
        self.data = {}
        for i,j in self.comment:
            if self.data.get(i) != None:
                self.data[i].append(j)
            else:
                self.data[i] = [j]

    def listcommentsperson(self):
        return self.data.keys()
    
    def generate(self):
        relation = []
        for per,_ in self.data.items():
            relation.append(((self.id,per),{"pubtime":_}))
        return relation
