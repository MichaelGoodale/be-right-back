from bs4 import BeautifulSoup
import sys

targetName = "Aidon Lebar"

convos = {}

messageFile = open("messages.htm", "r").read()

soup = BeautifulSoup(messageFile, "html.parser")

all_convos = soup.find_all('div',class_="thread")
for con in all_convos:
	conName = con.find(text = True)
	nameList = conName.split(', ')

	i = 0
	message_contents = con.find_all('p')

	if (len(nameList) == 2):
		name = ""
		for name_ in nameList : 
			if name_ != targetName: 
				name = name_
				convos[name_] = [] 
				#print name
				#print nameList

		messages = con.find_all('div', class_="message")
		for msg in messages: 
			msgDic = {}
			user = msg.find('span', class_="user").contents[0] 
			if user == targetName : 
				msgDic["isMe"] = True 
			else: 
				msgDic["isMe"] = False 


			# GET IT FROM THREAD NOT MESSAGE 
			msgDic["content"] = message_contents[i].contents[0]
			i += 1
 

		print msgDic
		convos[name].append(msgDic)




	


#print(test[])