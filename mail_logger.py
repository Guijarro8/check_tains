from mailjet_rest import Client


import os

from dotenv import load_dotenv

load_dotenv()


mail_sender = os.environ["MAIL_SENDER"]
mail_reciever = os.environ["MAIL_RECIEVER"]
api_key = os.environ["MAIL_JET_API_KEY"]
api_secret =  os.environ["MAIL_JET_API_KEY_secret"]

def mail_log(text, mail_rec = mail_reciever):
  mailjet = Client(auth=(api_key, api_secret), version='v3.1')
  data = {
    'Messages': [
      {
        "From": {
          "Email": mail_sender,
          "Name": "Pablo"
        },
        "To": [
          {
            "Email": mail_rec,
            "Name": "Pablo"
          }
        ],
        "Subject": "¡Que viene el tren!",
        "TextPart": text,
      }
    ]
  }
  result = mailjet.send.create(data=data)
  return result.status_code == 200