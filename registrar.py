# Akhil D
# registrar.py


# imports
import time, json
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from dept import Dept, EmptyDepartmentError


class Registrar:
    """Object representing the UCI registrar. Be sure to quit the driver when finished."""

    PATH = r"C:\Program Files (x86)\chromedriver.exe"
    URL = "https://www.reg.uci.edu/perl/WebSoc"
    NUM_DEPTS = 147

    def __init__(self):
        self._depts = self.depts()
        self._set_up_driver()

    def __str__(self):
        return "Registrar object"
    
    def __repr__(self):
        return "Registrar()"
    
    def __getitem__(self, dept : str):
        if type(dept) is not str:
            raise TypeError(f"Registar.__getitem__ : {dept} not of type str")
        elif dept not in self._depts:
            raise KeyError(dept)

        select = Select(self._driver.find_element_by_name('Dept'))
        select.select_by_value(dept)
        self._driver.find_element_by_name("Submit").click()
        return Dept(dept, self._driver)

    
    def __iter__(self):
        
        class Registrar_iter:

            def __init__(self, registrar_object : Registrar):
                self._registrar = registrar_object
                self._depts = iter(self._registrar._depts)

            def __next__(self):
                while True: # Repeats until a department with courses is returned or dept list ends.
                    try:
                        return self._registrar[next(self._depts)]
                    except EmptyDepartmentError: # skips departments with no listed courses
                        pass

            def __iter__(self):
                return self
        
        return Registrar_iter(self)

    def depts(self):
        """Returns a list of departments from a local depts.json file."""
        with open("depts.json", "r") as f:
            list_depts = json.loads(f.read())
        return list_depts
    
    def end_driver(self):
        self._driver.quit()
    
    def _set_up_driver(self):
        self._driver = webdriver.Chrome(self.PATH)
        self._driver.get(self.URL)


if __name__ == "__main__":
    
    # testing Registrar().depts()
    print(Registrar().depts())