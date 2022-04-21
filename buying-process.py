import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

_chrome_path = '/usr/local/bin/chromedriver'
_cpf_generator = "https://www.4devs.com.br/gerador_de_cpf"
_email_generator = "https://www.invertexto.com/gerador-email-temporario"
_xpath_title = '//*[@id="home"]/div[1]/main/div/div[1]/div[2]/div/div/div/div/div/div/div[1]/h1'


class Person:

    def __init__(self, cpf, email, phone, income, birthday, name):
        self.cpf = cpf
        self.email = email
        self.phone = phone
        self.income = income
        self.birthday = birthday
        self.name = name


class TestBuyingProcess:

    def __init__(self, product_url, person):
        self.driver = webdriver.Chrome(_chrome_path)
        self.wait = WebDriverWait(self.driver, 20)
        self.sleep = self.driver.implicitly_wait
        self.product_url = product_url
        self.get = self.driver.get
        self.find_by_id = self.driver.find_element_by_id
        self.find_by_xpath = self.driver.find_element_by_xpath
        self.person = person

    def get_disposable_email(self):
        self.get(_email_generator)
        self.person.email = self.find_by_id("email-input").get_attribute("value")
        print(self.person.email)

    def get_cpf(self):
        self.get(_cpf_generator)
        self.find_by_id("bt_gerar_cpf").click()
        self.sleep(10)
        cpf = self.find_by_id("texto_cpf").text
        if cpf:
            self.person.cpf = cpf
        print(cpf)

    def find_and_click_id(self, id):
        self.find_by_id(id).click()

    def find_and_click(self, xpath):
        self.find_by_xpath(xpath).click()

    def find_and_send_keys_xpath(self, xpath, keys):
        self.find_by_xpath(xpath).send_keys(keys)

    def find_and_send_keys_id(self, id, keys):
        self.find_by_id(id).send_keys(keys)

    def go_to_product(self):
        self.get(self.product_url)
        self.find_and_click_id('productRequest')

    def fill_email_form(self):
        self.sleep(2)
        self.find_and_send_keys_xpath("//input[@id='input-128']",
                                      self.person.email)

        self.find_and_click("//*[@id='submit']")

    def fill_first_form(self):

        self.sleep(2)

        form_fields = [
            ["input-168", self.person.name],
            ["input-174", self.person.cpf],
            ["input-177", self.person.birthday],
            ["input-180", self.person.phone],
            ["input-184", self.person.income],
        ]

        for field, key in form_fields:
            self.find_and_send_keys_id(field, key)

        self.find_and_click("//*[@id='input-188']")

        element = self.find_by_xpath("//*[@id='home']/div[1]/main/div/div[1]/div["
                                     "2]/div/div/div/div/div/div/div[2]/div["
                                     "1]/div/div/form/div/div/div/div/div[9]/button/span")

        self.driver.execute_script("arguments[0].click();", element)

        self.sleep(10)

    def simulation(self):
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, _xpath_title), 'Simulação'))

        element = self.find_by_xpath(
            "//*[@id='home']/div[1]/main/div/div[1]/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/form/div/div/div/div/div[6]/button/span[1]")

        self.driver.execute_script("arguments[0].click();", element)

        self.sleep(10)

    def fill_second_form(self):
        self.wait.until(EC.text_to_be_present_in_element((By.XPATH, _xpath_title), 'Informações Adicionais'))

    def buy_product(self):
        steps = [
            # self.get_disposable_email(),
            self.get_cpf(),
            self.go_to_product(),
            self.fill_email_form(),
            self.fill_first_form(),
            self.simulation(),
            self.fill_second_form(),
            self.sleep(4)
        ]

        for step in steps:
            step


if __name__ == '__main__':
    import random
    import string

    m = random.randint(13, 324)
    surname = "".join([random.choice(string.ascii_letters) for _ in range(6)])

    mateus = Person("91362197033", f"mateus.costa.novo{m}@franq.com.br",
                    "48996632325", "10000", "13081992", f"Mateus {surname} Costa")

    TestBuyingProcess("http://localhost:8080/pb/fran-tavares/emprestimos/104",
                      mateus).buy_product()