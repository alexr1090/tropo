import re
import urllib2
import datetime
import time
from xml.dom import minidom, Node

day_of_week_dic = {
"Mon": "Monday",
"Tue": "Tuesday",
"Wed": "Wednesday",
"Thu": "Thursday",
"Fri": "Friday",
"Sat": "Saturday",
"Sun ": "Sunday ",
"mph":"Milesperhour "
}

def replace_words(text, word_dic):
     rc = re.compile('|'.join(map(re.escape, word_dic)))

     def translate(match):
          return word_dic[match.group(0)]
     return rc.sub(translate, text)
def weather():
     result = ask("Enter or say your five digit zip code",{"choices":"[5 DIGITS]", 
        	"timeout":30,
        	"attempts":3,
        	"onBadChoice": lambda event : say("I'm sorry,  I didn't understand that.")})
     urlRead = urllib2.urlopen('http://xml.weather.yahoo.com/forecastrss/%s_f.xml'%result.value)
     xml = minidom.parse(urlRead)
     if xml:
          for channelNode in xml.documentElement.childNodes:
	       if channelNode.nodeName == 'channel':
	            for itemNode in channelNode.childNodes:
	                 if itemNode.nodeName == 'item':
			      for yWeatherNode in itemNode.childNodes:
			           if yWeatherNode.nodeName == 'yweather:forecast':
				        day = replace_words(yWeatherNode.getAttribute('day'), day_of_week_dic)
	          			low = yWeatherNode.getAttribute('low')
					high = yWeatherNode.getAttribute('high')
					condition = yWeatherNode.getAttribute('text')
					say("For "+day+", there is a low of "+low+" degrees and a high of "+high+" degrees. The condition is "+condition+".")
			

def weather_old():
    result = ask("Enter or say your five digit zip code",{"choices":"[5 DIGITS]", 
    "timeout":30,
    "attempts":3,
    "onBadChoice": lambda event : say("I'm sorry,  I didn't understand that.")})
   # f = urllib.urlopen('http://www.google.com/ig/api?weather=%s'%result.value)
   # wtxt =f.read()
   # f.close()
    var = ""
    temp = re.search(r'temp_f.{7}(\d+)', wtxt)
    if temp: var = var + ("Current temperature: %s"%temp.group(1))+'.'
    else: say ("no match found")

    temp = re.search(r'(Humidity:.\d+.)', wtxt)
    if temp:var = var +' '+ temp.group(1)+'.'
    else: say ("no match")

    temp = re.search(r'(Wind:.*mph)', wtxt)
    if temp: var = var +' '+ temp.group(1)+'.'
    else: say ("no match for wind")

    temp = re.search(r'low data="(\d+)"', wtxt)
    if temp: var= var+' '+ ("Low:%s"%temp.group(1))+'.'
    else: say ("no match for low data")

    temp = re.search (r'high data="(\d+)"', wtxt)
    if temp: var= var +' '+ ("High:%s"%temp.group(1))+'.'
    else: say ("no match for high data")

    temp = re.search (r'condition data="(\w+|\w+\s\w+|\w+\s\w+\s\w+)"', wtxt)
    if temp: var= var+' '+("Condition:%s"%temp.group(1))+'.'
    else: say ("no match for condition data")

    say (var)
x__x=0
yesterdays_game=0
def getInfo(day,month):
        global x__x
	global yesterdays_game
	if x__x>0:
		 yesterdays_game= 1
	in_progress =0 
        t = datetime.date.today()
	urlRead = urllib2.urlopen('http://gd2.mlb.com/components/game/mlb/year_' + t.strftime("%Y") + '/month_'+month+ '/day_'+day+'/miniscoreboard.xml')
	if not yesterdays_game:cardinals_say_info = ("Today the Cardinals don't play.")
        else: cardinals_say_info =("Yesterday the Cardinals were off.")
	if urlRead:
		xml = minidom.parse(urlRead)
		if xml:
			for game_node in xml.documentElement.childNodes :
				if game_node.nodeName == "game":
					home_team = game_node.getAttribute('home_team_name')
					road_team = game_node.getAttribute('away_team_name')
					if home_team == ("Cardinals"):
						cards_wins = game_node.getAttribute('home_win')
						cards_losses= game_node.getAttribute('home_loss')
						cards_record = (" The Cardinals record is "+cards_wins+ " wins and "+cards_losses+" losses.")
						opponent = game_node.getAttribute('away_team_city') + ' '+ game_node.getAttribute('away_team_name')
						start_time = game_node.getAttribute('home_time') + ' ' + game_node.getAttribute('home_ampm')
						if yesterdays_game==0:
							if game_node.getAttribute('status') == 'In Progress':
								#top inning returns 'Y' if true
								top_inning = game_node.getAttribute('top_inning')
								opponent_runs = game_node.getAttribute('away_team_runs')
								cards_runs = game_node.getAttribute('home_team_runs')
								tv_station = game_node.getAttribute('tv_station')
								#convert 'FS-M' to equal Fox Sports Midwest
								if tv_station == 'FS-M': tv_station = 'Fox Sports Midwest'
								in_progress = 1
								inning = game_node.getAttribute('inning')
								opponent_runs = int(opponent_runs)
								cards_runs = int(cards_runs)
								cards_runs_buf = str(cards_runs)
								opponent_runs_buf = str(opponent_runs)
								
								if top_inning=='Y':
									if opponent_runs == cards_runs: cardinals_say_info = ("Today the Cardinals started play at home at "+start_time+" on "+tv_station+" against the "+opponent+". Right now the game is tied "+cards_runs_buf+" to "+cards_runs_buf+" in the top of inning "+inning+". "+cards_record)
									elif opponent_runs > cards_runs:cardinals_say_info = ("Today the Cardinals started play at home at "+start_time+" on "+tv_station+" against the "+opponent+". Right now the cardinals are losing "+opponent_runs_buf+" to "+cards_runs_buf+" in the top of inning "+inning+"."+cards_record)
									else: cardinals_say_info = ("Today the Cardinals started play at home at "+start_time+" on "+tv_station+" against the "+opponent+". Right now the Cardinals are winning "+cards_runs_buf+" to "+opponent_runs_buf+" in the top of inning "+inning+"."+cards_record)
								else:
									if opponent_runs == cards_runs: cardinals_say_info = ("Today the Cardinals started play at home at "+start_time+" on "+tv_station+" against the "+opponent+". Right now the game is tied "+cards_runs_buf+" to "+cards_runs_buf+" in the bottom of inning "+inning+'.'+cards_record)
									elif opponent_runs > cards_runs:cardinals_say_info = ("Today the Cardinals started play at home at "+start_time+" on "+tv_station+" against the "+opponent+". Right now the cardinals are losing "+opponent_runs_buf+" to "+cards_runs_buf+" in the bottom of inning "+inning+"."+cards_record) 
									else: cardinals_say_info = ("Today the Cardinals started play at home at "+start_time+" on "+tv_station+" against the "+opponent+". Right now the Cardinals are winning "+cards_runs_buf+" to "+opponent_runs_buf+" in the bottom of inning "+inning+"."+cards_record)
							elif game_node.getAttribute('status') == 'Final':
								opponent_runs = game_node.getAttribute('away_team_runs')
								cards_runs = game_node.getAttribute('home_team_runs')
								in_progress = 1
								inning = game_node.getAttribute('inning')
								opponent_runs = int(opponent_runs)
								cards_runs = int(cards_runs)
								cards_runs_buf = str(cards_runs)
								opponent_runs_buf = str(opponent_runs)
								if opponent_runs < cards_runs: cardinals_say_info = ("The Cardinals already played today. They won "+cards_runs_buf+" to "+opponent_runs_buf+"."+cards_record) 		
								else: cardinals_say_info = ("The cardinals already played today. They lost "+ opponent_runs_buf + ' to '+cards_runs_buf+"."+cards_record)
							if not in_progress:cardinals_say_info=("Today the Cardinals play the " + opponent + " at home. The start time is "+ start_time+'.'+cards_record)
						#what to do when checking yesterdays game
						else:
							if game_node.getAttribute('status') == 'Final':
								opponent_runs = game_node.getAttribute('away_team_runs')
								cards_runs = game_node.getAttribute('home_team_runs')
								in_progress = 1
								inning = game_node.getAttribute('inning')
								opponent_runs = int(opponent_runs)
								cards_runs = int(cards_runs)
								cards_runs_buf = str(cards_runs)
								opponent_runs_buf = str(opponent_runs)
								if opponent_runs < cards_runs: cardinals_say_info = ("Yesterday the Cardinals played the " + opponent+". They won "+cards_runs_buf+" to "+opponent_runs_buf+".") 		
								else: cardinals_say_info = ("Yesterday the cardinals played the " +opponent+". They lost "+ opponent_runs_buf + ' to '+cards_runs_buf+".")
							
					elif road_team == ("Cardinals"):
						cards_wins = game_node.getAttribute('away_win')
						cards_losses= game_node.getAttribute('away_loss')
						cards_record = (" The Cardinals record is "+cards_wins+ " wins and "+cards_losses+" losses.")
						opponent = game_node.getAttribute('home_team_city') + ' ' + game_node.getAttribute('home_team_name')
						start_time = game_node.getAttribute('away_time') + ' ' + game_node.getAttribute('away_ampm')
						if yesterdays_game==0:
							if game_node.getAttribute('status') == 'In Progress':
								#top inning returns 'Y' if true
								top_inning = game_node.getAttribute('top_inning')
								opponent_runs = game_node.getAttribute('home_team_runs')
								cards_runs = game_node.getAttribute('away_team_runs')
								tv_station = game_node.getAttribute('tv_station')
								#convert 'FS-M' to equal Fox Sports Midwest
								if tv_station == 'FS-M': tv_station = 'Fox Sports Midwest'
								in_progress = 1
								inning = game_node.getAttribute('inning')
								opponent_runs = int(opponent_runs)
								cards_runs = int(cards_runs)
								cards_runs_buf = str(cards_runs)
								opponent_runs_buf = str(opponent_runs)
								if top_inning=='Y':
									if opponent_runs == cards_runs: cardinals_say_info = ("Today the Cardinals started play on the road at "+start_time+" on "+tv_station+" against the "+opponent+". Right now the game is tied "+cards_runs_buf+" to "+cards_runs_buf+" in the top of inning "+inning+"."+cards_record)
									elif opponent_runs > cards_runs:cardinals_say_info = ("Today the Cardinals started play on the road at "+start_time+" on "+tv_station+" against the "+opponent+". Right now the cardinals are losing "+opponent_runs_buf+" to "+cards_runs_buf+" in the top of inning "+inning+"."+cards_record) 
									else: cardinals_say_info = ("Today the Cardinals started play on the road at "+start_time+" on "+tv_station+" against the "+opponent+". Right now the Cardinals are winning "+cards_runs_buf+" to "+opponent_runs_buf+" in the top of inning "+inning+"."+cards_record)
								else:
									if opponent_runs == cards_runs: cardinals_say_info = ("Today the Cardinals started play on the road at "+start_time+" on "+tv_station+" against the "+opponent+". Right now the game is tied "+cards_runs_buf+" to "+cards_runs_buf+" in the bottom of innning "+inning+"."+cards_record)
									elif opponent_runs > cards_runs:cardinals_say_info = ("Today the Cardinals started play on the road at "+start_time+" on "+tv_station+" against the "+opponent+". Right now the cardinals are losing "+opponent_runs_buf+" to "+cards_runs_buf+" in the bottom of inning "+inning+"."+cards_record) 
									else: cardinals_say_info = ("Today the Cardinals started play on the road at "+start_time+" on "+tv_station+" against the "+opponent+". Right now the Cardinals are winning "+cards_runs_buf+" to "+opponent_runs_buf+" in the bottom of inning "+inning+"."+cards_record)
							elif game_node.getAttribute('status') == 'Final':
								opponent_runs = game_node.getAttribute('home_team_runs')
								cards_runs = game_node.getAttribute('away_team_runs')
								in_progress = 1
								inning = game_node.getAttribute('inning')
								opponent_runs = int(opponent_runs)
								cards_runs = int(cards_runs)
								cards_runs_buf = str(cards_runs)
								opponent_runs_buf = str(opponent_runs)
								if opponent_runs < cards_runs: cardinals_say_info = str("The Cardinals already played today. They won "+cards_runs_buf+" to "+opponent_runs_buf+"." +cards_record)		
								else: cardinals_say_info = ("The cardinals already played today. They lost "+opponent_runs_buf+" to "+cards_runs_buf+"."+cards_record)
							if not in_progress:cardinals_say_info =("Today the Cardinals play the " + opponent+ " on the road. The start time is " + start_time+'.'+cards_record)	
						#what to do for yesterdays game
						else:
							if game_node.getAttribute('status') == 'Final':
								opponent_runs = game_node.getAttribute('home_team_runs')
								cards_runs = game_node.getAttribute('away_team_runs')
								in_progress = 1
								inning = game_node.getAttribute('inning')
								opponent_runs = int(opponent_runs)
								cards_runs = int(cards_runs)
								cards_runs_buf = str(cards_runs)
								opponent_runs_buf = str(opponent_runs)
								if opponent_runs < cards_runs: cardinals_say_info = str("Yesterday the Cardinals played the " + opponent+". They won "+cards_runs_buf+" to "+opponent_runs_buf+".") 		
								else: cardinals_say_info = ("Yesterday the cardinals played the " +opponent+". They lost "+ opponent_runs_buf + ' to '+cards_runs_buf+".")
								
	say (cardinals_say_info)
	#get yesterdays game
	x__x+=1
	if not yesterdays_game:
		day = int(day)
		if day == 1: 
			day =giveUsADay(month)
			mon2 = int(month)
			mon2-=1
			mon2= str(mon2)
			if len(mon2)==1: mon2 = '0'+mon2
			getInfo(day,mon2)
		else:
			day -=1
			day = str(day)
			if len(day) ==1: day = '0' + day
			getInfo(day, month)

#giveUsADay returns integer day of month based on if current day is 1 
def giveUsADay(month):
	if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month==12 ):
		return 31
	elif (month == 4 or month==6 or month == 9 or month == 11):
		return  30
	else: return  28
def cardinals():
	t = datetime.date.today()
	#have to check server time. since their server is 5 hours ahead of our local time
	day = str(t)
	day = day.split('-')
	Prev_month = int(day[1])
	Prev_month-=1
	month = int(day[1])
	day = int(day[2])
	if Prev_month == 0:
		Prev_month=12
	hour = (time.localtime())
	hour = int(hour[3])
	if hour < 5:
		if day == 1:
			day=giveUsADay(Prev_month)
			day = str(day)
			month = str(Prev_month)
                else: 
			day -= 1
			day = str(day)
			month = str(month)
	        if len(month) == 1: month = '0' + month
                if len(day) == 1: day = '0'+ day
	        getInfo(day,month)	
	else:
	        day = str(day)
	        month = str(month)
	        if len(month) == 1: month = '0' + month
	        if len(day) == 1: day = '0'+ day
	        getInfo(day,month)
        


##DIC##

#using a dictionary because I need practice with them!
day_of_week_dic = {
"Mon": "Monday",
"Tue": "Tuesday",
"Wed": "Wednesday",
"Thu": "Thursday",
"Fri": "Friday",
"Sat": "Saturday",
"Sun ": "Sunday ",
"mph":"Milesperhour ",
"05":" oh five ",
"la dodgers":"L.A. dodgers"
}

##answer##

answer()
say("Thanks for calling Ben and Alex's Awesome Machine")
#look up number in a text file
callers_number = currentCall.callerID

fout = urllib2.urlopen('http://hosting.tropo.com/139757/www/num_file.txt')

for line in fout:
	line_buf = line.split(',')
	if callers_number == line_buf[0]:
		buf=("Welcome back "+line_buf[1])
		say(buf)


isayso = 1
while isayso:
	result = ask("What would you like to do?  Press 0 for a list of options.",     {'choices':"weather(1,weather), cardinals(2,cardinals),  spanish(5,spanish), menu(0,menu)"})


	if (result.name == 'choice'):
		if (result.value == "weather"):
			say("Weather")
			weather()
                        break
		if (result.value == "cardinals"):
			say("Cardinals")
			cardinals()
                        break
		if (result.value == "spanish"):
        		say(u"Lo siento, pero Benjamin y Alejandro no saben español para enseñarme.  Adios", {"voice":"Esperanza"})
        		break
		if (result.value == "menu"):
        		result2 = ask("for weather, say weather or press one.  To see what the cardinals are doing, press two. To end this call, simply hangup.",{'choices':"weather(1,weather), cardinals(2,cardinals)","timeout":10.0})
       	       	       

        		if (result2.name =='choice'):
				if (result2.value == 'weather'):
					say("Weather")
					weather()
					break
				elif(result2.value == 'cardinals'):
					say("Cardinals")
					cardinals()
					break
				else: continue

