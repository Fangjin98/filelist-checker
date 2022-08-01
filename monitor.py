import argparse
from calendar import FRIDAY
import email
from glob import glob
import time
import smtplib
import json
from datetime import datetime
from email.mime.text import MIMEText
from unicodedata import name
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

USTC_MSTP_SERVER="mail.ustc.edu.cn"
ONE_DAY_SEC = 60*60*24
FRIDAY = 4

parser = argparse.ArgumentParser(description='Directory monitor')
parser.add_argument('--dir', type=str, default='.')
parser.add_argument('--config', type=str, default='./config.json')
args = parser.parse_args()

is_modified=False
modified_records=[]

class Record:
    def __init__(self,name : str,creation_date : datetime) -> None:
        self.name=name
        self.creation_date=creation_date

    def __str__(self) -> str:
        return 'Name: {} \t Creation date: {}'.format(self.name, str(self.creation_date))

class FileChangeHandler(FileSystemEventHandler):
    def on_moved(self, event):
        pass

    def on_created(self, event):
        global is_modified
        print("The file has been added to {}".format(event.src_path))
        file_name=str.split(event.src_path, '/')[-1]
        creation_date=datetime.now().date()
        modified_records.append(Record(file_name, creation_date))
        is_modified=True

    def on_deleted(self, event):
        pass

def notifty_all(sender_info, receiver_list, mstp_server=USTC_MSTP_SERVER):
    content='This is an email sent from NAS to notify {} movie(s) have been added during this week: \n'.format(len(modified_records))
    for f in modified_records:
        content+=str(f)
        content+='\n'
    content+='\n'
    content+='To use NAS, visit https://dolomite-dancer-619.notion.site/NAS-d538f443b838426a8b465490b5dc1f43 .'
    
    email_sender=smtplib.SMTP()
    email_sender.connect(mstp_server)
    email_sender.login(sender_info[0], sender_info[1])
    for receiver in receiver_list:
        message =  MIMEText(content,'plain','utf-8')
        message['Subject']='Weekly NAS Movie Update'
        message['From'] = sender_info[0]
        message['To'] = receiver

        email_sender.sendmail(
            sender_info[0],receiver, str(message)
        )
    email_sender.quit()

def monitor_notify(directory, sender_info, receiver_list):
    event_handler=FileChangeHandler()
    observer=Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    try:
        global is_modified
        while True:
            time.sleep(ONE_DAY_SEC)
            week_day = datetime.today.weekday()
            if (week_day == FRIDAY) and is_modified:
                notifty_all(sender_info, receiver_list)
                modified_records.clear()
                is_modified=False
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    with open(args.config) as f:
        config=json.load(f)
        sender_info= (config['usr'], config['password'])
        receiver_list=config['receiver_list']

    monitor_notify(args.dir, sender_info, receiver_list)
 