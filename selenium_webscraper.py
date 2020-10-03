# Akhil D
# Scrapes the UCI registrar's schedule of classes
import time, json
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


PATH = r"C:\Program Files (x86)\chromedriver.exe"
URL = "https://www.reg.uci.edu/perl/WebSoc"

def grab_values(iterator):
    i = iter(iterator)
    try:
        next(i)
        while True:
            yield next(i).get_attribute("value")
    except StopIteration:
        return None


def grab_course_info(dept, iterator):
    # {code : [name, teacher, type of class]}
    i = iter(iterator)
    try:
        next(i)
        while True:
            value = next(i)
            list_elements = value.find_elements_by_tag_name("td")
            if len(value.find_elements_by_class_name("CourseTitle")) == 1:
                details = value.find_element_by_class_name("CourseTitle").text.upper().strip().lstrip(dept)
                if "(PREREQUISITES)" in details: 
                    details = details.rstrip("(PREREQUISITES)")
                details = details.split()
                course_id = details[0]
                course_name = " ".join(details[1:])
            elif len(list_elements) == 17:
                code = list_elements[0].text
                class_type = list_elements[1].text 
                instructor = list_elements[4].text
                yield code, dept + " " + course_id, course_name, instructor, class_type
                
    except StopIteration:
        return None


def run():
    try:
        driver = webdriver.Chrome(PATH)
        driver.get(URL)
        select = Select(driver.find_element_by_name('Dept'))
        courses_dict = {}
        course_codes = []
        depts = [dept.get_attribute("value") for dept in select.options[1:]]
        for dept in depts:
            select = Select(driver.find_element_by_name('Dept'))
            select.select_by_value(dept)
            driver.find_element_by_name("Submit").click()
            try:
                course_table = driver.find_element_by_class_name("course-list").find_element_by_tag_name("table").find_element_by_tag_name("tbody")
                for code, course_id, course_name, instructor, class_type in grab_course_info(dept, course_table.find_elements_by_tag_name("tr")):
                    courses_dict[code] = [course_id, course_name, instructor, class_type]
                    course_codes.append(code)
            except:
                pass
            driver.back()
    finally:
        with open("course_info.txt", "w") as f:
            f.write(json.dumps(courses_dict))
        with open("course_codes.txt", "w") as f:
            f.write(json.dumps(course_codes))
        driver.quit()

if __name__ == "__main__":
    run()
