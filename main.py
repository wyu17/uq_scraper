import mysql.connector as mysql
from helpers import get_soup
from course import Course
from plan import Plan
from program import Program
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

'''
Adds a new course to a mySQL database given a database and a course code string (e.g CSSE2310).
'''
def add_course(db, code):
    course = Course(code)
    mycursor = db.cursor()
    query = "SELECT * FROM courses WHERE code = '{searchCode}'".format(searchCode = code)
    mycursor.execute(query)
    existingCourses = mycursor.fetchall()
    if (len(existingCourses) > 0):
        print(code)
        return
    sql = "INSERT INTO courses (code, title, units, sem1, sem2, summer, prereq, incomp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (course.code, course.title, course.units, course.sem1, course.sem2, course.summer, course.prereq, course.incomp)
    print(val)
    mycursor.execute(sql, val)
    db.commit()

'''
Adds a new degree to a mySQL database given a database and a degree code string (e.g '2451' is the degree code for Computer Science)
'''
def add_degree(db, code):
    program = Program(code)
    mycursor = db.cursor()
    print(program.code)
    query = "SELECT * FROM degrees WHERE dcode = '{searchCode}'".format(searchCode = program.code)
    mycursor.execute(query)
    existingDegrees = mycursor.fetchall()
    if (len(existingDegrees) > 0):
        print(program.code)
        return
    sql = "INSERT INTO degrees (dcode, name, unit, YEAR, level) VALUES (%s, %s, %s, %s, %s)"
    val = (program.code, program.title, program.units, program.year, program.level)
    print(val)
    mycursor.execute(sql, val)
    db.commit()

'''
Adds a new plan to a given database. Takes a degree code string and a major code string (e.g 'CYBERC2451' for Computer Science Cyber Security major)
'''
def add_major(db, dcode, mcode):
    plan = Plan(mcode)
    mycursor = db.cursor()
    query = "SELECT * FROM majors WHERE mcode = '{searchCode}'".format(searchCode = plan.code)
    mycursor.execute(query)
    existingMajors = mycursor.fetchall()
    if (len(existingMajors) > 0):
        print("already exists")
        return
    sql = "INSERT INTO majors (dcode, mcode, type, name) VALUES (%s, %s, %s, %s)"
    val = (dcode, plan.code, plan.type, plan.title)
    print(val)
    mycursor.execute(sql, val)
    db.commit()

'''
Adds a course code to a section present in the database. Takes the degree code, major code and section name of the given section (e.g
Level 1 Compulsory Courses).
'''
def add_code_to_section(db, dcode, mcode, section, code):
    mycursor = db.cursor()
    # Checks if the given course is present in the databse already, and adds it if not
    if (len(code) == 8):
        add_course(db, code)
    query = "SELECT * FROM sectionCodes WHERE section = '{section}' and code = '{code}' and dcode = '{dcode}' and mcode = '{mcode}'".format(
        dcode = dcode, mcode = mcode, section = section, code = code)
    mycursor.execute(query)
    existingCourses = mycursor.fetchall()
    if (len(existingCourses) > 0):
        print("this code already exists")
        return
    sql = "INSERT INTO sectionCodes (section, code, dcode, mcode) VALUES (%s, %s, %s, %s)"
    val = (section, code, dcode, mcode)
    print(val)
    mycursor.execute(sql, val)
    db.commit()

'''
Adds an equivalent course code to the equivalence database. One example is MATH1051 and MATH1071 being equivalent for credit in many degrees. 
equivCode: an equivalence code e.g ['MATH1051+MATH1071']
codes: an array of codes e.g ['MATH1051', 'MATH1071']
'''
def add_equivalent(db, equivCode, codes):
    mycursor = db.cursor()
    for code in codes:
        query = "SELECT * FROM interX WHERE optionCode = '{equivCode}' and code = '{element}'".format(equivCode = equivCode, c = code)
        mycursor.execute(query)
        existingEquivs = mycursor.fetchall()
        if (len(existingEquivs) > 0):
            print("this code already exists")
            return
        add_course(db, code)
        sql = "INSERT INTO interX (optionCode, code) VALUES (%s, %s)"
        val = (equivCode, code)
        print(val)
        mycursor.execute(sql, val)
        db.commit()

'''
Takes a BeautifulSoup object obtained from UQ's new domain (future-students.uq.edu.au), scrapes all sections from this page and adds them
to the database, associating each section with the appropriate degree and major code.
When type = 0, scrapes all sections, while when type = 1, scrapes only the core courses. 
'''
def scrape_new_program(db, soup, dcode, majorCode, type):
    min = 0
    max = 0
    mycursor = db.cursor()
    allSections = 0
    rules = soup.find_all(class_ = "part__rule part__rule--auxiliary")
    for rule in rules:
        constraintsQuery = "SELECT * FROM constraints WHERE dcode = '{dcode}' AND constraintColumn = '{constraintColumn}'".format(
        dcode = dcode, constraintColumn = rule.get_text())
        mycursor.execute(constraintsQuery)
        existingConstraints = mycursor.fetchall()
        if (len(existingConstraints) == 0):
            sql = "INSERT INTO constraints (dcode, constraintColumn) VALUES (%s, %s)"
            val = (dcode, rule.get_text())
            mycursor.execute(sql, val)
            db.commit()
    if (type == 0):
        allSections = soup.find_all(class_ = "program-rules__part part selection-list")
    else:
        allSections = soup.find_all(id = "part-A")
    for section in allSections:
        title = section.find(class_ = "part__title").get_text()
        ruleselection = section.find(class_ = "part__rule part__rule--selection").get_text()
        extractedInts = [int(s) for s in ruleselection.split() if s.isdigit()]
        if (len(extractedInts) > 1):
            min = extractedInts[0]
            max = extractedInts[1]
        else:
            min = extractedInts[0]
            max = extractedInts[0]
        sectionsQuery = "SELECT * FROM sections WHERE dcode = '{searchCode}' AND mcode = '{mcode}' AND section = '{section}'".format(
            searchCode = dcode, mcode = majorCode, section = title)
        mycursor.execute(sectionsQuery)
        existingSections = mycursor.fetchall()
        print(existingSections)
        if (len(existingSections) == 0):
            sql = "INSERT INTO sections (dcode, mcode, section, min, max) VALUES (%s, %s, %s, %s, %s)"
            val = (dcode, majorCode, title, min, max)
            mycursor.execute(sql, val)
            db.commit()
        row = section.find_all(class_ = "selection-list__row curriculum-reference")
        for rowCode in row:
            referenceCode = rowCode.find(class_ = "curriculum-reference__code").get_text()
            if (len(referenceCode) == 8):
               add_code_to_section(db, dcode, majorCode, title, referenceCode) 
        equivGroup = section.find_all(class_ = "selection-list__row equivalence-group")
        for equiv in equivGroup:
            equivArray = []
            rowCode = equiv.find_all(class_ = "selection-list__row curriculum-reference")
            for rowCode in rowCode:
                curRefCode = rowCode.find(class_ = "curriculum-reference__code").get_text()
                equivArray.append(curRefCode)
            #Need to remove individual codes that got added previously
            for code in equivArray:
                sql = "DELETE FROM sectionCodes where dcode = %s and code = %s"
                val = (dcode, code)
                mycursor.execute(sql, val)
                db.commit()
            joinedEquiv = '+'.join(equivArray)
            add_equivalent(db, joinedEquiv, equivArray)
            add_code_to_section(db, dcode, majorCode, title, joinedEquiv)

''' Adds the sections for all majors of a given degree code (from the new UQ domain only)'''
def add_plan_section_new(db, dcode):
    mycursor = db.cursor()
    query = "SELECT mcode FROM majors WHERE dcode = '{searchCode}'".format(searchCode = dcode)
    mycursor.execute(query)
    existingMajors = mycursor.fetchall()
    #Scrape the page for each major
    for major in existingMajors:
        majorString = str(major)
        formattedMajor = majorString[2:len(majorString)-3]
        url = "https://my.uq.edu.au/programs-courses/requirements/plan/" + formattedMajor
        opts = Options()
        opts.headless = True
        driver = webdriver.Firefox(options=opts)
        driver.get(url)
        soup_file = driver.page_source
        soup = BeautifulSoup(soup_file)
        scrape_new_program(db, soup, dcode, formattedMajor, 0)
        driver.quit()

''' Adds the sections for the core courses of a given degree code (from the new UQ domain only)'''
def add_core_course_new(db, course):
        url = "https://my.uq.edu.au/programs-courses/requirements/program/" + course
        opts = Options()
        opts.headless = True
        driver = webdriver.Firefox(options=opts)
        driver.get(url)
        soup_file = driver.page_source
        soup = BeautifulSoup(soup_file)
        scrape_new_program(db, soup, course, "CORECO" + course, 1)
        driver.quit()

'''
Takes a BeautifulSoup page obtained from UQ's old domain of a degree's requirements page, (e.g https://my.uq.edu.au/programs-courses/program_list.html?acad_prog=2461) 
and the associated degree code, scrapes all majors and sections from this page and adds them to the database, 
associating each section with the appropriate degree and major code.

Note 1: Uses the major details already existing in the database, meaning that first the names and codes of all majors will need to obtained (this can be found
by searching on the UQ website)

Note 2: this will probably not work on all pages as some pages are laid out inconsistently: you may have to modify this function to get it to work or do some
manual formatting of the data.
'''
def scrape_course_page_old(db, soup, dcode):
    planList = soup.find_all(class_ = "planlist")
    majorName = ""
    newSectionName = ""
    min = 0
    max = 0
    mycursor = db.cursor()
    for plan in planList:
        planName = plan.find_all('h1')
        for headingName in planName:
            majorName = headingName.get_text().replace('(', '')
            majorName = majorName.replace('&', ' and ')
            majorName = majorName.replace(')', '')
        query = "SELECT mcode FROM majors WHERE name = '" + majorName + "' AND dcode = '" + dcode + "'"
        mycursor.execute(query)
        existingMajors = mycursor.fetchall()
        if (len(existingMajors) > 0):
            for major in existingMajors:
                majorCode = major[0]
                courselist = plan.find_all(class_ = "courselist")
                increment = 2
                for course in courselist:
                    # Some pages don't use paragraphs to hold units, might need to be modified
                    units = course.find_all('p')
                    # Different pages may use strong tags instead of bold tags or some other variation to represent the section name
                    sectionName = course.find_all('b')
                    for section in sectionName:
                        newSectionName = section.get_text()
                    for paragraph in units:
                        if (paragraph.get_text() is not None):
                            paragraphText = paragraph.get_text()
                            boldText = paragraph.find_all('b')
                            #Remove bolded numbers becaues bolded numbers don't contain unit information and cause issues parsing units
                            for bold in boldText:
                                paragraphText = paragraphText.replace(bold.get_text(), "")
                            extractedInts = [int(s) for s in paragraphText.split() if s.isdigit()]
                            if (len(extractedInts) > 1):
                                min = extractedInts[len(extractedInts) - 2]
                                max = extractedInts[len(extractedInts) - 1]
                            elif (len(extractedInts) == 1):
                                min = extractedInts[0]
                                max = extractedInts[0]
                    existingSectionsQuery = "SELECT * FROM sections WHERE dcode = '{searchCode}' AND mcode = '{mcode}' AND section = '{section}'".format(
                    searchCode = dcode, mcode = majorCode, section = newSectionName)
                    mycursor.execute(existingSectionsQuery)
                    existingSections = mycursor.fetchall()
                    # If a section with the same name doesn't exist add it to the database with name unchanged
                    modifiedSectionName = None
                    if (len(existingSections) == 0):
                        modifiedSectionName = newSectionName
                     # If there is an existing section increment the section name and add a new section with the same name but an increment
                    else:
                        modifiedSectionName = newSectionName + " " + str(increment)
                        increment+=1 
                    sql = "INSERT INTO sections (dcode, mcode, section, min, max) VALUES (%s, %s, %s, %s, %s)"
                    val = (dcode, majorCode, modifiedSectionName, min, max)
                    print(val)
                    mycursor.execute(sql, val)
                    db.commit()
                    # Look for links because all courses link to their course page
                    links = course.find_all('a', href=True)
                    for link in links:
                        sectionCodesQuery = "SELECT * FROM sectionCodes WHERE code = '{code}' AND section = '{section}' AND dcode = '{dcode}' AND mcode = '{mcode}'".format(
                        code = link.get_text(), section = modifiedSectionName, dcode = dcode, mcode = majorCode)
                        mycursor.execute(sectionCodesQuery)
                        existingSectionCodes = mycursor.fetchall()
                        # Filters out superscript links like [3]
                        if (len(existingSectionCodes) == 0 and ']' not in link.get_text()):
                            sql = "INSERT INTO sectionCodes (section, code, dcode, mcode, options) VALUES (%s, %s, %s, %s, %s)"
                            val = (modifiedSectionName, link.get_text(), dcode, majorCode, 0)
                            print(val)
                            mycursor.execute(sql, val)
                            db.commit()
    #Need to remove tabs and newlines from the scrape
    query = "update sectionCodes set code = replace(code, '\t', '')"
    mycursor.execute(query)
    db.commit()
    query = "update sectionCodes set code = replace(code, '\n', '')"
    mycursor.execute(query)
    db.commit()

db = mysql.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "classes"
)