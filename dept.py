# Akhil D
# dept.py


class EmptyDepartmentError(Exception):
    pass


class Dept:

    def __init__(self, dept : str, driver : "selenium webdriver"):
        self._driver = driver
        self._dept_str = dept
    
    def __iter__(self):
        
        class Dept_iter:

            def __init__(self, dept_object : Dept):
                self._dept = dept_object
                try:
                    course_table = self._dept._driver.find_element_by_class_name("course-list")\
                        .find_element_by_tag_name("table")\
                            .find_element_by_tag_name("tbody")
                    self._table_rows = iter(course_table.find_elements_by_tag_name("tr"))

                except:
                    self._dept._driver.back()
                    raise EmptyDepartmentError()

            def __next__(self):
                try:
                    while True:
                        current_row = next(self._table_rows)
                        list_elements = current_row.find_elements_by_tag_name("td")
                        if current_row.find_element_by_class_name("CourseTitle"):
                            details = current_row.find_element_by_class_name("CourseTitle").text.upper().strip().lstrip(self._dept._dept_str)
                            if "(PREREQUISITES)" in details: 
                                details = details.rstrip("(PREREQUISITES)")
                            details = details.split()
                            self._course_id = details[0]
                            self._course_name = " ".join(details[1:])
                        elif len(list_elements) == 17:
                            code = list_elements[0].text
                            class_type = list_elements[1].text 
                            instructor = list_elements[4].text
                            return code, self._dept._dept_str + " " + self._course_id, self._course_name, instructor, class_type 
                except StopIteration:
                    self._dept._driver.back()
                    return StopIteration

            def __iter__(self):
                return self
        
        return Dept_iter(self)