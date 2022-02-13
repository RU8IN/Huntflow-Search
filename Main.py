
from gui import gui_loop

with open('login_data.txt', 'r', encoding='utf-8') as file:
    email, password, firefox_profile_link = file.readlines()


if __name__ == '__main__':
    gui_loop(email, password, firefox_profile_link)
    print("Exiting Program")
