import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
from dataclasses import dataclass


def read_credentials():
    """ 
    1. Assigns the json file to secrets
    2. Opens json as a f (f could be any name)
    3. Reads the json file and assigns it to keys 
    4. returns the values read
    * with is a context_manager
    """""
    secrets = 'secrets.json'
    with open(secrets) as f:
        keys = json.loads(f.read())
        return keys


@dataclass
class Task:
    name: str
    link: str


class CheckIoSolver:
    """
    1. init is called when object(bot) is created. It initialize the attributes of the class.
       It's like constructor in OOP
    2. These are the attributes  of the class
    """
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.google = "https://www.google.com/"
        self.base_url = "https://checkio.org"
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def main_login(self):
        """
        1. Calls the function to open checkio page
        2. Keeps it open for 3 seconds
        3. Close the page (this is used to clean up the dock memory)
        """
        self.login_to_checkio()
        #links = self.get_islands_links
        self.get_unsolved_tasks_from_island('https://py.checkio.org/station/library/')
        time.sleep(5)
        self.driver.quit()

    def solve_tasks_on_island(self, link_to_island):
        pass

    def get_unsolved_tasks_from_island(self, link_to_island):
        print('debug')
        self.driver.get(link_to_island)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        tasks = soup.find_all(class_='island-tasks__container')
        unsolved_tasks = []
        for task in tasks:
            task_status = task.find(class_='island-tasks__side__sign').get('title')
            if task_status != 'Solved':
                title = task.find(class_='island-tasks__task__title').get('title')
                link = task.find('a').get('href')
                unsolved_tasks.append(Task(title, link))
        print(unsolved_tasks)

    def get_islands_links(self):
        opened_stations = self.driver.find_elements_by_xpath("//div[contains(@class,'map__station_state_opened')]")
        opened_stations_links = []
        for link in opened_stations:
            opened_stations_links.append(link.find_element_by_css_selector('a.map__station__link').get_attribute('href'))
        return opened_stations_links

    def login_to_checkio(self):
        """
        1. Opens checkio page using driver variable
        2. Call function to click on Python option
        3. Call function to login into Python
        """
        self.driver.get(self.base_url)
        self.get_on_python_checkio()
        self.put_credentials_to_form()

    def put_credentials_to_form(self):
        """
        1. Looks for the id_username on the page and send the login value
        2. Keeps the cursor on the user_name field for 1 second
        3. Looks for id_password on the page and stores it in the password_field variable
        4. Sends the password value
        5. Press enter
        """
        try:
            self.driver.find_element_by_id('id_username').send_keys(self.login)
            time.sleep(2)
            password_field = self.driver.find_element_by_id('id_password')
            password_field.send_keys(self.password)
            password_field.submit()
            time.sleep(3)
        except NoSuchElementException:
            print("Exception NoSuchElementException")

    def get_on_python_checkio(self):
        """
        1. Looks for the Python link text adn click it
        2. Waits 2 seconds to do it
        """
        try:
            self.driver.find_element_by_link_text('Python').click()
            time.sleep(2)
        except NoSuchElementException:
            print("incorrect page")


"""
The if if __name__ == '__main__' always go into a project. It will start it
"""
if __name__ == '__main__':
    """
    1. Call the function and stores the value into credentials
    2. Creates a new instance of the class and assigns this object to the local variable bot
       passing the username and password
    3. The object (bot) calls the function main_login()  
    """
    credentials = read_credentials()
    bot = CheckIoSolver(credentials['username'], credentials['password'])
    bot.main_login()
