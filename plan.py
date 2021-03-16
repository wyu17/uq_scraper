"""
Code to scrape University of Queensland program (degree) plan information
"""
from helpers import get_soup


class Plan:
  """A plan for certain courses to be completed in a program (degree)
  """
  # plan code -- i think it might be an int
  code: str = ""
  # plan title
  title: str = ""
  # program code plan is for -- i think it might be an int
  type: str = ""

  def __init__(self, linkCode: str):
    if linkCode == "":
      raise ValueError("Plan code cannot be empty.")
    else:
      self.update(linkCode)

  def update(self, linkCode : str):
    """Updates self based on information scraped from UQ
    """
    base_url = 'https://my.uq.edu.au{}'.format(linkCode)
    soup = get_soup(base_url)

    self.title = soup.find(id = "page-head").find("h1").get_text()
    self.code = linkCode[-10:]
    # Treat specialisations as extended majors
    if ("Extended Major" in self.title or "Specialisation" in self.title):
      self.type = "eMajor"
    elif ("Minor" in self.title):
      self.type = "minor"
    else:
      self.type = "major"
