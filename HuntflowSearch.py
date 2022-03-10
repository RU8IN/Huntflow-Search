import os

import re
import shutil
import time
from random import uniform

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# Entering email and password

# MainClass
class HuntflowSearch():
    def __init__(self, firefox_profile_link):
        self.huntflow_url = "https://huntflow.ru/my/recruit-online#applicants"
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
        self.options = webdriver.FirefoxOptions()
        self.options.set_preference("general.useragent.override", self.user_agent)
        self.options.set_preference("dom.webdriver.enabled", False)

        self.options.headless = False

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
        try:
            time.sleep(1)
            vacancy_number = re.findall(r"y/\d*/f", self.driver.current_url)[0][2:-2]
            green_button = self.driver.find_element_by_xpath(
                f"//*[@class='button button_green js-item-vacancy-connect-button{vacancy_number}']")
            green_button.click()
            all_labels = self.driver.find_elements_by_xpath(
                "//*[@class='root--3eQvm statusesList--pqhkh']/*[@class='itemName--1FsvZ']")

            for label in all_labels:
                if status.split('-')[0].lower() in label.get_attribute("title").lower():
                    label.click()
                    time.sleep(1)

            if "отказ" in status.lower():
                reason = status.split('-')[1]
                all_labels = self.driver.find_elements_by_xpath("//*[@class='root--3eQvm rejectReasonsList--3Hdf-']/*[@class='itemName--1FsvZ']")

                for label in all_labels:
                    if reason.lower() in label.get_attribute("title").lower():
                        label.click()
                        time.sleep(1)
                        break
                self.driver.find_element_by_xpath("//*[@class='button--2kgzJ button']").click()
            else:
                self.driver.find_element_by_xpath("//*[@class='button--2kgzJ button']").click()

        except Exception as ex:
            print(ex)
        return

    def SetHuntflowStatus(self, status: str):

        try:
            time.sleep(1)
            vacancy_number = re.findall(r"y/\d*/f", self.driver.current_url)[0][2:-2]
            green_button = self.driver.find_element_by_xpath(
                f"//*[@class='button button_green js-item-vacancy-connect-button{vacancy_number}']")
            green_button.click()
            all_labels = self.driver.find_elements_by_xpath(
                "//*[@class='root--3eQvm statusesList--pqhkh']/*[@class='itemName--1FsvZ']")

            for label in all_labels:
                if status.split('-')[0].lower() in label.get_attribute("title").lower():
                    label.click()
                    time.sleep(1)

            if "отказ" in status.lower():
                reason = status.split('-')[1]
                all_labels = self.driver.find_elements_by_xpath("//*[@class='root--3eQvm rejectReasonsList--3Hdf-']/*[@class='itemName--1FsvZ']")

                for label in all_labels:
                    if reason.lower() in label.get_attribute("title").lower():
                        label.click()
                        time.sleep(1)
                        break
                self.driver.find_element_by_xpath("//*[@class='button--2kgzJ button']").click()
            else:
                self.driver.find_element_by_xpath("//*[@class='button--2kgzJ button']").click()

        except Exception as ex:
            print(ex)
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
        # self.driver.find_element_by_xpath(
            # "/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[4]/ul/li/div[1]/div[1]/div/div/div/form/div[2]/div[2]/div[7]/div/button[1]").click()
        # time.sleep(1.5)
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
            "//*[contains(@class, 'item--2IRYQ')]")
        actual_amount_of_candidates = None
        visible_amount_of_candidates = None

        for current_tag in tag_span:
            if tag.lower() in current_tag.get_attribute("textContent").lower().strip():
                time.sleep(1)
                actual_amount_of_candidates = int(re.findall("\d+", current_tag.get_attribute("textContent"))[0])
                current_tag.click()
                time.sleep(1)
                break

        try:
            while visible_amount_of_candidates != actual_amount_of_candidates:
                visible_amount_of_candidates = len(self.driver.find_elements_by_xpath("//*[contains(@class, 'root--pbFXB')]"))
                self.driver.find_elements_by_xpath("//*[contains(@class, 'root--pbFXB')]")[-1].click()
                action = webdriver.ActionChains(self.driver)
                action.send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(4)
        except Exception as ex:
            time.sleep(20)
            print("Ошибка в прокрутке кандидатов.")
            print(ex)
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
                name = self.driver.find_element_by_class_name("title--zagSG").get_attribute(
                    "textContent").split(' ')[5].strip()

                if "фио" in name.lower() or "неизвестно" in name.lower():
                    self.SetHuntflowStatus("позвонить")
                    time.sleep(1)
                    continue
                phone_number = re.sub(r"\D", "", self.driver.find_element_by_xpath(
                    "//*[@class='phone--DtMb2 link--1k7bx']").get_attribute("textContent"))
                all_whatsapp_links[
                    name] = f"https://web.whatsapp.com/send?phone={phone_number} "
                all_candidate_links[name] = candidate_link
                k += 1
            except:
                continue
            if k > int(quantity) + 5:
                print("breaked")
                break
            time.sleep(1)
        return [all_whatsapp_links, all_candidate_links]

    def GetAllCandidatesLinks(self, gui_queue, new_status, more_or_less, must_age, city, phone_number, keywords):

        all_candidates = self.driver.find_elements_by_xpath("//*[contains(@class, 'root--pbFXB')]")

        all_candidate_links = {}

        for candidate in all_candidates:
            try:
                candidate.click()
            except selenium.common.exceptions.StaleElementReferenceException:
                print("Произошла ошибка. Нажмите кнопку Submit\n"
                      "(Старый браузер можно закрыть)")

            age = None

            time.sleep(1)
            # https://web.whatsapp.com/send?phone=79656689077

            candidate_link = self.driver.find_element_by_class_name("active--2F4Qd").find_element_by_tag_name(
                "a").get_attribute("href")
            name = self.driver.find_element_by_class_name("title--zagSG").get_attribute(
                "textContent").split(' ')[5].strip()

            # Получение возраста человека
            if must_age != '':
                try:
                    all_dds = self.driver.find_elements_by_xpath("//*[@class='dd--1rRof']")
                    for dd in all_dds:
                        age = re.findall(r"\d* (?:лет|года|год)", dd.get_attribute("textContent"))
                        if age:
                            age = int(re.sub(r"\D*", "", age[0]))
                            break
                    if not age:
                        continue

                    if more_or_less == True:
                        if '-' in must_age:
                            if not (int(must_age.split("-")[0]) <= int(age) <= int(must_age.split("-")[1])):
                                continue
                        elif int(age) < int(must_age):
                            continue
                    else:
                        if '-' in must_age:
                            if not (int(must_age.split("-")[0]) <= int(age) <= int(must_age.split("-")[1])):
                                continue
                        elif int(age) > int(must_age):
                            continue
                except:
                    continue

            # Получение города проживания и проверка на соответствие ключевым словам
            # Объединено в одно условие, потому что просмотр идёт в одном поле + общий except
            if city != '' or keywords != '':

                if city != '':
                    desc = self.driver.find_element_by_class_name(
                        "content--2uXLG").get_attribute("textContent")
                    candidate_city = city.lower() in desc.lower()
                    if not candidate_city:
                        continue

                try:
                    desc = ''
                    all_descriptions = self.driver.find_elements_by_xpath(
                        "//*[@class='resume-external-block__description resume-external-block__description_padding']")
                    all_bold = self.driver.find_elements_by_xpath("//*[@class='resume-external-block__bold']")

                    for i in all_descriptions:
                        desc += i.get_attribute("textContent")
                    for i in all_bold:
                        desc += i.get_attribute("textContent")

                    while '  ' in desc:
                        desc = desc.replace('  ', ' ')
                    if keywords != '':
                        try:
                            keywords = keywords.split(', ')
                        except:
                            pass

                        class ContinueI(Exception):
                            pass

                        try:
                            for word in keywords:
                                if word.lower() not in desc.lower():
                                    raise ContinueI
                        except ContinueI:
                            continue
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

            # Присвоение кандидату нового статуса

            if new_status != '':
                try:
                    self.SetHuntflowStatus(new_status)
                    time.sleep(1)
                except:
                    pass
            all_candidate_links[name] = candidate_link

            time.sleep(1)
            print(name)
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

    def get_photo(self):
        if not (os.path.isfile("photo.jpg") or os.path.isfile("photo .png")):
            return ''
        photo_path = os.path.abspath("photo1.jpg") if os.path.isfile("photo1.jpg") else os.path.abspath("photo.png")
        return photo_path



if __name__ == '__main__':
    pass
