# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from contextlib import closing
import requests
import xlwt
import xlrd
from xlutils.copy import copy
import urllib
import urllib2
import os
from common import *
from gevent import monkey;monkey.patch_all()
import gevent


import re
import shutil
import random
import sys
import urllib
import hashlib
import logging

def access(url,date):    

    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    #代理记得要挂上
    prox.http_proxy = "http://proxy.****.com:10086"
    prox.ssl_proxy = "http://proxy.****.com:10086"
    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=options,desired_capabilities=capabilities)
   
    
    driver.get(url)
  
    js="var q=document.documentElement.scrollTop=1000000"
    
    for i in range(0,40):     
        driver.execute_script(js)
        time.sleep(4)

    html = driver.page_source
    content = BeautifulSoup(html, 'html.parser')
    div=content.find(name="div",attrs={"class":"_7jjx"})
    div_list=div.find_all(name="div",attrs={"class":"_7owt"})
    print "%s 总广告数是: %d"%(all_date,len(div_list))
    filter_list=[] 
    for div in div_list:
        advertise_date=div.find(name="div",attrs={"class":"_7jwu"}).span.text
        if advertise_date == date:
            filter_list.append(div)  
    print "%s 广告数是 %d"%(date,len(filter_list)) 
    

    return filter_list
    

def download_file(div,path,id):
    video=div.find(name="video")
    path=path+id+"-.mp4"
    if video != None:
        try:
            print "start rm {}-.img".format(id)
            os.remove("{}/{}/{}/{}-.jpg".format(mount_point,keyword,all_date,id))
        except OSError as e:
            print e
        video_src=video.get("src")
        with closing(requests.get(video_src, stream=True)) as r:
            chunk_size = 1024*10
            content_size = int(r.headers['content-length'])
            print '下载开始'
            with open(path, "wb") as f:
               # p = ProgressData(size = content_size, unit='Kb', block=chunk_size)
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                #    p.output()
            print "下载完成"
 
 
def convert(str): 
    return int("".join(re.findall("\d*", str)))

class ProgressData(object):
 
    def __init__(self, block,size, unit, file_name='', ):
        self.file_name = file_name
        self.block = block/1000.0
        self.size = size/1000.0
        self.unit = unit
        self.count = 0
        self.start = time.time()
    def output(self):
        self.end = time.time()
        self.count += 1
        speed = self.block/(self.end-self.start) if (self.end-self.start)>0 else 0
        self.start = time.time()
        loaded = self.count*self.block
        progress = round(loaded/self.size, 4)
        if loaded >= self.size:
            print u'%s下载完成\r\n'%self.file_name
        else:
            pass
            print u'{0}下载进度{1:.2f}{2}/{3:.2f}{4} 下载速度{5:.2%} {6:.2f}{7}/s'.\
                  format(self.file_name, loaded, self.unit,\
                  self.size, self.unit, progress, speed, self.unit)
            print '%50s'%('/'*int((1-progress)*50))


def imageDownload(div,id):
   
    video=div.find(name="video") 
    
    if video != None:
        imgurl=video.get("poster")
        
    else:
        imgurl=div.find(name="img",attrs={"class":"_7jys img"})
        if imgurl==None:
            imgurl=div.find(name="img",attrs={"class":"_7jys _7jyt img"})
        imgurl=imgurl.get("src")

    urllib.urlretrieve(imgurl, "/%s/%s/%s.jpg"%("facebook","all",id))


def textInfo(div_list,keyword):
    
    text_id=os.listdir(path)[0]
    text_id=int(text_id)
    text_list=[]
    for div in div_list:

        dlist=[]
        

        date=div.find(name="div",attrs={"class":"_7jwu"}).span.text     
        theme=div.find(name="div",attrs={"class":"_7jyr"})
        theme=theme.find(name="div",attrs={"class":"_4ik4 _4ik5"}).text
        
        
        for root,dirs,files in os.walk("/facebook/patch3"):
           
           # print "/facebook/patch3:{}".format(files)
            if files==[]:
                link=str(text_id)+"-"+keyword
            for file in files:
                if file.split(".")[1] == str(text_id):
                
                    link="{}-{}".format(file.split(".")[0],keyword)
                   
                    break
                else:
                    
                    link=str(text_id)+"-"+keyword
        
              
        dlist.append(date)
        dlist.append(keyword.decode("utf-8"))
        dlist.append(link.decode("utf-8"))
        dlist.append(theme)
        text_list.append(dlist)

        text_id=text_id+1
    print "文本信息提取完成 删除/facebook/patch3"
    shutil.rmtree('/facebook/patch3')
    os.mkdir('/facebook/patch3')

    return text_list

def occurence_textcontent(row,div_list,fileName,text_list):

    dlist={}
    for text in text_list:

        theme=text[3]

        if theme not in dlist:
            dlist[theme]=1
        else:
            dlist[theme]=dlist[theme]+1

    
    readbook = xlrd.open_workbook(fileName, formatting_info=True)
    workbook = copy(readbook)
   
    rdata_sheet = readbook.sheets()[1]
    content_list=rdata_sheet.col_values(1)
    workbook = copy(readbook)
    wdata_sheet=workbook.get_sheet(1)


    for key,value in dlist.items():
            if key in content_list:
                    id=content_list.index(key)
                    num=rdata_sheet.cell(id,2).value
                    wdata_sheet.write(id,2,value+num)
            else:
                 wdata_sheet.write(row,0,keyword.decode("utf-8"))
                 wdata_sheet.write(row,1,key)
                 wdata_sheet.write(row,2,value)
                 row=row+1
    workbook.save(fileName)

def occurence_liblary(row,div_list,fileName,text_list):

    dlist={}
    for text in text_list:
        link=text[2]
       
        if link not in dlist:
            dlist[link]=1
        else:
            dlist[link]=dlist[link]+1
        
    
    readbook = xlrd.open_workbook(fileName, formatting_info=True)
    workbook = copy(readbook)

    rdata_sheet = readbook.sheets()[2]
    content_list=rdata_sheet.col_values(1)
    workbook = copy(readbook)
    wdata_sheet=workbook.get_sheet(2)


    for key,value in dlist.items():
            if key in content_list:
                    id=content_list.index(key)
                    num=rdata_sheet.cell(id,2).value
                    wdata_sheet.write(id,2,value+num)
            else:
                 wdata_sheet.write(row,0,keyword.decode("utf-8"))
                 wdata_sheet.write(row,1,key)
                 wdata_sheet.write(row,2,value)
                 row=row+1
    workbook.save(fileName)

def exportExecl(row,allInfoList,fileName):  
    print "excel 第{}行插入数据".format(row)
    readbook = xlrd.open_workbook(fileName, formatting_info=True)
    workbook = copy(readbook)
    data_sheet = workbook.get_sheet(0)
    for infolist in allInfoList:
        for column in range(0,4):
            # print type(infolist[column]),infolist[column]
            data_sheet.write(row,column,infolist[column])
        row=row+1
    workbook.save(fileName)

def createExecel(fileName):
    init1 = ['日期','游戏名','素材id','文案']
    init2 = ['游戏名','文案','出现次数']
    init3 = ['游戏名','素材id','出现次数']
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet1 = workbook.add_sheet('product')
    worksheet2 = workbook.add_sheet('document')
    worksheet3 = workbook.add_sheet('liblary')
    
    for i in range(len(init)):
        worksheet1.write(0,i,init1[i])
    for i in range(len(init)):
        worksheet2.write(0,i,init2[i])
    for i in range(len(init)):
        worksheet3.write(0,i,init3[i])

    workbook.save(fileName)

    
def read_excel(fileName):

    wb = xlrd.open_workbook(filename=fileName)

    sheet1 = wb.sheet_by_index(0)
    sheet2 = wb.sheet_by_index(1)
    sheet3 = wb.sheet_by_index(2)
    # print(sheet1.name,sheet1.nrows,sheet1.ncols)
    return sheet1.nrows,sheet2.nrows,sheet3.nrows
    # rows = sheet1.row_values(sheet1.nrows-1)#获取行内容
    # if rows != []:
    #     return sheet1.nrows
    # else:
    #     sys.exit()
   

    

def createDir(keyword,date):
    keyword_path="/mnt/gallery/{}/{}".format(keyword,date)
    path=os.path.abspath(keyword_path)
    if os.path.exists(path):
        print "directory is exists"
    else:
        os.mkdir("/mnt/gallery/{}".format(keyword))
        os.mkdir(keyword_path)


def get_md5_value(src):
        #调用hashlib里的md5()生成一个md5 hash对象
        myMd5 = hashlib.md5()
        #生成hash对象后，就可以用update方法对字符串进行md5加密的更新处理
        myMd5.update(src)
        #加密后的十六进制结果
        myMd5_Digest = myMd5.hexdigest()
        #返回十六进制结果
        return myMd5_Digest


def md5_pool(keyword):
        pool={}

        if os.path.exists("/facebook/patch1/{}".format(keyword)):
            pass
        else:
            os.mkdir("/facebook/patch1/{}".format(keyword))
        for root, dirs, files in os.walk("/facebook/patch1/{}".format(keyword)):
            files.sort(key=convert)
            for file_name in files:
                    filepath = "%s/%s"%(root,file_name)
                    with open(filepath,"rb") as fobj:
                        code = fobj.read()

                    md5_v = get_md5_value(code)
                    pool[md5_v] = file_name
        return pool
                        
            
        
def deduplicate(keyword):

        MD5_POOL=md5_pool(keyword)
        print "MD5 pool的值为：{}".format(MD5_POOL)
        for FROM_FOLDER in FROM_FOLDER_LIST:
                for root, dirs, files in os.walk(FROM_FOLDER):
                        files.sort(key=convert)
                        print "/facebook/all 下的文件为：{}".format(files)
                        for file_name in files:
                                filepath = "%s/%s"%(root,file_name)
                                print "扫描文件  ",filepath
                                
                                try:
                                       
                                        with open(filepath,"rb") as fobj:
                                               
                                                code = fobj.read()
                                      
                                        md5_v = get_md5_value(code)
                                      
                                        if not md5_v in MD5_POOL:
                                                print "移动文件 %s 到目录 %s下"%(filepath,TARGET_FOLDER)
                                                shutil.copy(filepath, "%s/%s"%("/facebook/patch1",keyword))
                                                #文件以-结尾
                                                ad_filename=file_name.split(".")[0]+"-.jpg"
                                                shutil.move(filepath, "%s/%s"%(TARGET_FOLDER,ad_filename))
                                                
                                                MD5_POOL[md5_v] = file_name
                                        else:
                                               
                                                file_name= MD5_POOL[md5_v].split(".")[0]+"."+file_name
                                                print "%s 是重复文件， 移动到目录 %s下"%(filepath,TARGET_FOLDER2)
                                                shutil.move(filepath, "%s/%s"%(TARGET_FOLDER2,file_name))
                                except Exception,err:
                                        print err
                                        print "copy file %s error"%filepath
                                        continue




if __name__ == '__main__':
    
    for keyword in keywordDict.keys():
        print keyword
        

        path="/facebook/{}".format(keyword)
        if os.path.exists(path):
                print "directory is exists"
        else:
            os.mkdir(path)
            os.mknod("{}/1".format(path))
           
        createDir(keyword,all_date)
        
        div_list=access(keywordDict[keyword],date)
        if div_list == []:
            print "没有符合条件的广告"
            continue

        id=int(os.listdir(path)[0])
        jobs=[]
        text_list=[]
        print "%s 初始id为%d"%(date,id)
        for div in div_list:
           #  imageDownload(div,id)
           #  id=id+1
            jobs.append(gevent.spawn(imageDownload,div,id))
            id=id+1
        gevent.joinall(jobs)
        
       
        #hash去
        FROM_FOLDER_LIST=["/facebook/all",]
        # 去重后的目录
        TARGET_FOLDER="{}/{}/{}/".format(mount_point,keyword,all_date)
        #重复文件的目录
        TARGET_FOLDER2="/facebook/patch3"
        print "开始去重："
        deduplicate(keyword)
         

        for root,dirs,files in os.walk(TARGET_FOLDER):

            files.sort()
            print "{} 下的文件： {}".format(TARGET_FOLDER,files)
            for file in files:

                files_id=file.split("-")[0]
                

                if int(files_id) >= int(os.listdir(path)[0]):
                 
                  div=div_list[int(files_id)-int(os.listdir(path)[0])]
                  download_file(div,TARGET_FOLDER,files_id)
            break

        
    # #     #text downlaod
        text_list=textInfo(div_list,keyword)
        
        fileName="{}/2019-08-ad.xls".format(mount_point)
        if os.path.exists(fileName):        
            print "execel file exeist"
        else:
            createExecel(fileName)

        row1,row2,row3=read_excel(fileName)
        
        exportExecl(row1,text_list,fileName)
        occurence_textcontent(row2,div_list,fileName,text_list)
        occurence_liblary(row3,div_list,fileName,text_list)
        print "修改初始id:{}->{}".format(os.listdir(path)[0],id)
        os.rename("{}/{}".format(path,os.listdir(path)[0]),"{}/{}".format(path,id))
        print '\n'*2
    
