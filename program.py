"""
Code to scrape University of Queensland program (degree) information
"""
from helpers import get_soup 

class Program:
  """A degree that the university offers
  """

  # program code -- i think its an int
  code: int = 0
  # program title
  title: str = ""
  # program level -- e.g. Bachelor, Bachelor Honours, etc
  level: str = ""
  # total unit value
  units: int = 0
  year: int = 2021

  def __init__(self, code: str):
    self.code = code
    self.update()

  def update(self):
    """Update self based on information scraped from UQ
    """
    if ("acad_prog" not in self.code):
      print("not a program")
      return
    base_url = 'https://my.uq.edu.au{}'.format(str(self.code))
    soup = get_soup(base_url)

    self.title = soup.find(id="program-title").get_text()
    self.level = soup.find(id="program-title").get_text().split(' ')[0].lower()
    self.units = int(soup.find(id="program-domestic-units").get_text())
    self.code = int(self.code[-4:])
