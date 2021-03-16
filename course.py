"""
Code to scrape University of Queensland course (subject) information
"""
from helpers import get_soup

class Course:
  """
  A subject that is offered by the university
  """

  # whether the course is valid
  valid_internal: bool = False
  # 8 character course code of form ABCD1234
  code: str = ""
  # name of course
  title: str = ""
  # description of course
  description: str = ""
  # unit value of the course
  units: int = 0
  # which semesters course is offered in: 0 for not offered, 1 for offered
  sem1: int = 0
  sem2: int = 0
  summer: int = 0
  # Course prerequisites
  prereq: str = ""
  # Course incompatible
  incomp: str = ""

  # init based on course code with rest populated by scraping
  def __init__(self, code: str):
    if code == "":
      raise ValueError("The course code cannot be empty.")
    else:
      self.code = code
      self.update()
 
  # update self based on information scraped from UQ
  def update(self):
    """Updates self based on information scraped from UQ
    """
    base_url = 'http://www.uq.edu.au/study/course.html?course_code={}'.format(self.code)
    soup = get_soup(base_url)

    if soup is None or soup.find(id="course-notfound"):
      return None

    description = soup.find(
      id="course-summary").get_text().replace('"', '').replace("'", "''")
    # apparent edge case; see STAT2203
    if '\n' in description:
      description = description.split('\n')[0]
    self.description = description
    self.title = soup.find(id="course-title").get_text()[:-11].replace("'","''")
    self.units = int(soup.find(id="course-units").get_text())

    semester_offerings = str(soup.find_all(id="course-current-offerings"))
    if "Semester 1, " in semester_offerings:
      self.sem1 = 1
    if "Semester 2, " in semester_offerings:
      self.sem2 = 1
    if "Summer Semester, " in semester_offerings:
      self.summer = 1

    prereq = soup.find(id = "course-prerequisite")
    if prereq is not None:
      if (type(prereq) != type("")):
        prereq = prereq.get_text()
      self.prereq = prereq

    incomp = soup.find(id = "course-incompatible")
    if incomp is not None:
      incomp = incomp.get_text()
      self.incomp = incomp
    