from bs4 import BeautifulSoup
import sys

targetName = "Aidon Lebar"

convos = {}

messageFile = open("messages.htm", "r").read()

soup = BeautifulSoup(messageFile, "html.parser")

all_convos = soup.find_all('div',class_="thread")
#finds all conversations, called threads by facebook
for con in all_convos:
	conName = con.find(text = True) #gets names of convo participants
	nameList = conName.split(', ') #makes a list out of the participants of each convo

	i = 0
	message_contents = con.find_all('p') #gets the contents of all messages sent in a list

	if (len(nameList) == 2): #weeds out the group chats
		name = ""
		for name_ in nameList : 
			if name_ != targetName: 
				name = name_
				convos[name_] = [] #names the converstation for who is the other person

		messages = con.find_all('div', class_="message")
		for msg in messages: 
			msgDic = {}
			user = msg.find('span', class_="user").contents[0] #gets the sender of the specific message
			if user == targetName : 
				msgDic["isMe"] = True 
			else: 
				msgDic["isMe"] = False 
			#determines if it was you or the other person who sent that message


			msgDic["content"] = ' '.join(message_contents[i].contents)
			#put contents of the message as a string in proper dictionary field
			i += 1
 

		print msgDic
		convos[name].append(msgDic)




	


#print(test[])