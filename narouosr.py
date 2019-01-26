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
	news_dic = feedparser.parse(RSS_URL)
	ret= []
	for i in range(5):
		ititle=re.split('[\-\]第部]',news_dic.entries[i].title)#タイトルの余計なとこを取る
		pubtime = news_dic.entries[0].published_parsed # 何時に投稿したか
		itime = str(pubtime.tm_hour + 9) # 日本時間に直す
		#戻り値をセットして返す
		j={'title':ititle[1], 'num': ititle[3], 'time':itime,}
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

#渡ってきた文字列の頭とお尻のn個の改行を消し、お尻に一つ改行を入れる
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

#フィードから必要な部分を抽出した記事のリストをもらう
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
osrtitle= feeds[index]['title'] #記事サブタイトル
osrtime= feeds[index]['time'] #記事投稿時間
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

