#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2, re, xbmcaddon, string, xbmc, xbmcgui, xbmcplugin, os, urllib

#__settings__ = xbmcaddon.Addon(id='plugin.video.podrobnosti.rss')
#__language__ = __settings__.getLocalizedString

HEADER     = "Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60"
SITE_URL  = 'http://www.podrobnosti.ua'

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

def get_programs(isLive=False):
	try:
		req = urllib2.Request(SITE_URL + '/rss/podrobnosti.rss')
		req.add_header('User-Agent', HEADER)
		f = urllib2.urlopen(req)
		a = f.read()
		f.close()
	except:
		return
	video_url_array = []
	name_array = []
	plot_array = []
	Category_array = []
	PubDate_array = []
	ImageURL_array = []
	array_size = 0

	start_prog = re.compile('<item>(.*?)</item>', re.DOTALL).findall(a)
	x = 2
	if len(start_prog) > 0:
		for Rss_data in start_prog:
			s_utf8 = Rss_data
			s_uni = s_utf8.decode('cp1251')
			Rss_data = s_uni.encode('utf8')
			item_data = re.compile(
			    '<title>(.+?)</title>\s.*' + 
			    '<link>(.+?)</link>\s.*' + 
			    '<pubDate>(.+?)</pubDate>\s.*' + 
			    '<category domain="http://podrobnosti.ua/podrobnosti/">(.+?)</category>\s.*' + 
			    '<guid isPermaLink="false">(.+?)</guid>\s.*' + 
			    '<description>(.+?)</description>\s.*' + 
			    '<media:content url="(.+?)" type="image/jpeg" width="(.+?)" height="(.+?)" />\s.*', re.MULTILINE| re.DOTALL).findall(Rss_data)
			if len(item_data) > 0:
				for Title, Link, PubDate, Category, Guid, Descr, ImageURL, ImageWidth, ImageHeight in item_data:
					img_base = re.compile('(.*)_3.jpg').findall(ImageURL)[0]
					video_url = img_base+'_4.mp4'
					cln_title = clean(Title)
					Plot = clean(Descr)
					listitem=xbmcgui.ListItem(str(x)+'. '+cln_title,iconImage=ImageURL,thumbnailImage=ImageURL)
					listitem.setInfo(type="Video", infoLabels = {
						"Title": 	str(x)+'. '+cln_title,
						"Studio": 	'PODROBNOSTI.UA',
						"Director": 	Link,
						"Plot": 	Plot,
						"Genre": 	Category + ' * ' + PubDate,
						"Date": 	PubDate } )
					if isLive:
						try:
							setindex = video_url_array.index(video_url)
							Plo = Category + ' * ' + PubDate + ' * ' + cln_title
							plot_array[setindex] += '\n\n' + Plo + '\n\n' + Plot
						except:
							video_url_array.append(video_url)
							name_array.append(cln_title)
							plot_array.append(Plot)
							Category_array.append(Category)
							PubDate_array.append(PubDate)
							ImageURL_array.append(ImageURL)

					else:
						xbmcplugin.addDirectoryItem(handle, video_url, listitem, False)
					x += 1
	if isLive:
		i = 0
		for cur_url in video_url_array:
			name = name_array[i]
			plot = plot_array[i]
			Cat = Category_array[i]
			PubDat = PubDate_array[i]
			img = ImageURL_array[i]
			listitem=xbmcgui.ListItem(name, iconImage=img, thumbnailImage=img)
			listitem.setInfo(type="Video", infoLabels = {
				"Title": 	name,
				"Studio": 	'PODROBNOSTI.UA',
				"Plot": 	plot,
				"Genre": 	Cat + ' * ' + PubDat,
				"Date": 	PubDat } )
			playList.add(cur_url, listitem)
			i += 1


params = get_params()
mode  = None

try:
	mode  = urllib.unquote_plus(params["mode"])
except:
	pass

if mode == None:
	listitem = xbmcgui.ListItem('1. PODROBNOSTI.Live!', iconImage=site_thumb, thumbnailImage=site_thumb)
	url = sys.argv[0] + "?mode=live"
	xbmcplugin.addDirectoryItem(handle, url, listitem, False)
	get_programs(False)

	xbmcplugin.setPluginCategory(handle, 'PODROBNOSTI.UA')
	xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_DATE)
	xbmcplugin.endOfDirectory(handle)

elif mode == 'live':
	playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playList.clear()
	get_programs(True)
	player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	player.play(playList)

