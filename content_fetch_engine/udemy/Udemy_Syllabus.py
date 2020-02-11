from pyudemy import Udemy
from pymongo import *
import pprint
udemy = Udemy('rRC240H2iJPsEs3xhf08t9oteczzegiiQdjeGcDt', 'xeNDt6vsxRxiOlzGl09ZvcmNzXdLXucBLUHMKQNIWJYJqkbucWjAh2uslTpMFxlX1GCsrOrktcnApxNWpkcWoZElIW20YUkVtAsSbKRwOkarTpX2gNLyUovtIuOKZ3wQ')

def fetch_data(search_for):
    search_term = search_for
    instrution_levels = ['beginner', 'intermediate', 'expert']
    mng_client = MongoClient('localhost', 27017)
    db = mng_client.arjun

    for x in range(0, len(instrution_levels)):
        response = udemy.courses(page=1, page_size=20, search=search_term, ordering='highest-rated', ratings='3', instructional_level=instrution_levels[x])

        #[--------------------- COURSE DETAILS LOOP --------------------------]
        for i in range(0, len(response['results'])):
            '''result = {'course_level': x+1}
            courseCir = udemy.public_curriculum(response['results'][i]['id'])
            courseRew = udemy.course_reviews(response['results'][i]['id'])

            result['course_source'] = 'udemy'
            result['search_term'] = search_term
            result['course_title'] = response['results'][i]['title']
            result['course_link'] = 'https://www.udemy.com' + str(response['results'][i]['url'])
            result['instructor_name'] = response['results'][i]['visible_instructors'][0]['title']
            result['instructor_url'] = 'https://www.udemy.com' + response['results'][i]['visible_instructors'][0]['url']
            
            if str(response['results'][i]['is_paid']) == True:
                result['course_price'] = response['results'][i]['price_detail']['amount']
            else:
                result['course_price'] = 0'''

            courseCir = udemy.public_curriculum(response['results'][i]['id'])
            # CIRRICULUM LOOP
            if i == 0:
                curriculum = {'domain': search_term, 'level': x+1}
                for j in range(0, len(courseCir['results'])):
                    curriculum['chapter_number'] = int(j)
                    curriculum['chapter_title'] = courseCir['results'][j]['title']
                    # curriculum['chapter_description'] = courseCir['results'][j]['description']

                db['syllabus'].insert_one(curriculum)

            # REVIEW LOOP
            '''overall_rating = 0
            for j in range(0, len(courseRew['results'])):
                #print('Review Number: '+str(j))
                #print('Rating: '+str(courseRew['results'][j]['rating']))
                #print('Name: '+courseRew['results'][j]['user']['name'])

                overall_rating += int(courseRew['results'][j]['rating'])
            result['course_rating'] = overall_rating / len(courseRew['results'])
            result['course_rating_count'] = len(courseRew['results'])
            #pprint.pprint(result)
            db['courses'].insert_one(result)'''
        #[--------------------------------------------------------------------]

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
        fetch_data(search_term)

if __name__=='__main__':
    main()