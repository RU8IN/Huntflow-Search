import time
from random import uniform

from HuntflowSearch import HuntflowSearch

class Performs():

    def __init__(self, firefox_profile_link):
        self.huntflow = HuntflowSearch(firefox_profile_link)

    def Perform1(self, email, password, gui_queue, number, tag, must_age, new_status, more_or_less, city, phone_number,
                 keywords):
        self.huntflow.Auth(email, password, gui_queue)
        self.huntflow.ClickMoreVacancies(gui_queue)
        time.sleep(1)
        while self.huntflow.CheckPresenceOfElementByClassName("dashboard-group__more-vacancies-button"):
            try:
                self.huntflow.ClickMoreVacancies(gui_queue)
            except:
                print("Все вакансии видны")
            time.sleep(2)
        self.huntflow.OpenLink(self.huntflow.GetLinkOfVac(number))
        time.sleep(1)

        self.huntflow.ClickOnTag(tag)

        time.sleep(3)

        results = self.huntflow.GetAllCandidatesLinks(gui_queue, new_status, more_or_less, must_age, city, phone_number,
                                                      keywords)
        time.sleep(1)
        with open("Результаты поиска.txt", 'w', encoding='utf-8') as file:
            for name in results:
                file.write(f"{name} {results[name]}\n")
        return

    def Perform2(self, gui_queue, email, password, vacancy_number, message_amount):
        self.huntflow.Auth(email, password, gui_queue)
        time.sleep(2)

        self.huntflow.ClickMoreVacancies(gui_queue)
        time.sleep(1)
        while self.huntflow.CheckPresenceOfElementByClassName("dashboard-group__more-vacancies-button"):
            self.huntflow.ClickMoreVacancies(gui_queue)
            time.sleep(2)

        self.huntflow.OpenLink(self.huntflow.GetLinkOfVac(vacancy_number))
        time.sleep(1)

        actual_amount_of_candidates = self.huntflow.ClickOnTag("Отправить wa", True)

        try:
            print("Clicked on tag")
            time.sleep(15)
            self.huntflow.driver.find_element_by_class_name("root--pbFXB").click()

        except Exception as ex:
            print(ex)

        with open('WhatsAppLinks.txt', 'w', encoding='utf-8') as file:
            whatsapp_links, huntflow_links = self.huntflow.GetAllCandidatesWhatsAppLinks(message_amount)
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

                if self.huntflow.will_stop:
                    break

                self.huntflow.SendMessage(strings[line_number], vacancy_number, self.huntflow.get_photo())
                time.sleep(2 + uniform(0.5, 1.5))

        return

    def Perform3(self, gui_queue, email, password):
        paths = self.huntflow.GetAllResumePaths()
        print(paths)
        self.huntflow.Auth(email, password, gui_queue)
        self.huntflow.ClickMoreVacancies(gui_queue)
        time.sleep(1)
        while self.huntflow.CheckPresenceOfElementByClassName("dashboard-group__more-vacancies-button"):
            self.huntflow.ClickMoreVacancies(gui_queue)
            time.sleep(2)
        for number in paths:
            # print(number)
            # print(self.huntflow.GetLinkOfVac(number))

            time.sleep(1)
            for el in paths[number]:
                if number != "база":
                    number = number.split(' ')[0]
                try:
                    print(el)
                    self.huntflow.OpenLink(self.huntflow.GetLinkOfVac(number))
                    time.sleep(1)
                    self.huntflow.UploadResume(el, number)
                except Exception as ex:
                    print("Произошла ошибка!")
                    print("Текст:")
                    self.huntflow.OpenLink(self.huntflow.GetLinkOfVac(number))
                    time.sleep(1)
                    print(ex)
        return