#!/usr/bin/env python

from config import Config
import datetime
import time
import locale
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, presence_of_element_located
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
config = Config()

def time_spent():
    return int(time.time() - config.start_time)

def login(browser):
    print(f"Logging: {time_spent()}s")
    browser.get(config.login)
    browser.find_element(By.ID, 'ContentFixedSection_uLogin_txtIdentificador').send_keys(config.username)
    browser.find_element(By.ID, 'ContentFixedSection_uLogin_txtContrasena').send_keys(config.password + Keys.RETURN)

def book(browser):
    print(f"Booking: {time_spent()}s")
    today = datetime.date.today()
    weekday = time.strptime(config.weekday, "%A").tm_wday
    required_date = today + datetime.timedelta( (weekday-today.weekday()) % 7 )
    required_date = required_date.strftime("%A, %d de %B de %Y").capitalize()

    WebDriverWait(browser, 3).until(element_to_be_clickable((By.XPATH, "//h4[text()='Reserva de espacios']"))).click()
    WebDriverWait(browser, 3).until(element_to_be_clickable((By.XPATH, f"//h4[text()='{config.sport}']"))).click()
    try:
        WebDriverWait(browser, 3).until(element_to_be_clickable((By.XPATH, f"//a[text()='{required_date}']"))).click()
        print(f"Trying to book {config.sport} on {required_date} at {config.time}h ")
    except:
        print(f"Weekday to book not found {required_date}")
        exit(0)

    WebDriverWait(browser, 3).until(element_to_be_clickable((By.ID, 'ContentFixedSection_uReservaEspacios_uReservaCuadrante_btnReservar')))
    tds = browser.find_elements(By.TAG_NAME, 'td')
    for td in tds:
        if sport_number := td.get_attribute('deccodrecinto'):
            break

    schedule = WebDriverWait(browser, 3).until(element_to_be_clickable((By.XPATH, f"//img[@id='ContentFixedSection_uReservaEspacios_uReservaCuadrante_img{sport_number}{config.time}00']")))
    return schedule

def confirm(browser, schedule):
    print(f"Confirming: {time_spent()}s")
    schedule.click()
    try:
        browser.switch_to.alert.accept()
    except:
        print(f"No light option for {config.sport}")
        pass

    browser.find_element(By.ID, 'ContentFixedSection_uReservaEspacios_uReservaCuadrante_btnReservar').click()
    WebDriverWait(browser, 3).until(element_to_be_clickable((By.ID, 'ContentFixedSection_uCarritoConfirmar_btnConfirmar')))
    browser.find_element(By.ID, 'ContentFixedSection_uCarritoConfirmar_txtCorreoElectronico').send_keys(config.email)
    browser.find_element(By.ID, 'ContentFixedSection_uCarritoConfirmar_txtRepitaCorreoElectronico').send_keys(config.email)
    browser.find_element(By.ID, 'ContentFixedSection_uCarritoConfirmar_btnConfirmar').click()

def payment(browser):
    print(f"Paying: {time_spent()}s")
    WebDriverWait(browser, 3).until(element_to_be_clickable((By.ID, 'divImgAceptar')))
    browser.find_element(By.ID, 'inputCard').send_keys(config.credit_number)
    browser.find_element(By.ID, 'cad1').send_keys(config.credit_expiration.split("/")[0])
    browser.find_element(By.ID, 'cad2').send_keys(config.credit_expiration.split("/")[1])
    browser.find_element(By.ID, 'codseg').send_keys(config.credit_cvc)
    browser.find_element(By.ID, 'divImgAceptar').click()
    print(f"Remember to confirm payment in mobile phone if needed")
    browser.save_screenshot("/app/card.png")
    notify(msg=f"Card payment {time_spent()}s", filepath="/app/card.png")
    WebDriverWait(browser, 300).until(element_to_be_clickable((By.XPATH, f"//input[@value='Continuar']"))).click()
    WebDriverWait(browser, 300).until(presence_of_element_located((By.XPATH, f"//span[@id='ContentFixedSection_lblTitulo']")))
    browser.save_screenshot("/app/payment.png")
    notify(msg=f"Payment confirmation {time_spent()}s", filepath="/app/payment.png")

def notify(msg, filepath="/app/payment.png"):
    url = f"https://api.telegram.org/bot{config.telegram_token}/sendPhoto"
    file = {"photo": open(filepath, "rb")}
    data = {"chat_id": config.telegram_chat_id, "caption": msg}
    response = requests.post(url, files=file, data=data)

    if response.status_code == 200:
        print("Photo sent successfully!")
    else:
        print("Failed to send photo. Error:", response.text)

def main():
    print(f"Starting: {time_spent()}s")
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    browser = webdriver.Remote(command_executor=config.selenium)

    login(browser)
    schedule = book(browser)

    if not schedule.get_attribute("Estado"):
        notify(msg=f"Not available {time_spent()}s", filepath="/app/fail.png")

    if schedule.get_attribute("Estado") == "Libre":
        print(f"Available: {time_spent()}s")
        confirm(browser, schedule)
        payment(browser)

    print(f"End: {time_spent()}s")
    browser.quit()


if __name__ == "__main__":
    main()