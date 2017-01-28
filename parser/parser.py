from bs4 import BeautifulSoup
import sys, json
import pprint 

#input facebook ID number and display name
def read_in():
	lines = sys.stdin.readlines()
	return json.loads(lines[0])

# example input: { "facebook_id": "100000757823244", "display_name": "Aidon Lebar" }
userIn = read_in() # format: { facebook_id: '348264782638746', display_name: 'David Lougheed' }

clientName = userIn["display_name"]
clientID = userIn["facebook_id"]

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
			name_processed = name_.replace('@facebook.com', '')
			if name_processed != clientName and name_processed != clientID: 
				name = name_processed
				convos[name_processed] = [] #names the converstation for who is the other person

		messages = con.find_all('div', class_="message")
		for msg in messages: 
			msgDic = {}
			user = msg.find('span', class_="user").contents[0].replace('@facebook.com', '') #gets the sender of the specific message
			if user == clientName or user == clientID: 
				msgDic["isMe"] = True 
			else: 
				msgDic["isMe"] = False 
			#determines if it was you or the other person who sent that message


			msgDic["content"] = ' '.join(message_contents[i].contents)
			#put contents of the message as a string in proper dictionary field
			i += 1
 
			convos[name] = [msgDic] + convos[name] 
		
		
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(convos)		

