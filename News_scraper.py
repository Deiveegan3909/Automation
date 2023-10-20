
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import time

now = datetime.datetime.now()
content = ''

def extract_news(url):
    try:
        print('Extracting Hacker News Stories...')
        cnt = ''
        cnt +=('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
        response = requests.get(url)
        time.sleep(3)  # adding a delay of 3 seconds after making a request
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
            cnt += ((str(i+1)+' :: '+ '<a href="' + tag.a.get('href') + '">' + tag.text + '</a>' + "\n" + '<br>') if tag.text != 'More' else '')
        return(cnt)
    except Exception as e:
        print(f"An error occurred: {e}")
        return ''

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content +=('<br><br>End of Message')

print('Composing Email...')
SERVER = 'smtp.gmail.com' # "your smtp server"
PORT = 587 # your port number
FROM =  'rationalthinkerdd@gmail.com' # "your from email id"
TO = 'arrow13115398deiveegan@gmail.com' # "your to email ids"  # can be a list
PASS = 'tjgjfmhjxcdclpaf' # "your email id's password"


msg = MIMEMultipart()
msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO
msg.attach(MIMEText(content, 'html'))

print('Initiating Server...')

try:
    server = smtplib.SMTP(SERVER, PORT)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string())
    print('Email Sent...')
    server.quit()
except Exception as e:
    print(f"An error occurred: {e}")
    
    