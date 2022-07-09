import argparse
import email
from glob import glob
import time
import smtplib
import json

from email.mime.text import MIMEText
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

parser = argparse.ArgumentParser(description='Directory monitor')
parser.add_argument('--dir', type=str, default='.')
parser.add_argument('--config', type=str, default='./config.json')
args = parser.parse_args()

is_modified=False
modified_files=[]

class FileChangeHandler(FileSystemEventHandler):
    def on_moved(self, event):
        pass

    def on_created(self, event):
        global is_modified
        print("add {}".format(event.src_path))
        modified_files.append(event.src_path)
        is_modified=True

    def on_deleted(self, event):
        pass

def notifty_all(sender_info, receiver_list):
    ustc_mstp_server="mail.ustc.edu.cn"
    content='This is an email sent from NAS to notify {} movie(s) have been added: \n'.format(len(modified_files))
    for f in modified_files:
        content+=f
        content+='\n'
    
    email_sender=smtplib.SMTP()
    email_sender.connect(ustc_mstp_server)
    email_sender.login(sender_info[0], sender_info[1])

    for receiver in receiver_list:
        message =  MIMEText(content,'plain','utf-8')
        message['Subject']='NAS Movie Update'
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
            time.sleep(1)
            if is_modified:
                notifty_all(sender_info, receiver_list)
                modified_files.clear()
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
 