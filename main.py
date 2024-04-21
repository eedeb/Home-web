from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import re
import requests
import os
file_location='/home/'+os.popen('w').read().split('\n')[2].split(' ')[0]
print(file_location)
ip=os.popen('hostname -I')
ip_address=ip.read()
if '.' in ip_address.split(' ')[1]:
    ip_address=ip_address.split(' ')[1]
else:
    ip_address=ip_address.split(' ')[0]

print(ip_address)

app = Flask(__name__)

pattern = r'([a-zA-Z])(\d)'
pattern2 = r'([a-z])([A-Z])'
pattern3 = r'([A-Z])([A-Z])'
pattern4 = r'(\d)([a-zA-Z])'
pattern5= r'([A-Z])'
def google_search(url):
    url=url.replace('+','plus')
    url="https://www.google.com/search?q="+url.replace(' ','+')
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        text_elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div'])
        
        page_text = ' '.join(element.get_text() for element in text_elements)
        page_text=page_text.replace('°', ' degrees ')
        page_text=page_text.replace('\u202f', ' ')
        page_text=page_text.replace('\u203a', ' ')
        page_text=page_text.replace(':00', " o'clock")
        #page_text=page_text.replace('\u', ' ')
        for i in range(0,10):
            page_text = re.sub(pattern, r'\1 \2', page_text)
            page_text = re.sub(pattern2, r'\1 \2', page_text)
            page_text = re.sub(pattern3, r'\1 \2', page_text)
            page_text = re.sub(pattern4, r'\1 \2', page_text)
        page_text=page_text.replace('N F L', 'NFL')
        page_text=page_text.replace('M L B', 'MLB')
        page_text=page_text.replace('N B A', 'NBA')
        page_text=page_text.replace('N H L', 'NHL')
        page_text=page_text.replace('P M', 'pm')
        page_text=page_text.replace('A M', 'am')
        page_text=page_text.replace('\n', ' ')
        #page_text=page_text.split("Featured Snippets")[0]
        page_text=page_text.split("Verbatim")[1]
        #page_text=page_text.split(".")[0]
        #page_text=page_text.split("?")[0]
        page_text=page_text.split("All times are in Eastern Time")[0]
        #page_text=page_text.split("-")[0]
        try:
            if 'def' in url:
                page_text=page_text.split("/")[2]
            pass
        except:
            pass
        page_text=page_text.split("People also ask")[0]
        page_text=page_text.split("Others want to know")[0]
        page_text=page_text.split("More questions")[0]
        if 'degree' in page_text:
            page_text=page_text.replace(' F ', ' fahrenheit ')
        page_text=page_text.replace(' Q ', ' Quarter ')
        page_text=page_text.replace(' Final,', '')
        page_text=page_text.replace(' Sun,', ' Sunday,')
        page_text=page_text.replace(' Mon,', ' Monday,')
        page_text=page_text.replace(' Tue,', ' Tuesday,')
        page_text=page_text.replace(' Wed,', ' Wednesday,')
        page_text=page_text.replace(' Thu,', ' Thursday,')
        page_text=page_text.replace(' Fri,', ' Friday,')
        page_text=page_text.replace(' Sat,', ' Saturday,')
        
        page_text=page_text.replace(' Jan ', ' January ')
        page_text=page_text.replace(' Feb ', ' February ')
        page_text=page_text.replace(' Mar ', ' March ')
        page_text=page_text.replace(' Apr ', ' April ')
        page_text=page_text.replace(' Jun ', ' June ')
        page_text=page_text.replace(' Jul ', ' July ')
        page_text=page_text.replace(' Aug ', ' August ')
        page_text=page_text.replace(' Sep ', ' September ')
        page_text=page_text.replace(' Oct ', ' October ')
        page_text=page_text.replace(' Nov ', ' November ')
        page_text=page_text.replace(' Dec ', ' December ')
        page_text = re.split(r'\.(?=[A-Z])', page_text)[0]
        if 'eather' in url:
            page_text = page_text.split(',')
            page_text[1] = re.split(r'(?<=[a-z])\s(?=[A-Z])', page_text[1])[0]
            page_text=str(page_text[0])+str(page_text[1])
        if 'sex' in page_text or 'fuck' in page_text or 'bitch' in page_text or 'shit' in page_text or ' ass ' in page_text or 'penis' in page_text or 'testicle' in page_text or 'vagania' in page_text or 'boobs' in page_text:
            return ('Response contains inapropriate language.')
        if '...' in page_text or 'www.' in page_text or '.com' in page_text or '.org' in page_text or '.gov' in page_text or '.edu' in page_text or '.io' in page_text:
            return (url)
        return page_text
    else:
        return f"Error: Unable to retrieve content. Status code {response.status_code}"

import announcements
import time
import os
try:
    import CustomChat      
except ModuleNotFoundError:
    os.system('pip install CustomChat')
@app.route('/')
def index():
    return render_template('index.html', announcements=announcements.announce)
@app.route('/process_section1', methods=['POST'])
def google_top():
    input_text = request.form['input_text']
    # Process input_text for section 1
    output_text = google_search(input_text)  # Example: Convert text to uppercase
    return output_text

@app.route('/fetch_announcements')
def fetch_announcements():
    return jsonify(announcements.announce)

@app.route('/process_section2', methods=['POST'])
def cmd_bottom():
    input_text = request.form['input_text']
    os.system('sudo -u elliot espeak -ven-us "'+input_text+'"')
    print(input_text)
    # Process input_text for section 2
    if input_text.lower() == 'clear':
        announcements.announce=[]
        returnvar="cleared"
    elif input_text in announcements.announce:
        announcements.announce.remove(input_text)
        returnvar="removed"
    else:
        announcements.announce.append(input_text)
        returnvar="added"
    file1 = open(file_location+"/Home-web/announcements.py", "w")
    file1.write("announce="+str(announcements.announce))
    file1.close()
    return returnvar


@app.route('/reboot')
def reboot_machine():
    os.system('sudo reboot')  # Adjust command if necessary
    return '', 204

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/chat/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    user_ip = request.remote_addr  # Get the user's IP address
    if user_input == 'reset':
        CustomChat.reset(user_ip)
        return jsonify({'response_1': 'reset', 'response_2': ''})
    else:
        responses = CustomChat.get_response(user_input, user_ip)  # Pass the user's IP address to get_response
        return jsonify({'response_1': responses[0], 'response_2': responses[1]})

if __name__ == '__main__':
    app.run(debug=False,host=ip_address,port=80)



