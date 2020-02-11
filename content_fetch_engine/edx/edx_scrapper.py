import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pprint
from pymongo import *
import re

def scrapper(search_for):

    mng_client = MongoClient('localhost', 27017)
    db = mng_client.arjun

    browser = webdriver.Firefox()
    search_term = search_for
    search_term = search_term.replace(' ', '+')
    browser.get('https://www.edx.org/course?search_query=' + search_term + '&course=all')
    time.sleep(15)

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(10)

    search_page_content = BeautifulSoup(browser.page_source, 'html.parser')
    courses = search_page_content.find_all('a', {'class': 'course-link'})
    #courses = ['https://www.edx.org/course/quantum-machine-learning-2']

    for course in courses:

        result = {}
        course_url = str(course['href'])
        course_url = course_url.replace('v2/', '')
        result['course_url'] = course_url
        if course_url == 'https://www.edx.org/course/microsoft-professional-capstone-artificial-intelligence-3':
            continue
        print(course_url)
        browser.get(course_url)
        time.sleep(20)

        page_content = BeautifulSoup(browser.page_source, 'html.parser')

        if page_content.find('h1', {'class':'course-intro-heading'}) and page_content.find('h1', {'class':'course-intro-heading'}).find('span'):
            course_title = page_content.find('h1', {'class':'course-intro-heading'}).find('span').get_text()
        elif page_content.find('h1', {'class':'course-intro-heading mb-2'}) and page_content.find('h1', {'class':'course-intro-heading mb-2'}).find('span'):
            course_title = page_content.find('h1', {'class':'course-intro-heading mb-2'}).find('span').get_text()
        elif page_content.find('h1', {'class':'course-intro-heading mb-2'}):
            course_title = page_content.find('h1', {'class':'course-intro-heading mb-2'}).get_text()

        if page_content.find('img', {'class':'header-image'}):
            result['thumbnail_url'] = page_content.find('img', {'class':'header-image'})['src']

        if page_content.find('img', {'class':'course-org-logo'}):
            course_org_logo = page_content.find('img', {'class':'course-org-logo'})['src']
        course_description = page_content.find('div', {'class': 'course-description'}).find('div').find('p').get_text()
        
        if page_content.find('div', {'class': 'course-info-list'}):
            what_you_learn = page_content.find('div', {'class': 'course-info-list'}).get_text()
            what_you_learn = what_you_learn.replace('\xa0', '')
        else:
            continue
        
        if page_content.find('h3', {'class': 'course-info-heading mb-4'}):
            certificate_price = page_content.find('h3', {'class': 'course-info-heading mb-4'}).find('span').get_text()
        elif page_content.find('h3', {'class': 'course-info-heading'}):
            certificate_price = page_content.find('h3', {'class': 'course-info-heading'}).get_text()
        
        temp = re.findall(r'\d+', certificate_price) 
        res = list(map(int, temp))

        if len(res) > 0:
            certificate_price = res[0] * 68.65
        else:
            certificate_price = -1
        
        result['course_title'] = course_title
        result['course_description'] = course_description
        result['search_term'] = search_for
        #result['course_link'] = course_url
        result['course_source'] = 'edx'
        result['skills_learned'] = what_you_learn
        #result['prerequisites'] = prerequisites
        result['institute_image_url'] = course_org_logo
        result['certificate_price'] = certificate_price

        # Instructors section
        if page_content.find('div', {'class': 'instructor-list no-gutters'}):
            instructors = page_content.find('div', {'class': 'instructor-list no-gutters'}).find_all('div', {'class': 'instructor-card-wrapper'})
            for instructor in instructors:
                #print(instructor)
                #result['instructor_image_url'] = instructor.find('div', {'class': 'instructor-image-wrapper'}).find('img', {'class':'rounded-circle w-100'})['src']
                result['instructor_name'] = instructor.find('a', {'class': 'name font-weight-bold'}).get_text()
                result['instructor_description'] = instructor.find('div', {'class': 'title font-italic'}).get_text()
            

        if page_content.find('ul', {'class': 'list-group list-group-flush px-4 w-100'}):
            course_table = page_content.find('ul', {'class': 'list-group list-group-flush px-4 w-100'}).find_all('li', {'class': 'list-group-item d-flex align-items-baseline row px-0'})
        else:
            continue
        #print(course_table)
        for info in course_table:
            labels = info.find_all('div', {'class': 'col'})
            #print('Len: ' + str(labels))
            key = str(labels[0].find('span').get_text())

            if key in ["Institution"]:
                result['institute_name'] = labels[1].find('a').get_text()
                result['institute_url'] = labels[1].find('a')['href']

            elif key in ["Length:"]:
                value = str(labels[1].find('span').get_text())
                res = [int(i) for i in value.split() if i.isdigit()]
                result['duration'] = round(sum(res) / len(res), 2)
                for x in res:
                    value = value.replace(str(x), '')
                value = value.replace(' ', '')
                length_in = value.lower()
                result['duration_in'] = length_in

            elif key in ["Subject:"]:
                result['subject'] = labels[1].find('a').get_text()

            elif key in ["Level:"]:
                value = labels[1].get_text()
                if value == 'Introductory':
                    level = 1
                elif value == 'Intermediate':
                    level = 2
                elif value == 'Advanced':
                    level = 3
                result['course_level'] = level

            elif key in ["Language:"]:
                result['course_language'] = labels[1].get_text()

            elif key in ["Price:"]:
                value = labels[1].find('p').find('span').get_text()
                if 'free' in value or 'FREE' in value:
                    course_price = 0
                else:
                    value = value.replace(' USD', '')
                    course_price = int(value)
                result['course_price'] = course_price

        db['courses'].insert_one(result)

def main():
    search_term_list = [
        'artificial intelligence',
        'big data analytics',
        'blockchain',
        'cloud computing',
        'cyber security',
        'data mining',
        'deep learning',
        'face recognition',
        'image processing',
        'IoT',
        'machine learning',
        'network security',
        'neural network',
        'smart grid'
    ]
    for search_term in search_term_list:
        print(search_term)
        scrapper(search_term)

if __name__=="__main__":
    main()