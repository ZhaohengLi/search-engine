# coding:utf-8
from django.http import HttpResponse
from django.shortcuts import render
from .models import Newslinks
import math
import re
import time

SHOW_NUM=10
orignalsearchinput=''
search=''
stime=0
etime=0
allresults={}
newscnt=0
pagecnt=0
costtime=0

def showNewsDetail(request, id):
    id=int(id)
    text = Newslinks.objects.get(id=id).text
    title = Newslinks.objects.get(id=id).title
    date = Newslinks.objects.get(id=id).date
    keywords = Newslinks.objects.get(id=id).keywords
    relatedkey = (keywords.split(',',1))[0]
    relatedkey = re.match(r'(.*?)\d{1,2}',relatedkey).group(1)
    relatedresults=list(Newslinks.objects.filter(title__contains=relatedkey))[:4]
    textdisplay='我们还为您准备了一些相关的新闻：'
    if len(relatedresults)==0:
        textdisplay='我们没有找到相关的新闻。'
    return render(request,'news.html',{'text':text,'title':title,'date':date,'id':id,'keywords':keywords,'results':relatedresults,'textdisplay':textdisplay,})


def index(request):
    if request.method=='POST':

        global SHOW_NUM
        global orignalsearchinput
        global search
        global stime
        global etime
        global allresults
        global newscnt
        global pagecnt
        global costtime

        tic=time.time()
        orignalsearchinput=request.POST['searchinput']
        search=request.POST['searchinput']
        if request.POST['stimeinput']!='' and request.POST['etimeinput']!='':
            stime=int(request.POST['stimeinput'])
            etime=int(request.POST['etimeinput'])
        else:
            stime=0
            etime=0

        if search=='':
            a=list(Newslinks.objects.filter(date__gt=20180912)[:6])
            return render(request,'home.html',{'showedtext':'刚刚你没有键入关键字，我们没无法开始搜索。','results':a})
        if ' ' in search:
            searchlist = search.split('')
            for item in searchlist:
                if item!='':
                    a=Newslinks.objects.filter(title__contains=item)
                    a= a | Newslinks.objects.filter(keywords__contains=item)
            a=a.distinct()
        else:
            a=Newslinks.objects.filter(title__contains=search)
            a= a | Newslinks.objects.filter(keywords__contains=search)
            a=a.distinct()

        if stime!=0 and etime!=0:
            a = a.filter(date__gt=int(stime))
            a = a.filter(date__lt=int(etime))
        toc = time.time()
        costtime = (toc-tic)*10
        allresults=list(a)
        newscnt=len(allresults)
        pagecnt=math.ceil(newscnt/SHOW_NUM)
        results=allresults[:SHOW_NUM]
        currntpagecnt=1
        haspre=bool(currntpagecnt>=2)
        hasnex=bool(currntpagecnt<=pagecnt-1)
        content={'orignalinput':orignalsearchinput,'newscnt':newscnt,
        'pagecnt':pagecnt,'results':results,'costtime':costtime,
        'currntpagecnt':currntpagecnt,'haspre':haspre,
        'hasnex':hasnex,'prepagecnt':currntpagecnt-1,'nexpagecnt':currntpagecnt+1}
        return render(request,'index.html',content)
    else:
        return HttpResponse('你没有键入任何内容')

def showhomepage(request):
    if request.method=='GET':
        a=list(Newslinks.objects.filter(date__gt=20180912)[:10])
        return render(request,'home.html',{'results':a,})
    else:
        return HttpResponse('WRONG GET!')


def showwantindex(request,wantpagecnt):
    global SHOW_NUM
    global orignalsearchinput
    global search
    global stime
    global etime
    global allresults
    global newscnt
    global pagecnt
    global costtime

    if wantpagecnt<=pagecnt and wantpagecnt>=1:
        results=allresults[(wantpagecnt-1)*SHOW_NUM:wantpagecnt*SHOW_NUM]
        currntpagecnt=wantpagecnt
        haspre=bool(currntpagecnt>=2)
        hasnex=bool(currntpagecnt<=pagecnt-1)
        content={'orignalinput':orignalsearchinput,'newscnt':newscnt,
        'pagecnt':pagecnt,'results':results,'costtime':costtime,
        'currntpagecnt':currntpagecnt,'haspre':haspre,
        'hasnex':hasnex,'prepagecnt':currntpagecnt-1,'nexpagecnt':currntpagecnt+1}
        return render(request,'index.html',content)
    else:
        results=allresults[:SHOW_NUM]
        currntpagecnt=1
        haspre=bool(currntpagecnt>=2)
        hasnex=bool(currntpagecnt<=pagecnt-1)
        content={'orignalinput':orignalsearchinput,'newscnt':newscnt,
        'pagecnt':pagecnt,'results':results,'costtime':costtime,
        'currntpagecnt':currntpagecnt,'haspre':haspre,
        'hasnex':hasnex,'prepagecnt':currntpagecnt-1,'nexpagecnt':currntpagecnt+1}
        return render(request,'index.html',content)


def showwantallnews(request,wantpagecnt):
    global SHOW_NUM
    wantpagecnt=int(wantpagecnt)
    newscnt=6947
    results=list(Newslinks.objects.all()[(wantpagecnt-1)*SHOW_NUM:wantpagecnt*SHOW_NUM])
    pagecnt=math.ceil(newscnt/SHOW_NUM)
    currntpagecnt=wantpagecnt
    haspre=bool(currntpagecnt>=2)
    hasnex=bool(currntpagecnt<=pagecnt-1)
    content={'newscnt':newscnt,'pagecnt':pagecnt,'results':results,
    'currntpagecnt':currntpagecnt,'haspre':haspre,
    'hasnex':hasnex,'prepagecnt':currntpagecnt-1,'nexpagecnt':currntpagecnt+1}
    return render(request,'allnews.html',content)
