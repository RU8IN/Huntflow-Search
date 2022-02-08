import os
import queue
import shutil
import time
from random import uniform
from threading import Thread

import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
import re

# Entering email and password

with open('login_data.txt', 'r', encoding='utf-8') as file:
    email, password, firefox_profile_link = file.readlines()


# MainClass
class HuntflowSearch():
    def __init__(self):
        self.huntflow_url = "https://huntflow.ru/my/recruit-online#applicants"
        self.user_agent = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
        self.options = webdriver.FirefoxOptions()
        self.options.set_preference("general.useragent.override", self.user_agent)
        self.options.set_preference("dom.webdriver.enabled", False)

        self.options.headless = False

        # self.user_profile_path = f"C:/Users/{os.environ.get('USERNAME')}/AppData/Roaming/Mozilla/Firefox/Profiles/eupfatba.default"
        # self.user_profile_path = f"C:/Users/Milena/AppData/Roaming/Mozilla/Firefox/Profiles/99h8vs9e.default-release"
        self.user_profile_path = firefox_profile_link.replace("\\", "/")
        self.firefox_profile = webdriver.FirefoxProfile(self.user_profile_path)

        self.all_vacancies = None
        self.will_stop = False

    def Auth(self, email, password, gui_queue):
        self.driver = webdriver.Firefox(firefox_profile=self.firefox_profile,
                                        executable_path="geckodriver.exe",
                                        options=self.options
                                        )
        # self.driver.implicitly_wait(60)
        self.driver.get(self.huntflow_url)
        time.sleep(1)
        try:
            if self.driver.current_url == "https://huntflow.ru/my/recruit-online#applicants":
                gui_queue.put('Authed')
                return
            gui_queue.put('Entering email')
            email_el = self.driver.find_element_by_id("email")
            email_el.clear()
            email_el.send_keys(email)
            time.sleep(1)
            gui_queue.put('Entering password')
            password_el = self.driver.find_element_by_id("password")
            password_el.clear()
            password_el.send_keys(password)
            time.sleep(1)
            self.driver.find_element_by_class_name("button_big").click()
            time.sleep(1)
        except:
            pass
        gui_queue.put('Authed')
        return

    def GetAllResumePaths(self):
        path = "Резюме/"
        folder_list = dict.fromkeys(os.listdir(path))
        for folder in folder_list:
            filelist = []
            for root, dirs, files in os.walk(f"Резюме/{folder}"):
                for file in files:
                    filelist += [os.path.abspath(f"Резюме/{folder}/{file}")]
            folder_list[folder] = filelist
        return folder_list

    def OpenLink(self, url: str):
        self.driver.get(url)
        return

    def ClickMoreVacancies(self, gui_queue):
        more_vacancies = self.driver.find_element_by_class_name("dashboard-group__more-vacancies-button")
        more_vacancies.click()
        time.sleep(1)
        gui_queue.put("Clicked on 'More Vacancies' Button")
        return

    def CheckPresenceOfElementByClassName(self, class_name: str):
        try:
            self.driver.find_element_by_class_name(class_name)
            return True
        except:
            return False

    def CheckPresenceOfElementByXpath(self, xpath: str):
        try:
            self.driver.find_element_by_xpath(xpath)
            return True
        except:
            return False

    def SetHuntflowStatusWithLink(self, status: str, huntflow_link):
        try:
            self.OpenLink(huntflow_link)
        except:
            if "whatsapp.com" in self.driver.current_url():
                time.sleep(1)
                self.driver.switch_to_alert().dismiss()
                time.sleep(1)
            self.OpenLink(huntflow_link)
        time.sleep(1)
        self.driver.find_element_by_class_name("applicant-card-vacancy-status__button").click()
        time.sleep(0.45)
        all_ahrefs = self.driver.find_elements_by_class_name("nav-list-item")
        for el in all_ahrefs:
            if f"{status.lower()}" in el.find_element_by_tag_name("a").get_attribute("textContent").lower():
                el.find_element_by_tag_name("a").click()
                break
        time.sleep(0.8)
        return

    def SendMessage(self, string: str, number: str, photo_path=''):

        name, link, huntflow_link = string.split(' ')
        self.driver.get(link)
        # self.driver.get("https://web.whatsapp.com/send?phone=79646111456")
        WebDriverWait(self.driver, 90).until_not(
            EC.presence_of_element_located((By.XPATH, "//*[@class='_35Zb2']")))

        # time.sleep(10)
        k = 0
        time.sleep(3)
        print('Прогрузилось')
        print(f'Кандидат: {name}  |  Ссылка: {huntflow_link}')
        try:
            # WebDriverWait(self.driver, 90).until(
            #     EC.presence_of_element_located((By.XPATH, "//*[@class='_2lMWa']")))
            pole = self.driver.find_elements_by_xpath("//*[@class='_13NKt copyable-text selectable-text']")[1]
            print('Поле найдено')
            pole.click()
            pole.clear()
            pole.send_keys(f"{name}/{number}")
            time.sleep(0.3 + uniform(0.2, 0.6))
            pole.send_keys(Keys.TAB)
            time.sleep(0.5)
            time.sleep(0.3 + uniform(0.2, 0.6))
            time.sleep(1)

            # Отправка фото
            # if photo_path != '':
            #     self.driver.find_element_by_xpath(
            #         "/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[1]/div[2]/div/div").click()
            #     time.sleep(0.5)
            #     self.driver.find_element_by_xpath(
            #         "/html/body/div/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div[1]/div[2]/div/span/div["
            #         "1]/div/ul/li[1]/button/input").send_keys(
            #         photo_path)
            #     time.sleep(0.5)
            #     self.driver.find_element_by_xpath(
            #         "/html/body/div/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div").click()
            #     pole.send_keys(photo_path)
            #     time.sleep(0.5)

            pole.send_keys(Keys.ENTER)
            time.sleep(0.4)
            pole.send_keys(Keys.ENTER)
            time.sleep(1)
            pole.clear()
            self.SetHuntflowStatusWithLink("Отправлен WA", huntflow_link)
            k += 1
        except Exception as ex:
            print('Поле ввода не найдено, статус "Позвонить"')
            print(str(ex))
            self.SetHuntflowStatusWithLink("Позвонить", huntflow_link)
        time.sleep(1)
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[4]/ul/li/div[1]/div[1]/div/div/div/form/div[2]/div[2]/div[7]/div/button[1]").click()
        time.sleep(1.5)
        return

    def GetAllVacanciesFromMainPage(self):
        table = self.driver.find_element_by_class_name("dashboard-group__data").find_element_by_tag_name(
            "tbody").find_elements_by_tag_name("tr")
        resume_links = {}
        for el in table:
            resume_links[el.find_element_by_tag_name("a").get_attribute(
                "textContent")] = f'{el.find_element_by_tag_name("a").get_attribute("href")}'
        resume_links['база'] = 'https://huntflow.ru/my/recruit-online#applicants'
        return resume_links

    def GetLinkOfVac(self, number="01"):
        if not self.all_vacancies:
            self.all_vacancies = self.GetAllVacanciesFromMainPage()
        link = ''
        for el in self.all_vacancies:
            if number in el:
                link = self.all_vacancies[el]
        return link

    def ClickOnTag(self, tag="В работе", need_amount=False):
        time.sleep(1)
        tag_span = self.driver.find_elements_by_xpath(
            f"//*[@class='item--2IRYQ']")

        for current_tag in tag_span:
            print(current_tag.get_attribute("textContent").lower())
            if tag.lower() in current_tag.get_attribute("textContent").lower():
                current_tag.click()

        amount_of_candidates = int(tag_span.find_element_by_tag_name("span").text) if need_amount else None

        # try:
        #     tag_span.click()
        # except:
        #     Прокрутка направо, пока не поулчится нажать на определённый тег
            # while True:
            #     try:
        #             tag_span.click()
        #             break
        #         except:
        #             self.driver.find_element_by_xpath("//*[contains(@class, 'rightArrowButton--2A5Ca')]").click()
        #             time.sleep(0.5)
        # if need_amount:
        #     return amount_of_candidates
        return

    def GetAllCandidatesWhatsAppLinks(self, quantity):
        all_candidates = self.driver.find_elements_by_class_name("card--9vbZ_")

        all_whatsapp_links = {}
        all_candidate_links = {}

        k = 0
        for candidate in all_candidates:
            candidate.click()
            time.sleep(0.7)
            try:
                candidate_link = self.driver.find_element_by_class_name("active--2F4Qd").find_element_by_tag_name(
                    "a").get_attribute("href")
                a = self.driver.find_element_by_class_name("applicant-card-title__header").get_attribute(
                    "textContent").split(' ')
                if len(a) == 31:
                    name = a[17].replace('\n', '').replace(' ', '')
                elif len(a) == 30:
                    name = a[16].replace('\n', '').replace(' ', '')

                if "фио" in name.lower():
                    self.SetHuntflowStatus("позвонить")
                    time.sleep(1)
                    continue
                all_whatsapp_links[
                    name] = f'{self.driver.find_element_by_class_name("applicant-card__phone-apps").find_elements_by_tag_name("a")[0].get_attribute("href")} '
                all_candidate_links[name] = candidate_link
                k += 1
            except:
                continue
            if k > int(quantity) + 5:
                print("breaked")
                break
            print(name)
            time.sleep(1)
        return [all_whatsapp_links, all_candidate_links]

    def SetHuntflowStatus(self, status: str):
        time.sleep(1)
        self.driver.find_element_by_class_name("applicant-card-vacancy-status__button").click()
        time.sleep(0.7)
        all_ahrefs = self.driver.find_elements_by_xpath("//*[@class='root--3eQvm statusesList--pqhkh']")
        for el in all_ahrefs:
            if f"{status.lower()}" in el.find_element_by_class_name("itemName--1FsvZ").get_attribute(
                    "textContent").lower():
                time.sleep(0.7)
                el.click()
                break
        time.sleep(0.5)
        self.driver.find_element_by_xpath("//*[@class='button--2kgzJ button']").click()
        return

    def GetAllCandidatesLinks(self, gui_queue, new_status, more_or_less, must_age, city, phone_number, keywords):
        all_candidates = self.driver.find_elements_by_class_name("card--9vbZ_")
        # all_candidates = self.driver.find_elements_by_class_name("root--pbFXB")

        all_candidate_links = {}

        for candidate in all_candidates:
            candidate.click()
            cont = False
            time.sleep(0.6)
            candidate_link = self.driver.find_element_by_class_name("active--2F4Qd").find_element_by_tag_name(
                "a").get_attribute("href")
            name = self.driver.find_element_by_class_name("title--zagSG").get_attribute(
                "textContent").split(' ')[5].strip() if not 'Скрыто' else ''
            print(name)
            # Получение возраста человека
            if must_age != '':
                try:
                    age = \
                    self.driver.find_element_by_xpath("//*[@class='dd--1rRof']").el.get_attribute("textContent").split(
                        ' ')[0]
                    print(age)
                    if more_or_less == True:
                        if int(age) < int(must_age):
                            continue
                    else:
                        if int(age) > int(must_age):
                            continue
                    # all_dds = self.driver.find_element_by_class_name(
                    #     "dd--1rRof").find_elements_by_tag_name("dd")
                    # for el in all_dds:
                    #     if "лет" in el.get_attribute("textContent") or "года" in el.get_attribute("textContent"):
                    #         age = el.get_attribute("textContent").split(' ')[0]
                    # if age is None:
                    #     continue
                except:
                    continue

            # Получение города проживания
            if city != '' or keywords != '':
                try:
                    desc = self.driver.find_element_by_class_name(
                        "resume-external-block__description").get_attribute("textContent")
                    # С помощью этой строчки регистр keywords не имеет значения
                    desc_city = desc.split()
                    desc_city = [el.lower() for el in desc_city]
                    # print(desc)
                    if keywords != '':
                        try:
                            keywords = keywords.split(', ')
                        except:
                            pass
                        for word in keywords:
                            if word.lower() not in desc.lower():
                                cont = True

                    if city != '':
                        candidate_city = city.lower() in desc.lower()
                        # if not candidate_city:
                        #     continue
                        print(name, candidate_city, age)

                except Exception as ex:
                    gui_queue.put(ex)
                    continue

            # Поулчение номера телефона
            if phone_number != '':
                try:
                    phone_number = phone_number.replace(' ', '').replace('+', '').replace('-', '')
                    candidate_phone = self.driver.find_element_by_class_name(
                        "applicant-card__link_phone_link").get_attribute("textContent")
                    candidate_phone = candidate_phone.replace(' ', '').replace('+', '').replace('-', '')
                    if phone_number not in candidate_phone:
                        continue
                except:
                    continue

            if cont:
                continue

            # Присвоение кандидату нового статуса

            if new_status != '':
                try:
                    self.SetHuntflowStatus(new_status)
                    time.sleep(1)
                except:
                    pass
            all_candidate_links[name] = candidate_link

            time.sleep(1)
        return all_candidate_links

    def UploadResume(self, path_to_resume: str, number):
        try:
            time.sleep(1)
            try:
                self.driver.find_element_by_id("plusAction").click()
            except:
                time.sleep(3)
                self.driver.find_element_by_id("plusAction").click()
            time.sleep(0.7)
            all_lis = self.driver.find_element_by_class_name("js-select-action").find_element_by_tag_name(
                "ul").find_elements_by_tag_name("li")
            for li in all_lis:
                if "добавить кандидата" in li.find_element_by_tag_name("a").get_attribute("textContent").lower():
                    WebDriverWait(self.driver, 120).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[2]/div[3]/div/div/div[1]/ul/li[2]/a")))
                    li.click()
                    time.sleep(0.8)
                    break
            # self.driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/div[1]/ul/li[2]/a").click()
            self.driver.find_element_by_class_name("applicant-popup-header__files").send_keys(path_to_resume)
            time.sleep(2.5)

            if self.CheckPresenceOfElementByXpath("//*[@class='button js-form-submit']"):
                self.driver.find_element_by_xpath("//*[@class='button js-form-submit']").click()
            else:
                self.driver.find_element_by_xpath(
                    "/html/body/div[9]/div/div/div/div[2]/form/div[2]/div/div/input[2]").click()
                time.sleep(0.7)
                if not os.path.isdir("Неотправленные"):
                    os.mkdir("Неотправленные")
                if not os.path.isdir(f"Неотправленные/{number}"):
                    os.mkdir(f"Неотправленные/{number}")
                shutil.copy2(path_to_resume, f"Неотправленные/{number}")
                os.remove(path_to_resume)
                return
            time.sleep(1)
            if self.CheckPresenceOfElementByXpath("//*[@class='button button_white button_middle']"):
                # Объединение резюме в случае, если есть аналогичное
                self.driver.find_element_by_xpath("//*[@class='button button_white button_middle']").click()
                time.sleep(1)
                self.driver.find_element_by_class_name("form-group").find_element_by_tag_name("button").click()
                time.sleep(0.7)
                self.driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div/button[1]").click()
                time.sleep(1)
        except Exception as ex:
            print(ex)
        time.sleep(0.7)
        try:
            self.driver.find_element_by_xpath("/html/body/div[24]/div/div[2]").click()
        except Exception as ex:
            print(ex)
        if not os.path.isdir("Отправленные"):
            os.mkdir("Отправленные")
        if not os.path.isdir(f"Отправленные/{number}"):
            os.mkdir(f"Отправленные/{number}")
        shutil.copy2(path_to_resume, f"Отправленные/{number}")
        os.remove(path_to_resume)
        return

    def Perform1(self, email, password, gui_queue, number, tag, must_age, new_status, more_or_less, city, phone_number,
                 keywords):
        self.Auth(email, password, gui_queue)
        self.ClickMoreVacancies(gui_queue)
        time.sleep(1)
        while self.CheckPresenceOfElementByClassName("dashboard-group__more-vacancies-button"):
            try:
                self.ClickMoreVacancies(gui_queue)
            except:
                print("Все вакансии видны")
            time.sleep(2)
        self.OpenLink(self.GetLinkOfVac(number))
        time.sleep(1)
        actual_amount_of_candidates = self.ClickOnTag(tag)

        # try:
        #     def ScrollIntoView(element):
        #         actions = ActionChains(driver=self.driver)
        #         actions.move_to_element(element).perform()
        #
        #     visible_amount_of_candidates = self.driver.find_element_by_class_name(
        #         "root--2MJQk").find_elements_by_class_name("link--p2vMM")
        #
        #     while len(visible_amount_of_candidates) != actual_amount_of_candidates:
        #         last_candidate_on_page = \
        #             self.driver.find_element_by_class_name("root--2MJQk").find_elements_by_tag_name("div")[-1]
        #         # ScrollIntoView(last_candidate_on_page)
        #         time.sleep(15)
        #         visible_amount_of_candidates = self.driver.find_element_by_class_name(
        #             "root--2MJQk").find_elements_by_class_name("link--p2vMM")
        # except Exception as ex:
        #     print(ex)

        time.sleep(15)

        results = self.GetAllCandidatesLinks(gui_queue, new_status, more_or_less, must_age, city, phone_number,
                                             keywords)
        time.sleep(1)
        with open("Результаты поиска.txt", 'w', encoding='utf-8') as file:
            for name in results:
                file.write(f"{name} {results[name]}\n")
        return

    def Perform2(self, gui_queue, email, password, vacancy_number, message_amount):
        self.Auth(email, password, gui_queue)
        time.sleep(2)
        # while EC.presence_of_element_located((By.XPATH, "//*[@class='dashboard-group__more-vacancies-button']")):
        #     self.ClickMoreVacancies(gui_queue)
        #     time.sleep(1)

        # while self.CheckPresenceOfElementByClassName("dashboard-group__more-vacancies-button"):
        #     self.ClickMoreVacancies(gui_queue)
        #     time.sleep(2)

        self.ClickMoreVacancies(gui_queue)
        time.sleep(1)
        while self.CheckPresenceOfElementByClassName("dashboard-group__more-vacancies-button"):
            self.ClickMoreVacancies(gui_queue)
            time.sleep(2)

        self.OpenLink(self.GetLinkOfVac(vacancy_number))
        time.sleep(1)

        actual_amount_of_candidates = self.ClickOnTag("Отправить wa", True)

        try:
            print("Clicked on tag")
            time.sleep(2)
            self.driver.find_element_by_class_name("root--pbFXB").click()
            visible_amount_of_candidates = len(
                self.driver.find_elements_by_xpath("//*[@class='root--2MJQk']/*[contains(@class, 'root--pbFXB')]"))
            print(visible_amount_of_candidates, actual_amount_of_candidates)
            while visible_amount_of_candidates != actual_amount_of_candidates:
                last_candidate_on_page = \
                    self.driver.find_elements_by_xpath("//*[@class='root--2MJQk']/*[contains(@class, 'root--pbFXB')]")[
                        -1]
                # last_candidate_on_page.send_keys(Keys.END)
                self.driver.find_element_by_xpath(
                    "//*[@class='layout__list js-layout-sidebar js-applicant-items']").click()
                self.driver.find_element_by_xpath(
                    "//*[@class='layout__list js-layout-sidebar js-applicant-items']").send_keys(Keys.END)
                time.sleep(2.5)
                visible_amount_of_candidates = len(
                    self.driver.find_elements_by_xpath("//*[@class='root--2MJQk']/*[contains(@class, 'root--pbFXB')]"))
                print(visible_amount_of_candidates)
        except Exception as ex:
            print(ex)

        with open('WhatsAppLinks.txt', 'w', encoding='utf-8') as file:
            whatsapp_links, huntflow_links = self.GetAllCandidatesWhatsAppLinks(message_amount)
            for name in whatsapp_links:
                if ' ' in name:
                    name = name.replace(' ', '')
                if '\n' in name:
                    name = name.replace('\n', '')
                if 'фио' in name.lower():
                    continue
                try:
                    string = f"{name} {whatsapp_links[name]} {huntflow_links[name]}\n"
                except Exception as ex:
                    print(ex)
                    pass
                while '  ' in string:
                    string = string.replace('  ', ' ')
                file.write(string)
        time.sleep(3)

        with open('WhatsAppLinks.txt', 'r', encoding='utf-8') as file:
            strings = file.readlines()
            for line_number in range(message_amount):
                # self.will_stop меняется в SendMessage()
                if not self.will_stop:
                    self.SendMessage(strings[line_number], vacancy_number, self.get_photo())
                    time.sleep(2 + uniform(0.5, 1.5))
                else:
                    break
        return

    def Perform3(self, gui_queue, email, password):
        paths = self.GetAllResumePaths()
        print(paths)
        self.Auth(email, password, gui_queue)
        self.ClickMoreVacancies(gui_queue)
        time.sleep(1)
        while self.CheckPresenceOfElementByClassName("dashboard-group__more-vacancies-button"):
            self.ClickMoreVacancies(gui_queue)
            time.sleep(2)
        for number in paths:
            # print(number)
            # print(self.GetLinkOfVac(number))

            time.sleep(1)
            for el in paths[number]:
                if number != "база":
                    number = number.split(' ')[0]
                try:
                    print(el)
                    self.OpenLink(self.GetLinkOfVac(number))
                    time.sleep(1)
                    self.UploadResume(el, number)
                except Exception as ex:
                    print("Произошла ошибка!")
                    print("Текст:")
                    self.OpenLink(self.GetLinkOfVac(number))
                    time.sleep(1)
                    print(ex)
        return

    def get_photo(self):
        if not (os.path.isfile("photo.jpg") or os.path.isfile("photo .png")):
            return ''
        photo_path = os.path.abspath("photo1.jpg") if os.path.isfile("photo1.jpg") else os.path.abspath("photo.png")
        return photo_path


# GUI Function/Loop
def gui_loop():
    gui_queue = queue.Queue()
    sg.theme("DarkAmber")

    gg = [[sg.Text("Номер вакансии: ")],
          [sg.Text("Тег")],
          [sg.Text("Город: ")],
          [sg.Text("Ключевые слова: ")],
          [sg.Text("Номер: ")],
          [sg.Text("Поменять статус на: ")],
          [sg.Text("Желаемый возраст: ")],
          ]
    easy = [
        [sg.Input(key="-VACANCY_NUMBER-")],
        [sg.Input(key="-TAG-", default_text="В работе")],
        [sg.Input(key="-CITY-")],
        [sg.Input(key='-KEY_WORDS-')],
        [sg.Input(key='-PHONE_NUMBER-')],
        [sg.Input(key='-NEW_STATUS-')],
        [sg.Input(key='-MUST_AGE-')],
    ]
    layout1 = [
        [sg.Column(gg, visible=True), sg.Column(easy)],
        [sg.Radio("Больше", group_id=0, key=228), sg.Radio("Меньше", group_id=0)],
        [sg.Submit(), sg.Cancel()]
    ]

    layout2 = [
        [sg.Column([
            [sg.Text("Введите кол-во сообщений: ")],
            [sg.Text("Введите номер вакансии: ")]
        ]),
            sg.Column([
                [sg.Input(key='-MESSAGE_AMOUNT-')],
                [sg.Input(key='-VACANCY_NUMBER_LAY2-')]
            ])],
        [sg.Submit(), sg.Cancel()]
    ]

    layout = [
        [sg.Column(layout1, key="-COL1-"),
         sg.Column(layout2, visible=False, key='-COL2-')],
        [sg.Button("1"), sg.Button("2"), sg.Button("Загрузить резюме", key='-LOAD_RESUME-')],
        [sg.Output(size=(63, 15))]
    ]
    lay = 1
    window = sg.Window('Huntflow Programs', layout)
    app = HuntflowSearch()

    while True:  # The Event Loop
        event, values = window.Read(timeout=100)
        if event in (None, "Exit", "Cancel"):
            app.driver.close()
            app.driver.quit()
            break

        try:
            message = gui_queue.get_nowait()
        except queue.Empty:
            message = None
        if message is not None:
            print(message)

        if event in '12':
            print(event)
            window[f"-COL{lay}-"].update(visible=False)
            lay = int(event)
            window[f"-COL{lay}-"].update(visible=True)

        if event == "Submit" and lay == 1:
            try:
                thread = Thread(target=app.Perform1,
                                args=(email, password, gui_queue, values["-VACANCY_NUMBER-"], values["-TAG-"],
                                      values["-MUST_AGE-"], values["-NEW_STATUS-"], values[228], values['-CITY-'],
                                      values['-PHONE_NUMBER-'], values['-KEY_WORDS-']),
                                daemon=True)
                thread.start()
            except Exception as ex:
                print(ex)
        if event == "Submit0" and lay == 2:
            try:
                thread = Thread(target=app.Perform2,
                                args=(
                                    gui_queue, email, password, values['-VACANCY_NUMBER_LAY2-'],
                                    int(values["-MESSAGE_AMOUNT-"])),
                                daemon=True)
                thread.start()
            except Exception as ex:
                print(ex)

        if event == '-LOAD_RESUME-':
            try:
                thread = Thread(target=app.Perform3,
                                args=(gui_queue, email, password),
                                daemon=True)
                thread.start()
            except Exception as ex:
                print(ex)


if __name__ == '__main__':
    gui_loop()
    print("Exiting Program")
