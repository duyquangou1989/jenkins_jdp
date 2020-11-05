import smtplib
import glob
import os, sys, getopt

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

MY_ADDRESS = 'infrasjenkins@gmail.com'
PASSWORD = 'OCGggvBn7o2nBEMy8KHN7UiKdZfkPrPy'
report_path = '/data/sonarqube/reports'

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def check_file_exist(filename):
    if os.path.isfile(filename):
    	return True
    return False

def latest_file(path):
    list_of_files = glob.glob(path + '/*.docx')
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def main(argv):
    subject_string = ''
    body_path = ''
    try:
        opts, args = getopt.getopt(argv,"hs:b:",["subject=","body_path="])
    except getopt.GetoptError as e :
      print (e)
      print ('')
      sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Fuck.py -s <subject_string> -b <body_mail>')
            sys.exit()
        elif opt in ("-s","--subject"):
            subject_string=arg
        elif opt in ("-b","--body_path"):
            body_path=arg
    #names, emails = get_contacts('/data/scripts/mycontacts.txt') # read contacts
    names, emails = get_contacts('./mycontacts.txt')
    message_template = read_template('predl_template.eml')
    mail_body = open(body_path)
    mail_body = mail_body.read()
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title(),MAIL_BODY=mail_body,PS='PreDL URL: https://pre-dl.dssvti.com')

        # Prints out the message body for our sake
        print(message)
        print('-------')
        msg = MIMEMultipart()
        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']=subject_string
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        #msg.attach(part)
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    main(sys.argv[1:])