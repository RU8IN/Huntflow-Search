import queue
from threading import Thread
import PySimpleGUI as sg

# GUI Function/Loop
from Performs import Performs


def gui_loop(email, password, firefox_profile_link):
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
    app = Performs(firefox_profile_link)

    while True:  # The Event Loop
        event, values = window.Read(timeout=100)
        if event in (None, "Exit", "Cancel"):
            app.huntflow.driver.close()
            app.huntflow.driver.quit()
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
    pass