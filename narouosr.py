###########################################
# narouosr.py
###########################################
# なろうに投稿した小説の活動報告とTwitter報告用の支援ツール
# Pythonista3(iPhone,iPad), Python3(Mac)のみ。自動で環境を判定して動作します
# 
# $ pyhon narouosr.py
# コンソールで実行すると、Atomフィードから最新5タイトルを取得し、表示
# タイトルとお知らせ媒体を選択すると、（何も入力しないとデフォルトで最新話＋活動報告を選択）
# 読みもせず雑に考えたお知らせ内容をクリップボードへいれてくれます。
###########################################

#フィードを読み込む
# readfeed(RSS_URL)[0]['title']
# とかでタイトルとかが読み込めるようにする

def readfeed(RSS_URL):
	import feedparser
	import re
	ent = feedparser.parse(RSS_URL)['entries']#フィードを取得
	# なぜか新着順で並んでないので一旦全部リストに入れてソートする
	ent= [{'id': e['id'], 'time': e['published'], 'title': e['title']}for e in ent]# 一旦リストに格納
	ent.sort(key=lambda x: x['time'], reverse=True)# ソートする
	# 新着5件をリストに入れつつタイトルを整える
	ret=[]
	for x in range(5):
		#タイトルの余計なとこを取る
		if '短編小説[' in ent[x]['title']:
			ititle= re.split('[\[\]]',ent[x]['title'])
			n= 0 #短編の話数は0とする
		else:
			ititle=re.split('[\-\]第部]',ent[x]['title'])
			n= ititle[3] #話数
		j= {'num':n, 'id': ent[x]['id'], 'time': ent[x]['time'], 'title': ititle[1]}
		ret.append(j)
	return(ret)


#記事を決定　降順で表示
# inputindex(dict-no-list)
# 整数を返す

def inputindex(arr):
	import sys
	#表示するメッセージを用意
	cat= ""
	for i,t in enumerate(arr):
		cat= "\n" + ('[{}], {}'.format(i, t['title'])) + cat
	cat= cat+ "\n\n　　上記から番号を選択してください default=[0]"
	#入力を求める
	print(cat)
	inp = input()
	#ここからはエラー処理
	try:
		inp=int(inp)
		test= arr[inp]['title']
	except :
		inp= 0
	else:
		pass #負の値を入れると、一番古い記事からさかのぼっていく	
	return(inp)

#媒体を選ばせる　昇順で表示
# choosebaitai(list)
# 整数を返す

def choosebaitai(arr):
	import sys
	#表示するメッセージを用意
	cat= ""
	for i,t in enumerate(arr):
		cat= cat + "\n" + ('[{}], {}'.format(i, t))
	cat= cat+ "\n\n　　上記から番号を選択してください default=[0]"
	#入力を求める
	print(cat)
	inp = input()
	#ここからはエラー処理
	try:
		inp=int(inp)
		test= arr[inp]
	except :
		inp= 0
	else:
		pass #負の値を入れると、一番古い記事からさかのぼっていく	
	return(inp)

#渡ってきた文字列をクリップボードへ
# osr(body)
# Macとiosで関数違うので処理かえてます

def osr(body):
	import getpass
	
	usr= (getpass.getuser())

	if(usr == 'mobile'):
		import clipboard
		clipboard.set(body)
	else:
		import pyperclip as clip
		clip.copy(body)
		
	return(True)

#渡ってきた文字列の頭とお尻のn個の改行を消す
#kaigyo(str)
#文字列を返す
def kaigyo(moji):
	import re
	moji= re.sub(r'^\n+', "", moji)
	moji= re.sub(r'\n+$', "", moji)
	# moji= moji + '\n'
	return moji


###########################################
import configparser
# 設定ファイルを読み込む
inifile = configparser.ConfigParser()
inifile.read('narouosr.ini', 'UTF-8')

#フィードから必要な部分を抽出した辞書リストをもらう
feeds= readfeed(inifile.get('user','rss'))

#どの記事をお知らせするのか番号を決定
index=0 #初期値をセット
index= inputindex(feeds) #インタラクティブに選ばない場合この行コメントアウト

#どの媒体に知らせるのか(テンプレを選ぶ)
temp= inifile.get('temp','narou') #初期値をセット
keys= inifile.options('temp') #インタラクティブに選ばない場合２行コメントアウト
temp= inifile.get('temp',keys[choosebaitai(keys)]) #インタラクティブに選ばない場合２行コメントアウト

#お知らせを作る
num1= int(feeds[index]['num'])
num0= num1 - 1
osrnum1= str(num1) #記事番号　URLの末尾のやつ
osrnum0= str(num0) #一つ前の記事番号

import datetime
date = datetime.datetime.strptime(feeds[index]['time'], '%Y-%m-%dT%H:%M:%S+09:00')
osrtime=str(date.hour)#記事投稿時間

osrtitle= feeds[index]['title'] #記事サブタイトル
osraramain= inifile.get('arasuji','main') #メインのあらすじ
osraramain= kaigyo(osraramain) #改行を整える
osrarasub= inifile.get('arasuji','sub') #サブのあらすじ
osrarasub= kaigyo(osrarasub) #改行を整える
osrurl= inifile.get('user','url') #小説目次URL
#余計な改行消します

#テンプレに突っ込む
body= temp.replace('@num1@', osrnum1).replace('@num0@', osrnum0).replace('@title@', osrtitle).replace('@time@', osrtime).replace('@aramain@', osraramain).replace('@arasub@', osrarasub).replace('@url@', osrurl)
body= kaigyo(body) #改行を整える

#実際に知らせる
osr(body)

print(body)

