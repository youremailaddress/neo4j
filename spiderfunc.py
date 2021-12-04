import requests
import random,re,time,datetime,json

class Util:
    def __init__(self):
        self.retrytime = 5

    def randomua(self):
        lis = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
            "Opera/8.0 (Windows NT 5.1; U; en)",
            "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
            "MAC：Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
            "Windows：Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)"
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
            "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
            "UCWEB7.0.2.37/28/999",
            "NOKIA5700/ UCWEB7.0.2.37/28/999",
            "Openwave/ UCWEB7.0.2.37/28/999",
            "Openwave/ UCWEB7.0.2.37/28/999",
            ]
        return random.choice(lis)

    def headers(self,**kwargs):
        a =  {
            'User-Agent':self.randomua(),
            'Content-Encoding':'gzip'
        }
        for k,v in kwargs.items():
            k.replace('_', '-')
            a[k] = v
        return a

    def proxies(self):
        return {'http':'127.0.0.1:10809','https':'127.0.0.1:10809'}

    def tryexcept(self,fuc,defaultreturn=[]):
        for i in range(self.retrytime):
            try:
                # print(i,fuc.__name__)
                return fuc()
            except Exception as e:
                if isinstance(e, UnicodeEncodeError):
                    continue
                print(str(e))
                continue
        return defaultreturn

class PersonAll(Util):
    def __init__(self,profilesorid):
        '''
        type:str
        这里有可能是64位数字profiles，也有可能是自定义id，需要另写一个方法判断
        '''
        super().__init__()
        ispro = self.checkisprofiles(profilesorid)
        # print(ispro)
        self.profileurl = "https://steamcommunity.com/"+("profiles/" if ispro else "id/")+profilesorid
        self.steamid = None
        self.i = 0
        self.count = None
        self.comments = []

    def _getsomeinfo(self):
        '''(None,None,None,None,None,None)'''
        req = requests.get(self.profileurl,headers=self.headers(Accept_Language='zh-CN,zh;'),proxies=self.proxies())
        if "The specified profile could not be found." in req.text:
            return False
        if "This profile is private" in req.text:
            return False
        steamid = re.findall('","steamid":"(.*?)",', req.text)
        print(steamid)
        if len(steamid) >= 1:
            steamid = steamid[0]
        else:
            steamid = None
        personaname = re.findall('","personaname":"(.*?)",', req.text)
        if len(personaname) >= 1:
            personaname = personaname[0]
        else:
            personaname = None
        summary = re.findall('","summary":"(.*?)"};', req.text)
        if len(summary) >= 1:
            summary = summary[0]
        else:
            summary = None
        level = re.findall('<span class="friendPlayerLevelNum">(.*?)</span>', req.text)
        if len(level) >= 1:
            level = level[0]
        else:
            level = None
        name = re.findall('<bdi>(.*?)</bdi>', req.text)
        if len(name) >= 1:
            name = name[0]
        else:
            name = None
        loc = re.findall(b'\r\n\t\t\t\t\t\t\t\t\t\t\t\t(.*?)\t\t\t\t\t',req.content)
        loc = [i for i in loc if i != b'']
        if len(loc) >= 1:
            loc = loc[0].decode("utf-8")
        else:
            loc = None
        self.steamid = steamid
        return steamid,personaname,summary,level,name,loc
        
    def handletime(self,tim):
        t = tim.split(" ")
        try:
            monthlis = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            month = monthlis.index(t[0])+1
            day = int(t[1][:-1]) if "," in tim else int(t[1])
            year = datetime.datetime.today().year if "," not in tim else int(t[2])
            hours = int(t[-1][:-2].split(":")[0])%12 if t[-1][-2] == "a" else int(t[-1][:-2].split(":")[0])%12 + 12
            minutes = int(t[-1][:-2].split(":")[1])
        except:
            return 0
        return int(datetime.datetime(year, month, day,hours,minutes,0,0).timestamp())
        
    def _getoldname(self):
        '''[]'''
        req = requests.post(self.profileurl+"/ajaxaliases/",headers=self.headers(Accept_Language="en-US,en;"),proxies={'http':'127.0.0.1:10809','https':'127.0.0.1:10809'})
        lis = eval(req.text)
        for i in range(len(lis)):
            lis[i]['timechanged'] = self.handletime(lis[i]['timechanged'])
        lis = [(i['newname'],str(i['timechanged'])) for i in lis]
        return lis

    def checkisprofiles(self,profilesorid):
        if len(profilesorid)!=17:
            return False
        elif profilesorid[:4] == "7656":
            try:
                pro = int(profilesorid)
                return True
            except:
                return False
        else:
            return False

    def _getfriends(self):
        '''[]'''
        url = self.profileurl + "/friends/"
        req = requests.get(url,headers=self.headers(),proxies=self.proxies())
        _id = []
        _id.extend(re.findall('" href="https://steamcommunity.com/id/(.*?)">', req.text))
        _id.extend(re.findall('" href="https://steamcommunity.com/profiles/(.*?)">', req.text))
        return _id
        
    def _getimages(self):
        '''[]'''
        url = self.profileurl + "/images/"
        req = requests.get(url,headers=self.headers(),proxies=self.proxies())
        imagesid = []
        imagesid.extend(re.findall(r'href="https://steamcommunity.com/sharedfiles/filedetails/\?id=(.*?)"', req.text))
        return imagesid

    def _getregestertime(self):
        '''Some error occured'''
        url = self.profileurl + "/badges/1"
        req = requests.get(url,headers=self.headers(),proxies=self.proxies(),allow_redirects=False)
        if req.status_code != 200:
            return "Member in a year or is protected."
        return re.findall('class="badge_description">\r\n\t\t\t\t\t\t(.*?)\t\t\t\t\t</div>', req.text)[0]

    def _getAllgroups(self):
        '''[]'''
        url = self.profileurl + "/groups/"
        req = requests.get(url,headers=self.headers(),proxies=self.proxies())
        grouplis = []
        grouplis.extend(re.findall("https://steamcommunity.com/groups/(.*?)/members",req.text))
        memberlis = []
        memberlis.extend(re.findall('/members">(.*?)</a>',req.text))
        memberlis = [int("".join(i.split(" ")[0].split(","))) for i in memberlis]
        return list(zip(grouplis,memberlis))

    def _getAllgames(self):
        '''[]'''
        url = self.profileurl + '/games/?tab=all'
        req = requests.get(url,headers=self.headers(),proxies=self.proxies())
        gamelis = []
        game = re.findall('var rgGames = (.*?)}];',req.text)
        if len(game) == 0:
            return []
        else:
            game = game[0]
        game = json.loads('{"data":'+game+'}]}')
        for item in game['data']:
            if item.get('hours_forever') == None:
                gamelis.append((item['appid'],0,0))
                continue
            gamelis.append((item['appid'],float("".join(item['hours_forever'].split(","))),item['last_played']))
        return gamelis

    def _getComments(self):
        # if self.count != None and self.i > self.count:
        #     raise Warning
        if self.steamid == None:
            return None
        req = requests.post("https://steamcommunity.com/comment/Profile/render/"+self.steamid+"/-1/?start=%d" % self.i,headers=self.headers(),proxies=self.proxies())
        a = req.json()
        # print(req.status_code)
        if a['success'] == "false":
            return
        if self.count == None:
            self.count = a['total_count']
        # print(re.findall('commentthread_author_link\" href=\"https:\/\/steamcommunity.com\/(id|profiles)\/(.*?)\"',a['comments_html']))
        profileid = [i[1] for i in re.findall('commentthread_author_link\" href=\"https:\/\/steamcommunity.com\/(id|profiles)\/(.*?)\"',a['comments_html'])]
        stamp = [int(i) for i in re.findall('data-timestamp=\"(.*?)\"', a['comments_html'])]
        self.comments.extend(list(zip(profileid,stamp)))
    
    def getAllComments(self):
        while True:
            self.tryexcept(self._getComments,defaultreturn=None)
            if self.i > self.count:
                self.i = 0
                break
            self.i += 10

    def getsomeinfo(self):
        return self.tryexcept(self._getsomeinfo,defaultreturn=(None,None,None,None,None,None))
    
    def getoldname(self):
        return self.tryexcept(self._getoldname)

    def getfriends(self):
        return self.tryexcept(self._getfriends)

    def getimages(self):
        return self.tryexcept(self._getimages)

    def getregestertime(self):
        return self.tryexcept(self._getregestertime,defaultreturn="Some error occured")

    def getAllgroups(self):
        return self.tryexcept(self._getAllgroups)

    def getAllgames(self):
        return self.tryexcept(self._getAllgames)

class GroupAll(Util):
    def __init__(self,groupid):
        super().__init__()
        self.groupurl = "https://steamcommunity.com/groups/"+groupid
        
    def _getsomeinfo(self):
        '''(None,None,None,None)'''
        req = requests.get(self.groupurl,headers=self.headers(),proxies=self.proxies())
        summary = re.findall('<meta name="Description" content="(.*?)>', req.text)
        if len(summary) == 0:
            summary = []
        else:
            summary = summary[0]
        foundtime = re.findall('<div class="data">(.*?)</div>\r\n', req.text)
        if len(foundtime) == 0:
            foundtime = []
        else:
            foundtime = foundtime[0]
        language = re.findall('<div class="data">(.*?)</div>\r\n', req.text)
        if len(language) < 2:
            language = []
        else:
            language = language[1]
        region = re.findall('<div class="data">(.*?)&nbsp;', req.text)
        if len(region) == 0:
            region = []
        else:
            region = region[0]
        return (summary,foundtime,language,region)

    def _getgroupmember(self):
        '''[]'''
        url = self.groupurl+"/members/"
        req2 = requests.get(url,headers=self.headers(),proxies=self.proxies())
        memberlist = []
        memberlist.extend(re.findall('<a class="linkFriend" href="https://steamcommunity.com/id/(.*?)"', req2.text))
        memberlist.extend(re.findall('<a class="linkFriend" href="https://steamcommunity.com/profiles/(.*?)"', req2.text))
        return memberlist

    def getsomeinfo(self):
        return self.tryexcept(self._getsomeinfo,defaultreturn=(None,None,None,None))
    
    def getgroupmember(self):
        return self.tryexcept(self._getgroupmember)

class GameAll(Util):
    def __init__(self,appid):
        super().__init__()
        self.appid = appid
        self.url = 'https://store.steampowered.com/broadcast/ajaxgetbatchappcapsuleinfo?appids='+appid+'&cc=US&l=schinese&origin=https:%2F%2Fstore.steampowered.com'

    def _getsomething(self):
        '''(None,None,None,None)'''
        req = requests.get(self.url,headers=self.headers(),proxies=self.proxies())
        smthing = req.json()
        # print(smthing,self.url)
        if len(smthing['apps']) == 0:
            req = requests.get('https://store.steampowered.com/broadcast/ajaxgetbatchappcapsuleinfo?appids='+self.appid+'&cc=CN&l=schinese&origin=https:%2F%2Fstore.steampowered.com',headers=self.headers(),proxies=self.proxies())
            smthing = req.json()
            if len(smthing['apps']) == 0:
                return (self.appid,"","",[])
        appid = smthing['apps'][0]['appid']
        title = smthing['apps'][0]['title']
        releasedate = smthing['apps'][0]['rt_release_date']
        tags = []
        for item in smthing['apps'][0]['tags']:
            tags.append(item['name'])
        return (appid,title,releasedate,tags)

    def getsomething(self):
        return self.tryexcept(self._getsomething,defaultreturn=(None,None,None,None))
