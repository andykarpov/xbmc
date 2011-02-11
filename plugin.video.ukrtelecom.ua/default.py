#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2, re, xbmcaddon, string, xbmc, xbmcgui, xbmcplugin, os, urllib

__settings__ = xbmcaddon.Addon(id='plugin.video.ukrtelecom.ua')
PLAYLIST   = os.path.join( os.getcwd(), "resources", "iptv.m3u" );

handle = int(sys.argv[1])
site_thumb   = os.path.join( os.getcwd(), "default.tbn" )

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

def clean(name):
	remove=[('<![CDATA[',''),(']]>',''),('<span>',' '),('</span>',' '),('&amp;','&'),('&quot;','"'),('&#39;','\''),('&nbsp;',' '),('&laquo;','"'),('&raquo;', '"'),('&#151;','-'),('<nobr>',''),('</nobr>',''),('<P>',''),('</P>','')]
	for trash, crap in remove:
		name=name.replace(trash, crap)
	return name

def get_programs():
	try:
		req = urllib2.Request('file://' + PLAYLIST)
		f = urllib2.urlopen(req)
		a = f.read()
		f.close()
	except:
		return

	start_prog = re.compile('#EXTINF:0,(.*?)\n(.*?)\n', re.MULTILINE | re.DOTALL).findall(a)
	x = 2
	if len(start_prog) > 0:
		for ChannelInfo, ItemUrl in start_prog:
			ChannelData = re.compile('([0-9]+)\s(.*)',re.DOTALL).findall(ChannelInfo)
			if len(ChannelData) > 0:
				for ChannelId, ChannelName in ChannelData:
					image_url = os.path.join(os.getcwd(), 'resources', 'icons', str(ChannelId) + '.png');
					use_proxy = __settings__.getSetting('use_http_proxy');
					http_proxy = __settings__.getSetting('http_proxy');
					if (use_proxy == "true"):
					    video_url = http_proxy + ItemUrl.replace('udp://@', '/udp/').replace('udp://', '/udp/');
					else:
					    video_url = ItemUrl
					cln_title = clean(ChannelName)
					Plot = clean(ChannelName)
					listitem=xbmcgui.ListItem(str(ChannelId)+'. '+cln_title,iconImage=image_url,thumbnailImage=image_url)
					listitem.setInfo(type="Video", infoLabels = {
						"Title": 	str(ChannelId)+'. '+cln_title,
						"Studio": 	'UKRTELECOM.UA',
						"Director": 	video_url,
						"Plot": 	Plot })
					xbmcplugin.addDirectoryItem(handle, video_url, listitem, False)
					x += 1

params = get_params()
mode  = None

try:
	mode  = urllib.unquote_plus(params["mode"])
except:
	pass

if mode == None:
	get_programs()
	xbmcplugin.setPluginCategory(handle, 'UKRTELECOM.UA')
	xbmcplugin.endOfDirectory(handle)

