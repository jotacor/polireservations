#!/usr/bin/env python

from config import Config
import datetime
import time
import locale
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, presence_of_element_located
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
config = Config()

def time_spent():
    return int(time.time() - config.start_time)

print(f"Starting: {time_spent()}s")
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
options = Options()
options.add_argument("--headless")
browser = webdriver.Firefox(options=options)
wait = WebDriverWait(browser, 3)


def login():
    print(f"Logging: {time_spent()}s")
    browser.get(config.login)
    browser.find_element(By.ID, 'ContentFixedSection_uLogin_txtIdentificador').send_keys(config.username)
    browser.find_element(By.ID, 'ContentFixedSection_uLogin_txtContrasena').send_keys(config.password + Keys.RETURN)

def book():
    print(f"Booking: {time_spent()}s")
    today = datetime.date.today()
    weekday = time.strptime(config.weekday, "%A").tm_wday
    required_date = today + datetime.timedelta( (weekday-today.weekday()) % 7 )
    required_date = required_date.strftime("%A, %d de %B de %Y").capitalize()

    wait.until(element_to_be_clickable((By.XPATH, "//h4[text()='Reserva de espacios']"))).click()
    wait.until(element_to_be_clickable((By.XPATH, f"//h4[text()='{config.sport}']"))).click()
    try:
        wait.until(element_to_be_clickable((By.XPATH, f"//a[text()='{required_date}']"))).click()
    except:
        print("Weekday to book not found")
        exit(0)

    wait.until(element_to_be_clickable((By.ID, 'ContentFixedSection_uReservaEspacios_uReservaCuadrante_btnReservar')))
    tds = browser.find_elements(By.TAG_NAME, 'td')
    for td in tds:
        if sport_number := td.get_attribute('deccodrecinto'):
            break

    schedule = wait.until(element_to_be_clickable((By.XPATH, f"//img[@id='ContentFixedSection_uReservaEspacios_uReservaCuadrante_img{sport_number}{config.time}00']")))
    return schedule

def confirm(schedule):
    print(f"Confirming: {time_spent()}s")
    schedule.click()
    try:
        browser.switch_to.alert.accept()
    except:
        # print("No light option, continuing...")
        pass
        
    browser.find_element(By.ID, 'ContentFixedSection_uReservaEspacios_uReservaCuadrante_btnReservar').click()
    wait.until(element_to_be_clickable((By.ID, 'ContentFixedSection_uCarritoConfirmar_btnConfirmar')))
    browser.find_element(By.ID, 'ContentFixedSection_uCarritoConfirmar_txtCorreoElectronico').send_keys(config.email)
    browser.find_element(By.ID, 'ContentFixedSection_uCarritoConfirmar_txtRepitaCorreoElectronico').send_keys(config.email)
    browser.find_element(By.ID, 'ContentFixedSection_uCarritoConfirmar_btnConfirmar').click()

def pay():
    print(f"Paying: {time_spent()}s")
    wait.until(element_to_be_clickable((By.ID, 'divImgAceptar')))
    browser.find_element(By.ID, 'inputCard').send_keys(config.credit_number)
    browser.find_element(By.ID, 'cad1').send_keys(config.credit_expiration.split("/")[0])
    browser.find_element(By.ID, 'cad2').send_keys(config.credit_expiration.split("/")[1])
    browser.find_element(By.ID, 'codseg').send_keys(config.credit_cvc)
    browser.find_element(By.ID, 'divImgAceptar').click()
    # Waiting to confirm payment in cell phone
    WebDriverWait(browser, 300).until(element_to_be_clickable((By.XPATH, f"//input[@value='Continuar']"))).click()
    wait.until(presence_of_element_located((By.XPATH, f"//span[@id='ContentFixedSection_lblTitulo']")))
    browser.save_screenshot("/tmp/payment.png")


def main():
    login()
    schedule = book()

    if not schedule.get_attribute("Estado"):
        print(f"Not available: {time_spent()}s")

    if schedule.get_attribute("Estado") == "Libre":
        print(f"Available: {time_spent()}s")
        confirm(schedule)
        pay()

    print(f"End: {time_spent()}s")
    browser.quit()


if __name__ == "__main__":
    main()