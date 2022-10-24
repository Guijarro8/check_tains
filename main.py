import requests
import pandas
from bs4 import BeautifulSoup
from mail_logger import mail_log

response = requests.get('https://www.bde.es/bde/es/secciones/convocatorias/')
soup = BeautifulSoup(response.content, 'html.parser')

ofertas_new = []
for i in soup.find(class_="listados texto_subhome"):
    a=i.text
    if len(a)>1:
        offer_list = a.split('\n')
        ofertas_new.append([offer_list[1], offer_list[2]])

ofertas_new = pandas.DataFrame(ofertas_new)
ofertas_new.columns = ["type","offer"]
ofertas_old = pandas.read_csv("ofertas_old.csv")

df = pandas.merge(ofertas_new, ofertas_old, on=['type','offer'], how='left', indicator='Exist')

new_announcement = df[df['Exist']=='left_only'] 
if len(new_announcement)>0:
    a=mail_log(new_announcement.offer.values)

ofertas_new.to_csv ("ofertas_old.csv", index=False)
print('Done')