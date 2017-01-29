from bs4 import BeautifulSoup
import sys, json
import pprint
import re 

#input facebook ID number and display name
def read_in():
	lines = sys.stdin.readlines()
	return json.loads(lines[0])

# example input: { "facebook_id": "100000757823244", "display_name": "Aidon Lebar", "path": "/Users/Aidon/Documents/Be_Right_Back/messages.htm" }
userIn = read_in() # format: { facebook_id: '348264782638746', display_name: 'David Lougheed', 'BRB/path/messages.htm' }

clientName = userIn["display_name"]
clientID = userIn["facebook_id"]
path = userIn["path"]

convos = {}

messageFile = open(path, "r").read()

soup = BeautifulSoup(messageFile, "html.parser")

all_convos = soup.find_all('div',class_="thread")

#finds all conversations, called threads by facebook
for con in all_convos:
	conName = con.find(text = True) #gets names of convo participants
	nameList = conName.split(', ') #makes a list out of the participants of each convo

	j = 0
	message_contents = con.find_all('p') #gets the contents of all messages sent in a list

	if (len(nameList) == 2): #weeds out the group chats
		name = ""
		for name_ in nameList : 
			name_processed = name_.replace('@facebook.com', '')
			if name_processed != clientName and name_processed != clientID: 
				name = name_processed
				convos[name_processed] = [] #names the converstation for who is the other person

		messages = con.find_all('div', class_="message")
		

		for i,msg in enumerate(messages):
		
			user = messages[i].find('span', class_="user").contents[0].replace('@facebook.com', '') 
			strippedString = ' '.join(message_contents[j].contents).replace("\n", "").replace("\"", "").replace("^", "")
			strippedString = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'," URL ", strippedString)
			content = strippedString
			j += 1
		
		
		# BASE CASE 
			if i == 0 : 
				if user == clientName or user == clientID : 
					wasMe = True 
				else: 
					wasMe = False 
			
				msgDic = {"isMe": wasMe, 'content': content} 
		 
			else : 
				if user == clientName or user == clientID: 
					isMe = True 
				else: 
					isMe = False  
				#determines if it was you or the other person who sent that message
		
		
				if isMe == wasMe : 
				
					if content.endswith(".") == True : 
						content = content + " " 
					elif content != "" : 
						content = content + ". " 
					msgDic["content"] = content + msgDic["content"]
				
				else: 
					wasMe = isMe 
					convos[name] = [msgDic] + convos[name] 
					msgDic = {"isMe": isMe, "content": content} 
					
				if i == ( len(messages) - 1): 
					convos[name] = [msgDic] + convos[name] 

			#put contents of the message as a string in proper dictionary field
			
	
#prints as a happy little json object thing
print(json.dumps(convos))
sys.stdout.flush()
sys.exit(0)
