# coding: utf-8
'''
Created on 2018年8月19日

@author: root
'''
from http_client import  HttpClient

from xml.dom import minidom
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import re,os
class UbuntuKylin(object):
    def __init__(self,username,password,loginfield='email'):
        self.Clint=HttpClient()
        self.cookietime='2592000'
        self.seccodemodid='member::logging'
        self.questionid=0
        self.answer=''
        self.idhash=''
        self.loginfield=loginfield
        self.username=username
        self.password=password
        self.seccodeverify=''
        self.loginhash=''
        self.rooturl='https://www.ubuntukylin.com/ukylin/'
        self.formhash=''
        self.logined=False
    def _login_by_cookie(self):
        self.Clint.load_cookie()
        html=pq(self.Clint.get('https://www.ubuntukylin.com/ukylin/forum.php'))
        if len(html('#lsform'))==0:
            return True
    def login(self):
        if not self._login_by_cookie():
            self.Clint.get('https://www.ubuntukylin.com/ukylin/forum.php')
            self.Clint.get('https://www.ubuntukylin.com/ukylin/home.php?mod=misc&ac=sendmail')
            
            req=self.Clint.get('https://www.ubuntukylin.com/ukylin/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login')
            
            self._loadxml(req)
            self.Clint.download('https://www.ubuntukylin.com/ukylin/misc.php?mod=seccode&idhash='+self.idhash, 'code.png')
            code_file_path=os.path.join(os.getcwd(),'code.png')
            # os.system("feh %s &"%code_file_path)
            self.seccodeverify=input('请输入验证码：')
            code=self.Clint.get(
                'https://www.ubuntukylin.com/ukylin/misc.php?mod=seccode&action=check&inajax=1&modid=member::logging&idhash='+self.idhash+'&secverify='+self.seccodeverify)
            if code.find('succeed') ==-1:
                return False
            params={
                'mod':'logging',
                'action':'login',
                'loginsubmit':'yes',
                'handlekey':'login',
                'loginhash':self.loginhash,
                'inajax':'1'
                }
            data={'formhash':self.formhash,
                  'referer':'https://www.ubuntukylin.com/ukylin/forum.php',
                  'loginfield':self.loginfield,
                  'username':self.username,
                  'password':self.password,
                  'questionid':self.questionid,
                  'answer':'',
                  'seccodehash':self.idhash,
                  'seccodemodid':self.seccodemodid,
                  'seccodeverify':self.seccodeverify,
                  'cookietime':self.cookietime
            }
            if self.Clint.post(self.rooturl+'member.php', data,params).find('succeedhandle_login')!=-1:
                self.logined=True
        else:
            self.logined=True
    def _loadxml(self,xmltext):
        dom=minidom.parseString(xmltext)
        cdata=dom.firstChild.childNodes[0].wholeText
        html=pq(cdata)
        self.loginhash= html("[name=login]").attr('id').split('_')[-1]
        self.idhash=html("[name=login] div span[id]").attr('id').split('_')[-1]
        self.formhash=html("[name=login] [name=formhash]").attr('value')
    def qiandao(self):
        if not self.logined:
            print('尚未登录，请登录')
            return None
        dom=minidom.parseString(self.Clint.get('https://www.ubuntukylin.com/ukylin/plugin.php?id=dsu_paulsign:sign&infloat=yes&handlekey=dsu_paulsign&inajax=1&ajaxtarget=fwin_content_dsu_paulsign'))
        cdata=dom.firstChild.childNodes[0].wholeText
        # html=BeautifulSoup(cdata,"html5lib")
        # if html.find('h1',text='您今天已经签到过了或者签到时间还未开始') !=None:
        #     print('今日已签到')
        #     return
        # formhash=html.find('input',{'name':"formhash"})['value']
        # print(cdata)
        html=pq(cdata)
        if html('h1').text()=="您今天已经签到过了或者签到时间还未开始":
            print("今日已签到")
            return
        formhash=html('[name=formhash]').attr('value')
        if self.Clint.post(self.rooturl+'plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1', {'formhash':formhash,'qdxq':'kx','qdmode':'3','fastreply':'0','todaysay':''}).find('签到成功')!= -1:
            print('签到成功')
            return