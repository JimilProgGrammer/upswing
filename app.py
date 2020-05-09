# [------------------------------------START IMPORTING FILES------------------------------------------]
from __future__ import division
from data_sources import yahoo_finance
# [---------------------------------------END IMPORTING FILES-----------------------------------------]

# [------------------------------------START IMPORTING LIBRARIES--------------------------------------]
import logging as logger
import random as r
import smtplib
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
import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl
import json
import repo
import random
import operator

# [---------------------------------------END IMPORTING LIBRARIES-------------------------------------]
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = u"C:/Users/yashs/Documents/arjun/flask/ArjunBot.json"


class Config(object):
  SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.debug = True
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


# jwt = JWTManager(app)

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
    print("Mail send initated.")
    server.ehlo()
    server.starttls()
    server.login(user, pwd)
    server.sendmail(FROM, TO, message)
    server.close()
    print("Mail send complete")
    logger.debug('successfully sent the mail')
    return "1"
  except Exception as e:
    print(e)
    return "0"


def SendOTPOverEmail(email):
  try:
    otp = str(r.randint(10000, 99999))
    # manandoshi1607@gmail.com
    subject = "Email Verification | Upswing"
    body = """
          Hi,

          Thanks for creating a new account on Upswing, and welcome :)

          The final step to create your account is to verify your email address.
          Your OTP is : """ + otp + """</b>
          Once that's done, you're all set.

          Regards,
          fsociety
          """
    emailRes = send_email("ayreonvendor1@gmail.com", "ayreonvendor123", email, subject, body)
    if (emailRes == 1):
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
  data = dbObj.find_record_with_limit("users", {"email_id": username}, 1)
  if not data:
    return (jsonify({'data': None, 'error': "Username Doesn't Exist"}))
  else:
    if username == data[0]["email_id"] and password == data[0]["password"]:
      ret = {
        'data': "Auth Successful.",
        'name': data[0]['name']
      }
      return create_json({"data": ret, "error": None})
    else:
      return (jsonify({'data': None, 'error': "Username Doesn't Match"}))


# [-----------------------------------------END LOGIN PAGE-----------------------------------------]

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


@app.route('/signup', methods=['Post'])
def sign_up():
  form = {}
  form['name'] = request.args.get("name")
  form['email_id'] = request.args.get("email_id")
  form['password'] = request.args.get("password")

  print(form)
  # return(jsonify(form))
  un = form['email_id']
  ob = repo.OhlcRepo()
  user = ob.find_record_with_limit(collection_name="users", query={"email_id": str(un)}, limit=1)
  if not user:
    """ Successful signup """
    """ OTP Verification for email """
    """ """
    o = SendOTPOverEmail(form['email_id'])
    form['otp'] = o
    form['is_otp_verified'] = False
    form['live_challenges'] = []
    form['completed_challenges'] = []
    form['balance'] = 500000.0
    form['equity_value'] = 0
    ob.insert_new_record(collection_name="users", insert_doc=form)
    return (jsonify({'data': 'Success', 'error': None}))
  else:
    """ Exception msg: User already exists """
    return (jsonify({'data': None, 'error': 'username already exists'}))


@app.route('/verify/<username>/<otp>', methods=['Post'])
def check(username, otp):
  # det=request.args
  ob = repo.OhlcRepo()
  res = ob.find_record_with_limit(collection_name="users", query={"email_id": str(username)}, limit=1)[0]
  print(res, "##")
  if res['otp'] == otp:
    ob.insert_record(collection_name="users", query={"email_id": username},
                     insert_doc={"$set": {"is_otp_verified": True}})
    return (jsonify({'data': 'email verified successfuly', 'error': None}))
  else:
    return (jsonify({'data': None, 'error': 'Otp incorrect'}))


@app.route('/welcome')
# @jwt_required
def getdetails():
  un = request.args.get("username")
  ob = repo.OhlcRepo()
  res = ob.find_record_with_limit(collection_name="users", query={"username": str(un)}, limit=1)[0]

  print(res)
  if 'academics' not in res.keys():
    return (jsonify({'data': {'profile_incomplete': True}, 'error': None}))
  else:
    return (jsonify({'data': {'profile_incomplete': False}, 'error': None}))


@app.route('/complete_profile', methods=['POST'])
def add_records():
  data = request.get_json()
  print(data)
  print(type(data))
  ob = repo.OhlcRepo()
  ob.insert_record(collection_name="users", query={'username': data['username']}, insert_doc={
    '$set': {'academics': data['academics'], 'courses': data['courses'], 'interests': data['interests']}})
  return (jsonify({'data': 'success'}))


@app.route('/search')
def retres():
  query = request.args.get("keyword")
  un = request.args.get("username")
  ob = repo.OhlcRepo()
  res = ob.find_record_with_projection_limit(collection_name="users", query={"usrname": un})


@app.route('/course_description')
def ret_course():
  title = request.args.get("title")
  source = request.args.get("source")
  ob = repo.OhlcRepo()
  res = ob.find_record_with_limit(collection_name="courses", query={"course_title": title, "course_source": source},
                                  limit=1)
  res[0]['_id'] = str(res[0]['_id'])
  return (jsonify({'data': res[0], 'error': None}))


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
  data = request.get_json()
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
  data = request.get_json()
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
  ob.insert_record('user_scores', {'username': username},
                   {'$set': {'score': int(quiz_score), 'level': level, 'domain': quiz_domain}})
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
  # username = request.args.get('username')
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
                                                     , projection={"_id": 0}
                                                     , limit=1))
  if not record:
    return jsonify({"data": None, "error": "Username does not exist"})
  record = record[0]
  if record['username'] == username:
    return (jsonify({'data': {"user": record}, 'error': None}))
  else:
    return (jsonify({'data': None, 'error': 'Username does not exists'}))


@app.route('/update_profile/<username>', methods=['POST'])
def update_user_profile(username):
  ob = repo.OhlcRepo()
  res = ob.find_record_with_limit(collection_name="users", query={"username": str(username)}, limit=1)[0]
  if res['username'] == username:
    update_doc = request.get_json(force=True)
    if res['academics'] != update_doc['academics'] or res['courses'] != update_doc['courses']:
      update_doc['balance'] += (len(update_doc['academics']) - len(res['academics'])) * 10
      update_doc['balance'] += (len(update_doc['courses']) - len(res['courses'])) * 10
    ob.insert_record(collection_name="users", query={"username": username}
                     , insert_doc={"$set":
        {
          "academics": update_doc["academics"],
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
  questions = ob.find_record_with_projection('quiz', {"domain": domain}, {"_id": 0})
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
        score = score + 1
    expertise = ""
    if score <= 3:
      expertise = "Beginner"
    elif score > 3 and score <= 6:
      expertise = "Intermediate"
    elif score > 6:
      expertise = "Advanced"

    update_doc = {"expertise": {"domain": domain, "details": {"score": score, "expertise": expertise}}}
    ob.insert_record(collection_name="users", query={"username": username}, insert_doc={"$set": update_doc})

    return create_json({"data": {"expertise": expertise, "score": score}, "error": None})
  else:
    return create_json({"data": None, "error": "Specified username is invalid; it does not exist."})


@app.route("/get_portfolio/<username>", methods=["GET"])
def get_user_portfolio(username):
  ob = repo.OhlcRepo()
  res = ob.find_record_with_limit(collection_name="users", query={"email_id": str(username)}, limit=1)[0]
  json_response = {'current_holdings': [], 'balance': 0, 'portfolio_net_gain': 0}
  if username == res['email_id']:
    portfolio = ob.find_records_with_query(collection_name="portfolio", query={"email_id": username, "is_live": True})
    stocks_visited = []
    portfolio_net_gain = 0
    for trade in portfolio:
      symbol = trade['stock_name']
      if symbol not in stocks_visited:
        stocks_visited.append(symbol)
        symbol_trades = [d for d in portfolio if d['stock_name'] == symbol]
        symbol_trades.sort(key=operator.itemgetter('timestamp'))
        original = 0
        quantity = 0
        print(symbol, symbol_trades)
        if len(symbol_trades) == 1:
          original = float(symbol_trades[0]['price'])
          quantity = float(symbol_trades[0]['quantity'])
        else:
          original = float(symbol_trades[-1]['price'])
          quantity = float(symbol_trades[-1]['quantity'])
        latest_close = ob.find_records_with_limit(collection_name=symbol, limit=1)[0]['close']
        data = {'symbol': symbol, 'price': latest_close, 'quantity': quantity, 'net_gain': round((latest_close - original),5),
                'percent_gain': round((((latest_close - original) / original) * 100),5)}
        portfolio_net_gain = portfolio_net_gain + (latest_close - original)
        json_response['current_holdings'].append(data)

    portfolio = ob.find_records_with_query(collection_name="portfolio",
                                           query={"email_id": username, "is_live": False})
    stocks_visited = []
    for trade in portfolio:
      symbol = trade['stock_name']
      if symbol not in stocks_visited:
        stocks_visited.append(symbol)
        symbol_trades = [d for d in portfolio if d['stock_name'] == symbol]
        symbol_trades.sort(key=operator.itemgetter('timestamp'))
        original = symbol_trades[-2]['price']
        sold_at = symbol_trades[-1]['price']
        quantity = symbol_trades[-1]['quantity']
        data = {'symbol': symbol, 'price': sold_at, 'quantity': quantity, 'net_gain': round((sold_at - original),5),
                'percent_gain': round((((sold_at - original) / original) * 100),5)}
        json_response['current_holdings'].append(data)
    json_response['balance'] = round(res['balance'],2)
    json_response['portfolio_net_gain'] = round(portfolio_net_gain,5)
    return create_json({"data": json_response, "error": None})
  else:
    return create_json({"data": None, "error": "The specified username does not exist."})


@app.route("/stock_picker/<username>", methods=["GET"])
def stock_picker(username):
  ob = repo.OhlcRepo()
  user = ob.find_record_with_limit(collection_name="users", query={"email_id": str(username)}, limit=1)
  if user:
    balance = user[0]['balance']
    data = ob.find_record_with_projection(collection_name="stocks", query={}, projection={"_id": 0})
    stocks_data = []
    for stock in data:
      symbol = stock['stock_name']
      print(symbol)
      close = round(ob.find_records_with_sort(collection_name=symbol, query={})[0]['close'], 2)
      print(symbol, close)
      stocks_data.append({"stock_name": symbol, "description": stock['description'], "close": close})
    json_response = {"balance": round(balance,2), "data": stocks_data}
    return create_json({"data": json_response, "error": None})
  else:
    return create_json({"data": None, "error": "Username passed is invalid."})


@app.route("/buy_stocks", methods=["POST"])
def buy_stocks():
  form = {}
  form['username'] = request.args.get("username")
  form['stock_name'] = request.args.get("stock_name")
  form['quantity'] = request.args.get("quantity")
  form['price'] = request.args.get("price")
  print(form)
  ob = repo.OhlcRepo()
  user = ob.find_record_with_limit(collection_name="users", query={"email_id": str(form['username'])}, limit=1)[0]
  if user:
    if user['balance'] > float(form['quantity']) * float(form['price']):
      stock_portfolio = ob.find_record_with_projection_limit(collection_name="portfolio"
                                                             , query={"email_id": form['username'],"stock_name": form['stock_name']}
                                                             , projection={"_id": 0, "quantity": 1}, limit=1)

      quantity = int(form['quantity'])
      if len(stock_portfolio) > 0:
        quantity = quantity + stock_portfolio[0]['quantity']

      timestamp = datetime.datetime.now().strftime("%d/%m/%Y")
      ob.insert_new_record(collection_name="portfolio", insert_doc={
        "email_id": form['username'],
        "stock_name": form['stock_name'],
        "quantity": quantity,
        "price": float(form['price']),
        "is_live": True,
        "timestamp": timestamp,
        "trade_type": "BUY"
      })
      ob.insert_record(collection_name="users", query={"email_id": str(form['username'])}, insert_doc={
        "$set": {
          "balance": user['balance'] - (float(form['quantity']) * float(form['price']))
        }
      })
      return create_json({"data": "BUY transaction executed successfully.", "error": None})
    else:
      return create_json({"data": None, "error": "Insufficient Balance. Cannot buy any more stocks."})
  else:
    return create_json({"data": None, "error": "Username passed is invalid."})

@app.route("/sell_stocks", methods=["POST"])
def sell_stocks():
  form = {}
  form['username'] = request.args.get("username")
  form['stock_name'] = request.args.get("stock_name")
  form['quantity'] = request.args.get("quantity")
  form['price'] = request.args.get("price")
  print(form)
  ob = repo.OhlcRepo()
  user = ob.find_record_with_limit(collection_name="users", query={"email_id": str(form['username'])}, limit=1)[0]
  if user:
    stock_portfolio = ob.find_record_with_projection_limit(collection_name="portfolio"
                                                     , query={"email_id": form['username'], "stock_name": form['stock_name']}
                                                     , projection={"_id":0, "quantity": 1}, limit=1)

    if len(stock_portfolio) == 0:
      return create_json({"data":None, "error": "You cannot SELL a stock that you don't own."})

    stock_portfolio = stock_portfolio[0]
    if form['quantity'] <= stock_portfolio['quantity']:
      is_live = True
      if int(form['quantity']) == stock_portfolio['quantity']:
        is_live = False
      timestamp = datetime.datetime.now().strftime("%d/%m/%Y")
      ob.insert_new_record(collection_name="portfolio", insert_doc={
        "email_id": form['username'],
        "stock_name": form['stock_name'],
        "quantity": int(stock_portfolio['quantity']) - int(form['quantity']),
        "price": float(form['price']),
        "is_live": is_live,
        "timestamp": timestamp,
        "trade_type": "SELL"
      })
      ob.insert_record(collection_name="users", query={"email_id": str(form['username'])}, insert_doc={
        "$set": {
          "balance": user['balance'] + (float(form['quantity']) * float(form['price']))
        }
      })
      return create_json({"data": "SELL transaction executed successfully.", "error": None})
    else:
      return create_json({"data":None, "error": "You cannot SELL more equities than you own."})
  else:
    return create_json({"data": None, "error": "Username passed is invalid."})

@app.route("/initial_data_load", methods=["GET"])
def daily_data_load():
  try:
    ob = repo.OhlcRepo()
    stocks = ob.find_record_with_projection(collection_name="stocks", query={}, projection={"_id": 0, "stock_name": 1})

    start_date = datetime.date.today() - datetime.timedelta(days=1260)
    start_date = start_date.strftime("%Y-%m-%d")

    for doc in stocks:
      symbol = doc['stock_name']
      print("INSERTING: " + symbol)
      data = yahoo_finance(symbol, start_date)
      data = data.to_dict("records")
      ob.insert_many_records(collection_name=symbol, insert_doc=data)
      print("DONE INSERTING: " + symbol)
    return create_json({"data": "Success"})
  except Exception as e:
    print(e)
    return create_json({"Error": e})


@app.route("/daily_data_load")
def daily_data_load_endpoint():
  ob = repo.OhlcRepo()
  stocks = ob.find_record_with_projection(collection_name="stocks", query={}, projection={"_id": 0, "stock_name": 1})

  start_date = datetime.date.today() - datetime.timedelta(days=252)
  start_date = start_date.strftime("%Y-%m-%d")

  for doc in stocks:
    symbol = doc['stock_name']
    print("INSERTING: " + symbol)
    data = yahoo_finance(symbol, start_date)
    data = data.to_dict("records")
    for record in data:
      query_doc = {"timestamp": record["timestamp"]}
      insert_doc = record
      ob.update_query(collection_name=symbol, query_doc=query_doc, insert_doc=insert_doc)
    print(record['timestamp'])
    print("DONE INSERTING: " + symbol)


@scheduler.task('cron', hour=8)
def daily_data_load():
  ob = repo.OhlcRepo()
  stocks = ob.find_record_with_projection(collection_name="stocks", query={}, projection={"_id": 0, "stock_name": 1})

  start_date = datetime.date.today() - datetime.timedelta(days=7)
  start_date = start_date.strftime("%Y-%m-%d")

  for doc in stocks:
    symbol = doc['stock_name']
    print("INSERTING: " + symbol)
    data = yahoo_finance(symbol, start_date)
    data = data.to_dict("records")
    for record in data:
      query_doc = {"timestamp": record["timestamp"]}
      insert_doc = record
      ob.update_query(collection_name=symbol, query_doc=query_doc, insert_doc=insert_doc)
    print("DONE INSERTING: " + symbol)


if __name__ == '__main__':
  app.run(debug=True)
