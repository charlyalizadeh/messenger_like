from bs4 import BeautifulSoup
import re
import pandas as pd

class MessengerMsg:
    def __init__(self,name="",message=[],number_react = []):
        self.name = name
        self.message = message
        self.number_react = number_react

class MessengerStat:
    def __init__(self,name="Messenger Conversation"):
        self.messages = []
        self.html = ""

    def import_html(self,html):
        self.html = html

    def import_html_file(self,filename):
        file = open(filename,'r')
        self.html = file.read()

    def parse_data(self):

        bs = BeautifulSoup(self.html,'html.parser')
        name_origin = input("Please enter the Facebook name of the account from wich you got the html source code from : ")

        react_by_name = {}
        for first_div in bs.find_all('div',{'class':'_1t_p clearfix'}):

            name = first_div.find('img',{'class':'img','height':'32','width':'32'})
            if name==None:
                name = first_div.find('h5')
                name = name_origin if name==None else name.text
            else:
                name = name['alt']

            messages = []
            nb_react = []
            # Message by message
            for message in first_div.find_all('div',{'class':re.compile('clearfix.*')}):
                try:
                    # Text 
                    text_message = message.find('span',{'class':'_3oh- _58nk'})
                    if text_message!=None:
                        messages.append(text_message.text)

                    # Audio 
                    audio_message = message.find('a',{'role':'button','href':'#'})
                    if audio_message!=None:
                        messages.append("Audio")


                    # Vidéo 
                    video_message = message.find('video')
                    if video_message!=None:
                        messages.append(video_message['src'])

                    
                    # Image
                    images = message.find_all('div',{'role':'presentation'})
                    all_image = ""
                    if images!=None:
                        for image in images:
                            if image.has_attr('style'):
                                all_image+=image['style'][23:-3]+';'
                            else:
                                gif = image.find('img')
                                messages.append(gif['src'])
                    if all_image!="":
                        messages.append(all_image)

                    # Gif

                    # Number reactions
                    reaction = message.find('span',{'class':re.compile('_4kf5 _4kf6.*')})
                                                    
                    if reaction!=None:
                        nb_react.append(int(reaction.text))
                    else:
                        nb_react.append(0)

                except(AttributeError,KeyError) as er:
                    messages = ['Error']
                    nb_react = [-1]

            for i in range(0,len(messages)):
                print(name + ' : ',end = ' ')
                print(messages[i] + '  NDR : ' + str(nb_react[i]))
                
                self.messages.append(MessengerMsg(name,messages,nb_react))

    def get_react_stat(self):
        react_by_name = {}
        message_by_name = {}
        for message in self.messages:
            sum_react = sum(message.number_react)
            if message.name in react_by_name.keys():
                react_by_name[message.name]+=sum_react
            else:
                react_by_name[message.name] = sum_react

            nb_message = len(message.message)
            if message.name in message_by_name.keys():
                message_by_name[message.name]+=nb_message
            else:
                message_by_name[message.name] = nb_message


        data = pd.DataFrame(columns = ['Nom','Nombre de messages','Total Réactions','Ratio'])

        react_by_name = {k:v for k,v in sorted(react_by_name.items(), key=lambda item : item[1])}
        for key,val in react_by_name.items():
            data = data.append({'Nom':key,'Nombre de messages':message_by_name[key],'Total Réactions':val,'Ratio':val/message_by_name[key]},ignore_index=True)
        print(data)




test = MessengerStat('WED ADA')
test.import_html_file('messenger.html')
test.parse_data()
test.get_react_stat()
            

        

        














