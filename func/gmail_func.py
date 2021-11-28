import os
import sys

# receiving emails
import imaplib
import email
import unidecode
from email.header import decode_header

# sending emails
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

FROM_EMAIL  = os.environ["FROM_EMAIL"]
FROM_PWD    = os.environ["FROM_PWD"]
SMTP_SERVER =  os.environ["SMTP_SERVER"]
SMTP_PORT   = os.environ["SMTP_PORT"]

def get_mails(search_keywords):

    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox')

    search = mail.search(None, f'(SUBJECT "{search_keywords}")' )[1][0].split()
    mail_ids = list(map(int, search))

    wish_list = dict()
    emails = dict()

    # get names and email adresses in explicit string values
    for mail_id in mail_ids:
        res, msg = mail.fetch(str(mail_id), '(RFC822)' )
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode email sender
                if len(decode_header(msg.get("From"))) == 1:
                    From, encoding = decode_header(msg.get("From"))[0]
                    explicit_name = unidecode.unidecode(From.split()[0].lower())
                    explicit_address = From
                elif len(decode_header(msg.get("From"))) == 2:
                    From_name, encoding_name = decode_header(msg.get("From"))[0]
                    From_address, encoding_address = decode_header(msg.get("From"))[1]
                    if isinstance(From_name, bytes):
                        From_name = From_name.decode(encoding_name)
                    explicit_name = unidecode.unidecode(From_name.split()[0].lower())
                    if isinstance(From_address, bytes):
                        From_address = From_address.decode('utf-8')
                    explicit_address = From_address.strip()
                else:
                    print("WARNING: too much value to unpack in email headers")
                    sys.exit(1)

        # get the body of each mail
        data = mail.fetch(str(mail_id), '(RFC822)' )
        for response_part in data:
            arr = response_part[0]
            if isinstance(arr, tuple):
                msg = email.message_from_string(str(arr[1],'utf-8'))
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain":
                            email_body = body.strip()
        wish_list[explicit_name] = email_body
        emails[explicit_name] = explicit_address

    names = list(wish_list.keys())

    return names, emails, wish_list

def send_mails(dict_giver_receiver, emails, wish_list):
    #The mail addresses and password
    sender_address = FROM_EMAIL
    sender_pass = FROM_PWD
    for giver in list(dict_giver_receiver.keys()):
        receiver_address = emails[giver]
        receiver = dict_giver_receiver[giver]
        mail_content = f"""
Coucou {str.capitalize(giver)}, tu as tiré au sort {str.capitalize(receiver)} pour le Secret Santa !\n
{str.capitalize(receiver)} a été très sage cette année et si jamais tu es en panne d'idées, {str.capitalize(receiver)} aimerait beaucoup recevoir {wish_list[receiver]} !\n
C'est uniquement à titre indicatif, libre à toi de choisir quelque chose d'autre !\n
Bisous enneigés,\n
Santa Newton \u2764\uFE0F"""
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Secret Santa 2021'   #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
    return None