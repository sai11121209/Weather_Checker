import ui,requests,location,csv
from PIL import Image


def update(sender):
	#背景
	sender.superview['BackImage'].image = image
	sender.superview['Title'].text = data['title']
	sender.superview['Today Weather'].text = weatherdata['today']
	sender.superview['Tomorrow Weather'].text = weatherdata['tomorrow']
	DATomorrow = sender.superview['DATomorrow Weather']
	if len(weatherdata) == 3:
		DATomorrow.text = weatherdata['DAtomorrow']
	else:
		DATomorrow.text = '明後日情報取得中'
	sender.superview['Details'].text = data['description']['text']
	sender.superview['Update Date'].text = '最終更新時刻:'+data['publicTime'].split('+')[0]
	sender.superview['GpsData'].text = '現在地:'+ungeodata['result']['prefecture']['pname']+ungeodata['result']['municipality']['mname']
	sender.superview['Copyright'].text = data['copyright']['provider'][0]['name']+':'+data['copyright']['provider'][0]['link']+'\n'+data['copyright']['title']+':'+data['copyright']['link']
	sender.superview['CopyrightGeodata'].text = ungeodata['meta'][0]['content']

def end(sender):
	sender.close()
	
def getgps():
	location.start_updates()
	gpsdata = location.get_location()
	location.stop_updates()
	return gpsdata
	
def getungeo(gpsdata):
	geourl = 'https://www.finds.jp/ws/rgeocode.php?json&lat='+str(gpsdata['latitude'])+'&lon='+str(gpsdata['longitude'])
	ungeodata = requests.get(geourl).json()
	return ungeodata

def selectimage(data):
	image = []
	types = ['晴','曇','雨']
	image.append(ui.Image.named('sunny.JPG'))
	image.append(ui.Image.named('cloudy.JPG'))
	image.append(ui.Image.named('rainy.JPG'))
	image = dict(zip(types,image))
	for type in types:
		if type in data:
			return image[type]
			
def csvreader(fileName):
	data = []
	with open(fileName+'.csv',encoding = 'utf-8') as file:
		reader = csv.reader(file)
		for row in reader:
			data.append(row)
		return data
	
def setarea(datas,pcode):
	for data in datas:
		if len(pcode)==2:
			if ''.join(data[0][0:2]) in pcode:
				return data[0]
		if len(pcode)==1:
			if data[0][0] in pcode:
				print(data[0])
				return str(data[0])

locationlist = csvreader('wpd')
ungeodata = getungeo(getgps())
print(ungeodata['result']['prefecture']['pname']+ungeodata['result']['municipality']['mname'])
weatherurl = 'http://weather.livedoor.com/forecast/webservice/json/v1?city='

data = requests.get(weatherurl+setarea(locationlist,str(int(ungeodata['result']['prefecture']['pcode'])))).json()

str = []
#ロケーションurl取得
for locationurl in data['pinpointLocations']:
	if locationurl['name'] == ungeodata['result']['municipality']['mname']:
		url = locationurl['link']
for weather in data['forecasts']:
	str.append(weather['dateLabel']+'('+weather['date']+')'+':'+weather['telop'])
weatherlabel = ['today','tomorrow','DAtomorrow']
weatherdata = dict(zip(weatherlabel,str))
v = ui.load_view()
image = selectimage(list(data['forecasts'][0]['telop'])[0])
update(v.subviews[1])
v.background_color = '#63bcff'
v.present('sheet')
