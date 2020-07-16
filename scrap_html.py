from bs4 import BeautifulSoup
import re

file = open('messenger.html')
bs = BeautifulSoup(file.read(),'html.parser')

react_by_name = {}
for first_div in bs.find_all('div',{'class':'_1t_p clearfix'}):

    name = first_div.find('img',{'class':'img','height':'32','width':'32'})
    if name==None:
        name = first_div.find('h5')
        name = 'NONE' if name==None else name.text
    else:
        name = name['alt']

    message_text = first_div.find_all('span',{'class':'_3oh- _58nk'})
    if message_text!=None:
        for single_message in message_text:
            print(name,end=' : ')
            print(single_message.text,end='')

    message_audio = first_div.find_all('a',{'aria-label':"Message vocal"})
    if message_audio!=None:
        for single_message in message_audio:
            print(name,end=' : ')
            print("Audio",end='')

    nb_react = first_div.find('span',{'class':re.compile('_4kf5 _4kf6.*')})
    if nb_react!=None:
        print(' NDR : '+ nb_react.text)
        if name in react_by_name.keys():
            react_by_name[name]+=int(nb_react.text)
        else:
            react_by_name[name]=int(nb_react.text)
    print()
    

for key,val in react_by_name.items():
    print(key,' : ',val)
    







