import xml.etree.ElementTree as ET
import os
from datetime import datetime
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

def send_mail(content,pid):
    msg = MIMEText(content)
    msg["From"] = "<mailId>"
    msg["To"] = "mailId"
    msg["Subject"] = "Zombie process data"
    p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
    p.communicate(msg.as_string()+" process id added "+pid)

stream = os.popen('/opt/rubies/ruby-2.1.10/bin/passenger-status --show=xml')
output = stream.read()
print(output)
process_count= int(ET.fromstring(output).find('process_count').text)
if process_count == 1:
    sys.exit(0)
stream1 = os.popen('/opt/rubies/ruby-2.1.10/bin/passenger-status --show=requests')
zombie_output = stream1.read()
zombie_process_exist = None
for process in ET.fromstring(output).find('supergroups').find('supergroup').find('group').find('processes').findall('process'):
    last_used= int(process.find('last_used').text[:-6])
    print(process)
    da= datetime.fromtimestamp(last_used)
    db= datetime.now()
    total_seconds= (db-da).total_seconds()
    print(total_seconds)
    print(process.find('pid').text)
    pid= process.find('pid').text
    real_memory= int(process.find('real_memory').text)/(1024*1024)
    print(real_memory)
    if real_memory >= 1:
        zombie_process_exist = True
        os.system('kill -9 '+pid)            
    if total_seconds > 600:
        zombie_process_exist = True
        os.system('kill -9 '+pid)
if zombie_process_exist:
    send_mail(zombie_output,pid)          
