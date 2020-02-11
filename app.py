# [------------------------------------START IMPORTING FILES------------------------------------------]
from __future__ import division
from content_fetch_engine import udemy, coursera, edx, youtube
# [---------------------------------------END IMPORTING FILES-----------------------------------------]

# [------------------------------------START IMPORTING LIBRARIES--------------------------------------]
from googletrans import Translator
import logging as logger
import urllib.request
import urllib.parse
import random as r
import argparse
import smtplib
import uuid
import os
import datetime
from flask_apscheduler import APScheduler
from flask import Flask, jsonify, request, Response
'''from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,
    create_refresh_token,
    jwt_refresh_token_required
)'''
from pymongo import MongoClient
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import json
import repo
import random
# [---------------------------------------END IMPORTING LIBRARIES-------------------------------------]
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = u"C:/Users/yashs/Documents/arjun/flask/ArjunBot.json"

class Config(object):
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.debug = True
app.config.from_object(Config())
app.config['SECRET_KEY'] = 'super-secret'

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

#jwt = JWTManager(app)

# [------------------------------------START CHATBOT FUNCTIONS----------------------------------------]
def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    f = open("SessionPath.txt","a+")
    f.write("Session Path :: {}\n".format(session))
    f.close
    for text in texts:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)

        return response.query_result.fulfillment_text

def Neel_Bot(botName,sessionID,question):
    #Converting to english
    translator = Translator(service_urls=['translate.google.com'])
    convertedPlaintext = translator.translate([question], dest='en')
    answer=detect_intent_texts(botName, sessionID, [convertedPlaintext[0].text], u"0")
    return answer

def getAnswer(question,UserId):
    chatbot_name = "ArjunBot"
    project_id = "web-search-cd9e4"
    UserQuestion = question.replace('+',' ')
    sessionID = UserId
    answer = Neel_Bot(project_id, sessionID, UserQuestion)
    return answer
# [---------------------------------------END CHATBOT FUNCTIONS---------------------------------------]

# [------------------------------------START SEND EMAIL-----------------------------------------------]
def send_email(user, pwd, recipient, subject, body):
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        logger.debug('successfully sent the mail')
        return "1"
    except Exception as e: 
        print(e)
        return "0"

def SendOTPOverEmail(email):
	try:
		otp = str(r.randint(10000, 99999))
		#manandoshi1607@gmail.com
		subject = "Email Verification | A.R.J.U.N"
		body = """
	    		Hi,

	    		Thanks for creating a new account on A.R.J.U.N, and welcome :)

	    		The final step to create your account is to verify your email address. 
	    		Your OTP is : """+otp+"""</b>
	    		Once that's done, you're all set.

	    		Regards,
	    		Tech Militia
	    		"""
		emailRes = send_email("ayreonvendor1@gmail.com", "ayreonvendor123",email, subject, body)
		if(emailRes==1):
			emailResponseStatus = {}
			emailResponseStatus["req_status"] = emailRes
			emailResponseStatus["OTP"] = otp
		else:
			emailResponseStatus = {}
			emailResponseStatus["req_status"] = 0
			emailResponseStatus["OTP"] = otp
		return str(otp)
	except Exception as e:
		print(e)
		return ""

# [------------------------------------END SEND EMAIL-------------------------------------------------]

# [------------------------------------START SEND SMS-------------------------------------------------]
def sendSMS(apikey, numbers, sender, message):
    params = {'apikey': apikey, 'numbers': numbers, 'message' : message, 'sender': sender}
    f = urllib.request.urlopen('https://api.textlocal.in/send/?'+ urllib.parse.urlencode(params))
    return (f.read(), f.code)

def sendOTPtoPhone(phoneNo):
    #Send the request

    message = 'Hi this is Neel. Your OTP is:: '+str(r.randint(1, 9))
    resp, code = sendSMS('ucbTyQZmpS4-DGo19AnCvnd1qWjqLrhI2LWeRNZLPN', phoneNo, 'TXTLCL', message)
    logger.debug(resp)
    if(resp):
        return resp
    else:
        return "0"
# [------------------------------------END SEND SMS---------------------------------------------------]

# [---------------------------------------START LOGIN PAGE--------------------------------------------]
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.username
    
@app.route("/auth", methods=["Post"])
def authenticate():
    username = request.args.get("username")
    password = request.args.get("password")

    dbObj = repo.OhlcRepo()
    data = dbObj.find_record_with_limit("users", {"username":username}, 1)
    if not data:
        return(jsonify({'data':None,'error':"Username Doesn't Exist"}))
    else:
        if username == data[0]["username"] and password == data[0]["password"]:
            ret = {
                'message': "Auth Successful."
            }
            return jsonify(ret),200
        else:
            return(jsonify({'data':None,'error':"Username Doesn't Match"}))

# [-----------------------------------------END LOGIN PAGE-----------------------------------------]
#[--------------------------------------Fuzzy function-------------------------------------------------]
def fuzzify(param1,param2):
   # New Antecedent/Consequent objects hold universe variables and membership
   # functions
   ip1 = ctrl.Antecedent(np.arange(0, 11, 1), 'ip1')
   ip2 = ctrl.Antecedent(np.arange(0, 11, 1), 'ip2')
   tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

   # Auto-membership function population is possible with .automf(3, 5, or 7)
   ip1.automf(3)
   ip2.automf(3)

   # Custom membership functions can be built interactively with a familiar,
   # Pythonic API
   tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
   tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
   tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])
   rule1 = ctrl.Rule(ip1['poor'] | ip2['poor'], tip['low'])
   rule2 = ctrl.Rule(ip2['average'], tip['medium'])
   rule3 = ctrl.Rule(ip1['good'] | ip2['good'], tip['high'])
   tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
   tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
   # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
   # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
   tipping.input['ip1'] = float(param1)
   tipping.input['ip2'] = float(param2)

   # Crunch the numbers
   tipping.compute()
   res=tipping.output['tip']
   print(res)
   return(res*4.0)

#[--------------------------------------Recommending personalised courses-------------------------------------------------]
@app.route('/get_personalised_courses', methods=['GET'])
def group_by_current_role():
    username = request.args.get('username')
    domain = request.args.get('domain')
    ob = repo.OhlcRepo()

    user_record = list(ob.find_record_with_limit('users', {'username': username}, 1))
    user_record = user_record[0]
    current_role = user_record['current_role']
    _id = str(user_record['_id'])
    
    total_courses_done = len(user_record['courses'])
    domain_course_count = 0
    for course in user_record['courses']:
        if course['domain'] == domain:
            domain_course_count += 1
    user_record['domain_inclination'] = round(domain_course_count / total_courses_done * 10, 2)

    records = list(ob.find_records_with_query('users', {'current_role': current_role}))

    community_records = [i for i in records if not (str(i['_id']) == _id)] 
    filtered_records = []

    for another_user in community_records:
        total_courses_done = len(another_user['courses'])
        domain_course_count = 0
        for course in user_record['courses']:
            if course['domain'] == domain:
                domain_course_count += 1
        another_user['domain_inclination'] = round(domain_course_count / total_courses_done * 10, 2)
        another_user['inclination_diff'] = int(abs(another_user['domain_inclination'] - user_record['domain_inclination']))

    fuzzy_result = {}
    user_courses = []
    for another_user in community_records:

        count = 0
        # Academic background
        academic_meta = []
        for degrees in another_user['academics']:
            academic_meta.append(degrees['institute_name'] + " : " + degrees['name'])

        # Courses background
        course_meta = []
        for courses in another_user['courses']:
            course_meta.append(courses['title'] + " : " + courses['domain'])

        # Interests
        interested_domain = another_user['interests']['domain']
        interested_goal = another_user['interests']['goal']

        # Compare with user_record
        for degrees in user_record['academics']:
            if str(degrees['institute_name'] + " : " + degrees['name']) in academic_meta:
                count+=1

        for courses in user_record['courses']:
            user_courses.append(str(courses['title'] + " : " + courses['domain']))
            if str(courses['title'] + " : " + courses['domain']) in course_meta:
                count += 1

        if user_record['interests']['domain'] == interested_domain:
            count += 1
        if user_record['interests']['goal'] == interested_goal:
            count += 1

        another_user['similarity_count'] = count

    # Continue with fuzzy logic
    for another_user in community_records:
        fuzzy_result[another_user['username']] = fuzzify(10-another_user['inclination_diff'], another_user['similarity_count']/2)

    return_list = []
    for keyy, value in sorted(fuzzy_result.items(), key=lambda item: item[1], reverse=True):
            print("%s: %s" % (keyy, value))
            return_list.append({'username': keyy, 'fuzz_score': value})
    missing_courses = []
    for result in return_list:
        records = list(ob.find_record_with_limit('users', {'username': result['username']}, 1))
        for course in records[0]['courses']:
            if course['title'] + " : " + course['platform'] not in user_courses and course['domain'] == domain:
                temp = list(ob.find_record_with_limit('courses', {'course_title': course['title'], 'course_source': course['platform']},1))
                temp[0]['_id'] = str(temp[0]['_id'])
                missing_courses.append(temp[0])
    
    return create_json(missing_courses)

# send CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response

@app.route('/unprotected')
def unprotected():
    return jsonify({
        'message': 'This is an unprotected resource.'
    })

@app.route('/protected')
#@jwt_required
def protected():
    return jsonify({
        'message': 'This is a protected resource.',
        'current_identity': str(current_identity)
    })

@app.route('/trending')
def retcourse():
    dict={}
    l=[]
    d={
    'title':'Machine Learning',
    'source':'Coursera',
    'instructor':'Andrew Ng',
    'rating':'4.8',
    'price':'5000',
    'course_link':'https://www.Coursera.com/MachineLearning'
    }
    l.append(d)
    d={}
    d={
    'title':'Machine Learning A-z',
    'source':'Udemy',
    'instructor':'Krill Eremenko',
    'rating':'4.7',
    'price':'640',
    'course_link':'https://www.Udemy.com/MachineLearning A-Z'
    }
    l.append(d)
    d={}
    d={
    'title':'Deep Learning A-z',
    'source':'Udemy',
    'instructor':'Krill Eremenko',
    'rating':'4.9',
    'price':'640',
    'course_link':'https://www.Udemy.com/DeepLearning A-Z'
    }
    l.append(d)
    d={}
    d={
    'title':'Complete Python Bootcamp',
    'source':'Udemy',
    'instructor':'Jose Portilla',
    'rating':'4.7',
    'price':'720',
    'course_link':'https://www.Udemy.com/CompletePythonBootcamp'
    }
    l.append(d)
    d={}
    d={
    'title':'Node.js bootcamp',
    'source':'Edx',
    'instructor':'San Jone',
    'rating':'4.8',
    'price':'700',
    'course_link':'https://www.edx.com/nodejsbootcamp'
    }
    l.append(d)
    d={}
    d={
    'title':'Angular 6',
    'source':'Coursera',
    'instructor':'Krill Eremenko',
    'rating':'4.7',
    'price':'3000',
    'course_link':'https://www.Coursera.com/Angular 6'
    }
    l.append(d)
    d={}
    d={
    'title':'Deep Learning A-z',
    'source':'Udemy',
    'instructor':'Krill Eremenko',
    'rating':'4.9',
    'price':'640',
    'course_link':'https://www.Udemy.com/DeepLearning A-Z'
    }
    l.append(d)
    dict['data']=l
    dict['error']=None
    return(jsonify(dict))

@app.route('/signup',methods=['Post'])
def sign_up():
    form={}
    form['name']=request.args.get("name")
    form['username']=request.args.get("username")
    form['phone']=request.args.get("phone")
    form['password']=request.args.get("password")
    form['country']=request.args.get("country")
    form['state']=request.args.get("state")
    form['city']=request.args.get("city")
    print(form)
    print(type(form))
    #return(jsonify(form))
    un=form['username']
    ob=repo.OhlcRepo()
    user = ob.find_record_with_limit(collection_name="users", query={"username":str(un)}, limit=1)
    print(user)
    if not user:
        """ Successful signup """
        """ OTP Verification for email """
        """ """
        o=SendOTPOverEmail(form['username'])
        form['email_otp']=o
        form['email_verified']=False
        form['searched_keywords'] = []
        form['balance'] = 100.0
        ob.insert_new_record(collection_name="users", insert_doc=form)
        return(jsonify({'data':'Success','error':None}))
    else:
        """ Exception msg: User already exists """
        return(jsonify({'data':None,'error':'username already exists'}))

@app.route('/verify/<username>/<otp>', methods=['Post'])
def check(username,otp):
    #det=request.args   
    ob=repo.OhlcRepo()
    res=ob.find_record_with_limit(collection_name="users",query={"username":str(username)},limit=1)[0]
    print(res,"##")
    if res['email_otp']==otp:
        
        ob.insert_record(collection_name="users",query={"username":username},insert_doc={"$set":{"email_verified":True}})
        return(jsonify({'data':'email verified successfuly','error':None}))
    else:
        return(jsonify({'data':None,'error':'Otp incorrect'}))

@app.route('/<question>/<userid>')
def ArjunBotEndpoint(question, userid):
    if(type(question)!='str'):
        question = str(question)
    if(type(userid)!='int'):
        userid = int(userid)
    question = question.replace('%20',' ')
    answer = getAnswer(question,userid)
    print(type(answer))
    return str(answer)

@app.route('/search/<domain>')
def search(domain):
    # Step 1: Check whether first time search ?
    un = request.args.get("username")
    domain = request.args.get("username")
    # Step 2: 
    pass

@app.route('/welcome')
#@jwt_required
def getdetails():
    un=request.args.get("username")
    ob=repo.OhlcRepo()
    res=ob.find_record_with_limit(collection_name="users", query={"username":str(un)}, limit=1)[0]
    
    print(res)
    if 'academics' not in res.keys():
        return(jsonify({'data':{'profile_incomplete':True},'error':None}))
    else:
        return(jsonify({'data':{'profile_incomplete':False},'error':None}))

@app.route('/complete_profile',methods=['POST'])
def add_records():
    data=request.get_json()
    print(data)
    print(type(data))
    ob=repo.OhlcRepo()
    ob.insert_record(collection_name="users",query={'username':data['username']},insert_doc={'$set':{'academics':data['academics'],'courses':data['courses'],'interests':data['interests']}})
    return(jsonify({'data':'success'}))


@app.route('/ArjunWebhook', methods=['POST'])
def ExtractDomain():
    data = request.get_json(silent=True)
    Domain = data['queryResult']['parameters']['DomainName']
    reply = {
        "fulfillmentText": "Answer From Webhook & Domain: "+Domain,
    }
    return jsonify(reply)

@app.route('/search')
def retres():
    query=request.args.get("keyword")
    un=request.args.get("username")
    ob=repo.OhlcRepo()
    res=ob.find_record_with_projection_limit(collection_name="users",query={"usrname":un})

@app.route('/refresh', methods=['POST'])
#@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200

@app.route('/course_description')
def ret_course():
    title=request.args.get("title")
    source=request.args.get("source")
    ob = repo.OhlcRepo()
    res=ob.find_record_with_limit(collection_name="courses",query={"course_title":title,"course_source":source},limit=1)
    res[0]['_id']=str(res[0]['_id'])
    return(jsonify({'data':res[0],'error':None}))

def create_json(data):
   """Utility method that creates a json response from the data returned by the service method.
   :param data:
   :return:
   """
   base_response_dto = {
       'data': data,
   }
   js = json.dumps(base_response_dto)
   resp = Response(js, status=200, mimetype='application/json')
   return resp

@app.route('/first_time_quiz', methods=['POST'])
def first_time_quiz():
   data=request.get_json()
   ob = repo.OhlcRepo()
   records = list(ob.find_record_with_limit('quiz', {'domain': data['domain']}, 9))
   results = {'beginner': [], 'intermediate': [], 'advanced': []}
   for record in records:
       record['_id'] = str(record['_id'])
       if record['level'] == 1:
           results['beginner'].append(record)
       if record['level'] == 2:
           results['intermediate'].append(record)
       if record['level'] == 3:
           results['advanced'].append(record)
   return create_json(results)

@app.route('/quiz_result', methods=['POST'])
def store_quiz_result():
   data=request.get_json()
   username = data['username']
   quiz_score = int(data['score'])
   quiz_domain = data['domain']
   if quiz_score < 6:
       level = 1
   elif quiz_score < 9:
       level = 2
   elif quiz_score == 9:
       level = 3
   ob = repo.OhlcRepo()
   ob.insert_record('user_scores', {'username': username}, {'$set': {'score': int(quiz_score), 'level': level, 'domain': quiz_domain}})
   return create_json('Run recommendation engine')

def quiz(domain):
   ob = repo.OhlcRepo()
   records = list(ob.find_record_with_limit('quiz', {'domain': domain}, 9))
   results = {'beginner': [], 'intermediate': [], 'advanced': []}
   for record in records:
       record['_id'] = str(record['_id'])
       if record['level'] == 1:
           results['beginner'].append(record)
       if record['level'] == 2:
           results['intermediate'].append(record)
       if record['level'] == 3:
           results['advanced'].append(record)
   results['type'] = 'quiz'
   return create_json(results)

@app.route('/courses', methods=['GET'])
def find_top_courses():
    #username = request.args.get('username')
    domain = request.args.get('domain')
    ob = repo.OhlcRepo()
    final_list = []
    for course_source in ['udemy', 'coursera', 'edx', 'youtube']:
        records = list(ob.find_record_with_limit('courses', {'search_term': domain, 'course_source': course_source}, 5))
        for x in records:
            x['_id'] = str(x['_id'])
            final_list.append(x)
    random.shuffle(final_list)
    return create_json(final_list)

@app.route('/feedback')
def send_feedback():
    pass

@app.route('/search_by_domain', methods=['GET'])
def search_by_domain():
   username = request.args.get('username')
   domain = request.args.get('domain')
   ob = repo.OhlcRepo()
   records = list(ob.find_record_with_limit('users', {'username': username}, 1))
   print(records)
   if 'searched_keywords' in records[0]:
       searched_keywords = records[0]['searched_keywords']
   else:
       searched_keywords = []
   if domain not in searched_keywords:
       searched_keywords.append(domain)
       ob.update_query('users', {'username': username}, {'searched_keywords': searched_keywords})
       return quiz(domain)
   else:
       return create_json('Run recommendation engine')

@scheduler.task('cron', hour=4)
def content_fetch():
    print('Crawls for new courses every day')
    '''
    # Udemy 
    udemy.Udemy_API.main()
    # Coursera
    coursera.coursera_main.main()
    # EdX
    edx.edx_scrapper.main()
    # Youtube
    youtube.youtubeapi.main()'''

@app.route('/get_profile/<username>', methods=['GET'])
def get_user_profile(username):
    ob = repo.OhlcRepo()
    record = list(ob.find_record_with_projection_limit(collection_name='users'
                                                       , query={'username': str(username)}
                                                       , projection={"_id":0}
                                                       , limit=1))
    if not record:
        return jsonify({"data":None, "error":"Username does not exist"})
    record = record[0]
    if record['username'] == username:
        return (jsonify({'data': {"user":record}, 'error': None}))
    else:
        return (jsonify({'data': None, 'error': 'Username does not exists'}))

@app.route('/update_profile/<username>', methods=['POST'])
def update_user_profile(username):
    ob = repo.OhlcRepo()
    res = ob.find_record_with_limit(collection_name="users", query={"username": str(username)}, limit=1)[0]
    if res['username'] == username:
        update_doc = request.get_json(force=True)
        if res['academics'] != update_doc['academics'] or res['courses'] != update_doc['courses']:
            update_doc['balance'] += (len(update_doc['academics'] ) - len(res['academics']))*10 
            update_doc['balance'] += (len(update_doc['courses'] ) - len(res['courses']))*10 
        ob.insert_record(collection_name="users", query={"username": username}
                         , insert_doc={"$set":
                                           {
                                               "academics":update_doc["academics"],
                                               "courses": update_doc["courses"],
                                               "interests": update_doc["interests"],
                                               "city": update_doc["city"],
                                               "state": update_doc["state"],
                                               "country": update_doc["country"],
                                               "name": update_doc["name"],
                                               "password": update_doc["password"],
                                               "phone": update_doc["phone"],
                                               "balance": update_doc["balance"]
                                           }})
        return (jsonify({'data': 'Your profile has been updated successfully!', 'error': None}))
    else:
        return (jsonify({'data': None, 'error': 'There was an error in updating your profile. Please try again.'}))

@app.route("/get_quiz_questions/<domain>", methods=["GET"])
def get_quiz_questions(domain):
	ob = repo.OhlcRepo()
	questions = ob.find_record_with_projection('quiz', {"domain": domain}, {"_id":0})
	if not questions:
		return create_json({"data": None, "error": "There was an error in fetching the questions. Please try again later."})
	else:    
		return create_json({"data": questions, "error": None})

@app.route("/evaluate_quiz/<username>/<domain>", methods=["POST"])
def evaluate_quiz(username, domain):
    ob = repo.OhlcRepo()
    res = ob.find_record_with_limit(collection_name="users", query={"username": str(username)}, limit=1)[0]
    if username == res['username']:
        attempted_quiz = request.get_json(force=True)
        score = 0
        for question in attempted_quiz:
            evaluation = ob.find_record_with_projection('quiz', {"domain": domain, "question": question}, {"_id": 0})[0]
            if evaluation and evaluation['correct_answer'] == attempted_quiz[question]:
                score = score+1
        expertise = ""
        if score <= 3:
            expertise = "Beginner"
        elif score > 3 and score <= 6:
            expertise = "Intermediate"
        elif score > 6:
            expertise = "Advanced"

        update_doc = {"expertise": {"domain":domain, "details":{"score": score, "expertise": expertise}}}
        ob.insert_record(collection_name="users", query={"username": username}, insert_doc={"$set": update_doc})

        return create_json({"data": {"expertise": expertise, "score":score}, "error": None})
    else:
        return create_json({"data":None, "error": "Specified username is invalid; it does not exist."})
    
if __name__ == '__main__':
    app.run(debug=True)
