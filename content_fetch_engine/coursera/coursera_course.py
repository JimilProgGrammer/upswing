from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

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

def get_details(url, result):

    page_content = get_site_file(url)

    if page_content == None:
        print('The file could not be found')
    else:
        course_title = page_content.find('div', {'class': 'Row_nvwp6p'}).find('h1').get_text()
        course_rating = float(page_content.find('div', {'class': 'Row_nvwp6p'}).find('span', {'class': 'H4_1k76nzj-o_O-weightBold_uvlhiv-o_O-bold_1byw3y2 m-l-1s m-r-1 m-b-0'}).get_text())
        course_rating_count = str(page_content.find('div', {'class': 'P_gjs17i-o_O-weightNormal_s9jwp5-o_O-fontBody_56f0wi m-r-1s color-white'}).find('span').get_text())
        course_rating_count = course_rating_count.replace(' ', '')
        course_rating_count = course_rating_count.replace(',', '')
        course_rating_count = int(course_rating_count.replace('ratings', ''))

        if page_content.find('div', {'class': 'partnerBanner_np2ice-o_O-Box_120drhm-o_O-displayflex_poyjc'}) and page_content.find('div', {'class': 'partnerBanner_np2ice-o_O-Box_120drhm-o_O-displayflex_poyjc'}).find('img'):
            result['institute_image_url'] = str(page_content.find('div', {'class': 'partnerBanner_np2ice-o_O-Box_120drhm-o_O-displayflex_poyjc'}).find('img')['src'])

        review_count = str(page_content.find('div', {'class': 'reviewsCount'}).find('span').get_text())
        review_count = review_count.replace(' ', '')
        review_count = review_count.replace(',', '')
        review_count = int(review_count.replace('reviews', ''))

        enrollment_count = str(page_content.find('div', {'class': 'rc-ProductMetrics'}).find('div').find('span').find('span').get_text())
        enrollment_count = int(enrollment_count.replace(',', ''))

        skills_section = page_content.find_all('span', 'Pill_56iw91 m-r-1s m-b-1s')
        skills_learned = []
        for x in skills_section:
            skills_learned.append(x.find('span').find('span').get_text())

        result['course_title'] = course_title
        result['course_rating'] = course_rating
        result['course_rating_count'] = course_rating_count
        result['course_review_count'] = review_count
        result['course_enrollment_count'] = enrollment_count
        result['skills_learned'] = skills_learned
        
        courses_description = page_content.find('div', {'class': 'content-inner'}).find('p').get_text()
        recent_views = str(page_content.find('div', {'class': 'rc-ProductMetrics'}).find('span').find('span').get_text())
        recent_views = recent_views.replace(' ', '')
        recent_views = int(recent_views.replace(',', ''))
        stats = page_content.find_all('h2', {'class': "H2_1pmnvep-o_O-weightNormal_s9jwp5-o_O-fontHeadline_1uu0gyz m-x-2 m-b-0"})
        stat_list = []
        stat_text = ['started_new_career', 'career_benefit', 'got_pay_increase']
        for stat in stats:
            percent = str(stat.get_text())
            percent = int(percent.replace('%', ''))
            stat_list.append(percent)
            #print(percent)
        reviews = page_content.find_all('div', {'class': 'review'})
        review_list = []
        for review in reviews:
            review_list.append(review.find('p', {'class': 'TopReviewsComment_z4w825 font-sm'}).get_text())

        reviews_author = page_content.find_all('div', {'class': 'review'})
        author_list = []
        for review in reviews_author:
            author_list.append(review.find('span', {'class': "text-uppercase"}).get_text())
        
        #print(courses_description)
        #print(recent_views)

        result['course_description'] = courses_description
        result['course_recent_views'] = recent_views
        result['course_stats'] = {}
        for i in range(0, len(stat_list)):
            result['course_stats'][stat_text[i]] = stat_list[i]
        '''result['course_stats']['started_new_career'] = stat_list[0]
        result['course_stats']['career_benefit'] = stat_list[1]
        result['course_stats']['got_pay_increase'] = stat_list[2]
'''
        if author_list:
            for i in range(0, len(author_list)):
                result['top_review_'+str(i+1)] = {'on': author_list[i], 'comment': review_list[i]}

        instructors = page_content.find_all('div', {'class': 'instructorWrapper_jfe7wu'})
        result['instructors'] = []
        for instructor in instructors:
            temp = {}
            if instructor.find('img'):
                temp['instructor_image_url'] = instructor.find('img')['src']
            if instructor.find('h3').find('a'):
                temp['instructor_name'] = instructor.find('h3').find('a').get_text()
            if instructor.find('div'):
                temp['instructor_description'] = instructor.find('div').get_text()

            result['instructors'].append(temp)
            
        return result
        '''for course in courses:
            try:
                course_title = course.h2.get_text()
                course_rating = course.find('span',{'class': 'ratings-text'}).\
                get_text()
                course_enrollment = course.find('span',{'class': 'enrollment-number'}).\
                get_text()
                course_difficulty = course.find('span',{'class': 'difficulty'}).\
                get_text()
                course_partner = course.find('span',{'class': 'partner-name'}).\
                get_text()
                
                print(f"Course Title: \t {course_title}")
                print(f"Course Rating: \t {course_rating}")
                print(f"Course Enrollment: \t {course_enrollment}")
                print(f"Course Difficulty: \t {course_difficulty}")
                print(f"Course Partner: \t {course_partner}")
                
                if course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_98hw3a'}):
                    course_type = course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_98hw3a'}).\
                get_text()
                    print(f"Course Type: \t {course_type}")
                    
                elif course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_ppj89h'}):
                    course_type = course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_ppj89h'}).\
                get_text()
                    print(f"Course Type: \t {course_type}")
                    
                elif course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_a7fx15'}):
                    course_type = course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_ppj89h'}).\
                get_text()
                    print(f"Course Type: \t {course_type}")
                    
                elif course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_56jmnj'}):
                    course_type = course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_ppj89h'}).\
                get_text()
                    print(f"Course Type: \t {course_type}")
                    
                elif course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_w182mu'}):
                    course_type = course.find('div',{'class': 'productTypePill_vy0uva-o_O-gradientBg_ppj89h'}).\
                get_text()
                    print(f"Course Type: \t {course_type}")
                    
                
                print('\n'+('|')+('<'*3)+('-'*7)+' New Course ' +('-'*7)+('>'*3)+('|')+'\n')
            except AttributeError as e:
                print(e)'''

if __name__=="__main__":
    main()