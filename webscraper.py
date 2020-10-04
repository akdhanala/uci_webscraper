# Akhil D
# webscraper.py


# imports
from registrar import Registrar
import json


def update_course_codes(course_codes_lst : [str]) -> None:
    with open("course_codes.json", "w") as f:
        f.write(json.dumps(course_codes_lst))

def update_course_info(course_dict : {str : [str]}) -> None:
    with open("course_info.json", "w") as f:
        f.write(json.dumps(course_dict))

def run() -> None:
    course_codes = []
    courses_dict = {}
    uci_registrar = Registrar()
    for dept in uci_registrar:
        for code, course_id, course_name, instructor, class_type in dept:
            courses_dict[code] = [course_id, course_name, instructor, class_type]
            course_codes.append(code)
    
    uci_registrar.end_driver()
    
    update_course_codes(course_codes)
    update_course_info(courses_dict)



if __name__ == "__main__":
    run()