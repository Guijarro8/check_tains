import time
import pandas

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


from bs4 import BeautifulSoup

from mail_logger import mail_log

#Inicio estancia de firefox con las siguientes opciones y lanzo la peticion de la web con la fecha selecionada
options = Options()
options.headless = True
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

driver = webdriver.Firefox(executable_path=r"C:\Users\pablo.guijarro\Downloads\geckodriver-v0.32.0-win32\geckodriver",options=options)

driver.get("https://www.sj.se/en/kop-resa/valj-resa/V%C3%A4xj%C3%B6%20station/Copenhagen%20Airport/2022-12-17")

# Cargamos la pagina un poco guarramente, porque no consigo la peticion exacta, bajando poco a poco

time.sleep(4)
driver.execute_script("window.scrollBy(0,document.body.scrollHeight/6)")
time.sleep(2)
driver.execute_script("window.scrollBy(0,document.body.scrollHeight/6)")
time.sleep(2)
driver.execute_script("window.scrollBy(0,document.body.scrollHeight/6)")
time.sleep(2)
driver.execute_script("window.scrollBy(0,document.body.scrollHeight/6)")
time.sleep(2)
driver.execute_script("window.scrollBy(0,document.body.scrollHeight/6)")
time.sleep(2)
driver.execute_script("window.scrollBy(0,document.body.scrollHeight/6)")
time.sleep(2)
driver.execute_script("window.scrollBy(0,document.body.scrollHeight/6)")
time.sleep(2)

#formateamos el Html de la pagina
soup = BeautifulSoup(driver.page_source, 'html.parser')


# Encontramos los elementos "not_availabe", "work_planned" & "priced"
data_sj_new = pandas.DataFrame()
data_sj_new['not_available']= [len(soup.findAll(class_="MuiTypography-root MuiTypography-h3 MuiTypography-alignRight css-9yyfpl"))]
data_sj_new['work_planned'] = [len(soup.findAll(class_="MuiTypography-root MuiTypography-body1 MuiTypography-alignRight css-esvwf1"))]
data_sj_new['priced'] = [len(soup.findAll(class_="MuiTypography-root MuiTypography-h1static css-75sez1"))]

#toma el historico
data_sj_old = pandas.read_csv(r"C:\Users\pablo.guijarro\Documents\available_train_check\data_sj_old.csv")

dicc_tipo_viajes = {
    'not_available':'no disponibles',
    'work_planned':'con obras',
    'priced':'con precio',
}

# Chequea la historia  y manda el mail si cambios
if ~data_sj_old.equals(data_sj_new):
    mail=''
    for i in data_sj_new.columns:
        if (data_sj_new[i] != data_sj_old[i])[0]:
            mail = mail + f"Cambios en  viajes {dicc_tipo_viajes[i]} antes había {data_sj_old[i][0]} y ahora {data_sj_new[i][0]} \n" 
    a = mail_log(mail)
    b = mail_log(mail,mail_rec="hallsteperez@gmail.com")
    c = mail_log(mail,mail_rec="guijarromatos@gmail.com")

data_sj_new.to_csv(r"C:\Users\pablo.guijarro\Documents\available_train_check\data_sj_old.csv", index=False)
driver.close()