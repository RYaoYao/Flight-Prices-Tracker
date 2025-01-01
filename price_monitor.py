
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv
from pathlib import Path 

def send_email(subject,body,sender,recipients,password): 
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
       smtp_server.ehlo()
       smtp_server.starttls()
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
       smtp_server.quit()
    print("Message sent!")

i=1
while i ==1:
    driver=webdriver.ChromiumEdge()

    driver.get('https://www.kayak.com.ph/flights/MNL-TPE/2025-10-04/2025-10-10?ucs=negisj&sort=bestflight_a')
    time.sleep(20)
    content=driver.page_source
    soup=BeautifulSoup(content,features='html.parser')
    kayak_flight_details=soup.select_one('.Hv20-value:has(div > span)')
    kayak_price = kayak_flight_details.text[1:6].replace(',', '')

    driver.get('https://www.google.com/travel/flights/search?tfs=CBwQAhopEgoyMDI1LTEwLTA0ag0IAhIJL20vMDE5NXBkcgwIAxIIL20vMGZ0a3gaKRIKMjAyNS0xMC0xMGoMCAMSCC9tLzBmdGt4cg0IAhIJL20vMDE5NXBkQAFIAXABggELCP___________wGYAQE&tfu=EgoIABAAGAAgAigB&hl=en&gl=PH')
    time.sleep(20)
    content=driver.page_source
    soup=BeautifulSoup(content,features='html.parser')
    for span in soup('span', attrs={'class': 'hXU5Ud aA5Mwe'}):
        google_flight_price=span.text[1:6].replace(',','')

    cheapest_price = min(int(kayak_price),int(google_flight_price))

    if int(cheapest_price) <= 6500:
        env_path = Path('.')/'.env'
        load_dotenv(dotenv_path= env_path)
        sender = os.getenv('FROM')
        password = os.getenv('PASSWORD')
        subject = "Found cheap flight"
        recipient = os.getenv('TO')
        message = "Found cheap flight for the price of: " + cheapest_price +". at URL:'https://www.kayak.com.ph/flights/MNL-TPE/2025-10-04/2025-10-10?ucs=negisj&sort=bestflight_a"
        send_email(subject,message,sender,recipient,password)
    driver.quit()
    time.sleep(21600)