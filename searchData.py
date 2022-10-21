import requests, json, pymysql, time, schedule
	# korea covid-19 api url
	# we allow this api access grant in https://www.data.go.kr/data/15099842/openapi.do
url = 'http://apis.data.go.kr/1790387/covid19CurrentStatusConfirmations/covid19CurrentStatusConfirmationsJson'
	# api service key
uri = url + '?serviceKey='

	"""
	table create information
	create table entire(
	date date not null default now(),
	Num int not null);
	"""

	#database address, user/pw, DB name, user need select, insert grant
dbcon = pymysql.connect(host = '127.0.0.1', user = 'user', password = 'password', db = 'dbname', charset = 'utf8')
print('Database CovidData Connect Success. ' + time.strftime('%Y-%m-%d %H:%M:%S'))
	#database sql insert object
cur = dbcon.cursor()

def datacheck():
			#api response value
        response = requests.get(uri).json()
        	#this api mmdd value return ex) 01.01. need data change yy-mm-dd foramt
        data = response['response']['result'][0]
        arr = data['mmdd7'].split('.')
        tday = str(time.localtime().tm_year) + '-' + arr[0] + '-' + arr[1]

        print('Data Update Check.... ' + time.strftime('%Y-%m-%d %H:%M:%S'))

        	#equal date in table check
        cur.execute('select * from entire where date = \'' + tday + '\';')
        	#selectd recode
        recode = cur.fetchall()

        	#recode row == 0, not recode
        if len(recode)==0:
                print('New Data Updated. ' + time.strftime('%Y-%m-%d %H:%M:%S') + ' Updating...')
                
                	#table new data insert
                cur.execute('insert into entire(num) values(' + data['cnt7'] + ');')
                dbcon.commit()

                	#new data select, successful data input check
                cur.execute('select * from entire where date = \'' + time.strftime('%Y-%m-%d') + '\';')
                recode = cur.fetchall()
                if len(recode)!=0:
                        print('Data input Success. ' + time.strftime('%Y-%m-%d %H:%M:%S') + '\ntoday Num = ' + data['cnt7'])

    #new data check delay, I check 30min cycle
schedule.every(30).minutes.do(datacheck)

while True:
    schedule.run_pending()
    	#function check cycle/clock/delay (separate from upper delay)
    time.sleep(600)
