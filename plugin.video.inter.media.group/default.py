#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib,urllib2,cookielib,re,sys,os,time
import xbmcplugin,xbmcgui,xbmcaddon,xbmc

shownail = xbmc.translatePath(os.path.join(os.getcwd().replace(';', ''),"icon.png"))
pluginhandle = int (sys.argv[1])

def addDir(name,url,mode,iconimage='',plot=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        icon=xbmc.translatePath(os.path.join(os.getcwd().replace(';', ''),iconimage))
        liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot":plot})
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def ROOT():
        addDir('Inter','Inter','playInter','inter.png')
        addDir('HTH','HTH','playHTH', 'ntn.png')
        addDir('K-1','K1','playK1', 'k1.png')

def PLAYVIDEO(name, swf, rts, path):
    i=xbmcgui.ListItem(name)
    i.setProperty("SWFPlayer", swf)
    i.setProperty("PlayPath", path)
    xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(rts, i)

def PLAYINTER():
    PLAYVIDEO('Inter', 'http://inter.ua/images/player.swf?v5.2.1151', 'rtmp://62.149.26.237:80/tv', 'mp4:inter')

def PLAYHTH():
    PLAYVIDEO('HTH', 'http://ntn.ua/images/player.swf?v5.2.1151', 'rtmp://62.149.26.237:80/tv', 'mp4:ntn')
    
def PLAYK1():
    PLAYVIDEO('K-1', 'http://ntn.ua/images/player.swf?v5.2.1151', 'rtmp://62.149.26.237:80/tv', 'mp4:k1')

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param


params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=urllib.unquote_plus(params["mode"])
except:
        pass

if mode==None:
        ROOT()
        xbmcplugin.endOfDirectory(int(sys.argv[1]),updateListing=False,cacheToDisc=True)
elif mode=='playInter':
        PLAYINTER()
elif mode=='playHTH':
        PLAYHTH()
elif mode=='playK1':
        PLAYK1()

