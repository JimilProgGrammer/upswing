from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from coursera_course import get_details
import json
import pprint
import pandas as pd
from pymongo import *
from math import ceil

def get_site_file(url):
    """
    url - base url to access desired web file
    """    
    try:
        html = urlopen(url)
        bs = BeautifulSoup(html, 'html.parser')
        return bs
    
    except HTTPError as e:
        print(e)

def fetch_specialization_courses(url, result):
    global final_list
    page_content = get_site_file(url)
    if page_content == None:
        print('The file could not be found')
    else:
        course_title = page_content.find('div', {'class': 'Row_nvwp6p'}).find('h1').get_text()
        enrollment_count = str(page_content.find('div', {'class': 'rc-ProductMetrics'}).find('div').find('span').find('span').get_text())
        enrollment_count = int(enrollment_count.replace(',', ''))
        courses_description = page_content.find('div', {'class': 'content-inner'}).find('p').get_text()
        recent_views = str(page_content.find('div', {'class': 'rc-ProductMetrics'}).find('span').find('span').get_text())
        recent_views = recent_views.replace(' ', '')
        recent_views = int(recent_views.replace(',', ''))

        result['course_title'] = course_title
        result['course_description'] = courses_description
        result['course_recent_views'] = recent_views
        result['course_enrollment_count'] = enrollment_count

        final_list.append(result)

        print(pprint.pprint(result, indent=4))

        courses_collection = page_content.find_all('div', {'class': 'Row_nvwp6p CourseItem p-b-3'})
        for course in courses_collection:
            return_value = get_details('https://www.coursera.org' + str(course.find('a')['href']), {})
            return_value['course_type'] = 'COURSE IN SPECIALIZATION'
            return_value['part_of_specialization'] = result['course_title']
            return_value['course_source'] = 'coursera'
            final_list.append(return_value)
            pprint.pprint(return_value)

def scrapper(search_for):

    global final_list
    final_list = []

    mng_client = MongoClient('localhost', 27017)
    db = mng_client.arjun

    search_term = search_for
    original_search = search_term
    search_term = search_term.replace(' ', '%20')
    page_number = 1
    level_count = {'Beginner': 0, 'Intermediate': 0, 'Advanced': 0, 'Mixed': 0}

    temp_content = get_site_file('https://www.coursera.org/courses?query=' + str(search_term) + '&indices%5Bprod_all_products%5D%5Bpage%5D=1&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&configure%5BclickAnalytics%5D=true')
    results_returned = temp_content.find('h3', {'class': 'rc-NumberOfResultsSection body-2-text'}).find('span').get_text()
    
    num = [int(s) for s in results_returned.split() if s.isdigit()]
    print('Max search results: ' + str(num[0]))
    max_pages = ceil(num[0] / 10)

    while True:

        page_content = get_site_file('https://www.coursera.org/courses?query=' + str(search_term) + '&indices%5Bprod_all_products%5D%5Bpage%5D=' + str(page_number) + '&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&configure%5BclickAnalytics%5D=true')
        page_number += 1
        try:
            discovery_course = page_content.find("ul", \
                                                {'class':'ais-InfiniteHits-list'})
        except AttributeError as e:
            print('Something seems to be missing with the tag')

        if page_content == None:
            print('The file could not be found')
        else:
            courses = page_content.find_all('li', {'class': 'ais-InfiniteHits-item'})
            for course in courses:
                try:
                    result = {}
                    course_difficulty = course.find('span',{'class': 'difficulty'}).\
                    get_text()

                    if course.find('span',{'class': 'partner-name'}):
                        course_partner = course.find('span',{'class': 'partner-name'}).get_text()

                    course_link = 'https://www.coursera.org' + str(course.find('a')['href'])

                    result['course_source'] = 'coursera'
                    result['course_level'] = course_difficulty
                    result['institute_name'] = course_partner
                    result['search_term'] = original_search
                    
                    if course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_98hw3a'}):
                        course_type = course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_98hw3a'}).\
                    get_text()
                        
                    elif course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_ppj89h'}):
                        course_type = course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_ppj89h'}).\
                    get_text()
                        
                    elif course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_a7fx15'}):
                        course_type = course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_ppj89h'}).\
                    get_text()
                        
                    elif course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_56jmnj'}):
                        course_type = course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_ppj89h'}).\
                    get_text()
                        
                    elif course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_w182mu'}):
                        course_type = course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_ppj89h'}).\
                    get_text()
                        
                    #print(f"Course Type: \t {course_type}")
                    result['course_type'] = course_type
                    if course_type == 'COURSE':
                        print(course_link)
                        return_value = get_details(course_link, result)

                        found_list = list(db['courses'].find({'course_title': return_value['course_title']}))
                        if len(found_list) == 1:
                            continue
                        
                        db['courses'].insert_one(return_value)
                        final_list.append(return_value)
                        #pprint.pprint(return_value, indent=4)
                        if course_difficulty in level_count:
                            level_count[course_difficulty] += 1

                    #elif course_type == 'SPECIALIZATION':
                    #    fetch_specialization_courses(course_link, result)
                        
                    #print('\n'+('|')+('<'*3)+('-'*7)+' New Course ' +('-'*7)+('>'*3)+('|')+'\n')
                except AttributeError as e:
                    print(e)

        if page_number < max_pages:
            print('')
        else:
            break
        increment = False
        for x in level_count:
            if level_count[x] < 10:
                increment = True

        if not increment:
            break

    '''df = pd.DataFrame(final_list)
    df.to_csv('coursera.csv')'''
