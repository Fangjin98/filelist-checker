import argparse
import os
import json
import smtplib

from email.mime.text import MIMEText

USTC_MSTP_SERVER="mail.ustc.edu.cn"
PREV_FILE_LIST = "list.json"

parser = argparse.ArgumentParser(description='File List Check')
parser.add_argument('--dir', type=str, default='.')
parser.add_argument('--config', type=str, default='./config.json')
args = parser.parse_args()

def launch(directory, sender_info, receiver_list):
    current_file_list = {'list':os.listdir(directory)}
    print(current_file_list)
    
    if(os.path.exists(PREV_FILE_LIST)):
        with open(PREV_FILE_LIST,'r+') as f:
            prev_file_list = json.load(f)
            result, diff_list = compare(current_file_list['list'], prev_file_list['list'])
            print(result)
            if result == 'add':               
                print(diff_list)
                notifty(sender_info,receiver_list,diff_list)
            
            f.seek(0)
            f.truncate()
            json.dump(current_file_list, f, indent=4, ensure_ascii=False)
    else:
        print('Init file list')
        with open(PREV_FILE_LIST, 'a+') as f:
            json.dump(current_file_list, f, indent=4, ensure_ascii=False)

        
def compare(current_file_list, prev_file_list):
    current_files= set(current_file_list)
    prev_files=set(prev_file_list)

    if current_files == prev_files:
        return ('equal', [])
    elif len(current_file_list) > len(prev_file_list):
        diff = current_files - prev_files
        return ('add', diff)
    else:
        diff = prev_files - current_files
        return ('remove', diff)

def notifty(sender_info, receiver_list, diff_list, mstp_server=USTC_MSTP_SERVER):
    content='This is an email sent from NAS to notify {} movie(s) have been added during this week: \n'.format(len(diff_list))
    for f in diff_list:
        content+=str(f)
        content+='\n'
    content += '\n'
    content += 'To use NAS, contact fangjin98@mail.ustc.edu.cn for help.' # TODO: add Feishu
    
    print(content)
    
    email_sender=smtplib.SMTP()
    email_sender.connect(mstp_server)
    email_sender.login(sender_info[0], sender_info[1])
    for receiver in receiver_list:
        message =  MIMEText(content,'plain','utf-8')
        message['Subject']='Notify of Movie Updates in the NAS'
        message['From'] = sender_info[0]
        message['To'] = receiver

        email_sender.sendmail(
            sender_info[0],receiver, str(message)
        )
    email_sender.quit()    

if __name__ == "__main__":
    with open(args.config) as f:
        config=json.load(f)
        sender_info= (config['usr'], config['password'])
        receiver_list=config['receiver_list']

    launch(args.dir, sender_info, receiver_list)
 