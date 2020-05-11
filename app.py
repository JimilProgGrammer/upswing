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
from bson import json_util
import numpy as np
import json
import repo
import random
import operator
# [---------------------------------------END IMPORTING LIBRARIES-------------------------------------]
class Config(object):
  SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.debug = True
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

"""
:author: Sujoy
"""
# [------------------------------------START SEND EMAIL-----------------------------------------------]
def send_email(user, pwd, recipient, subject, body):
  """
  Utility function that send OTP in email from 'user' Email ID
  to 'recipient' Email ID.
  """
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
  """
  Utility method that generates random OTP, forms email body
  and uses send_email() to send email over TLS.
  """
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
@app.route("/auth", methods=["Post"])
def authenticate():
  """
  Login API to verify if userID and password were correct.
  """
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
  """
  Executed before sending output of each API; helps
  in preventing CORS error.
  """
  response.headers.add('Access-Control-Allow-Origin', '*')
  if request.method == 'OPTIONS':
    response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
    headers = request.headers.get('Access-Control-Request-Headers')
    if headers:
      response.headers['Access-Control-Allow-Headers'] = headers
  return response


@app.route('/signup', methods=['Post'])
def sign_up():
  """
  Signs up user by checking whether username is already existing or not
  and then sending OTP to user, if signup is successful.
  """
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
  """
  API to verify whether user entered the OTP
  correctly or not.
  """
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


def create_json(data):
  """
  Utility method that creates a json response from the data returned by the service method.
   :param data:
   :return:
  """
  base_response_dto = {
    'data': data,
  }
  js = json.dumps(base_response_dto)
  resp = Response(js, status=200, mimetype='application/json')
  return resp


@app.route("/buy_stocks", methods=["POST"])
def buy_stocks():
  """
  Utility method that is called when user wants to buy certain
  quantity of a stock.
  1. Sees stock_portfolio collection to identify the quantity of
     that stock that the user has.
  2. Updates portfolio collection with a new BUY trade.
  3. Updates balance in user collection.
  """
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
  """
  API that is called when user wants to sell a certain quantity
  of a particular stock.
  1. Sees stock_portfolio collection to identify the quantity of
     that stock that the user has.
  2. Updates portfolio collection with a new SELL trade.
  3. Updates balance in user collection.
  """
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
  """
  First API that is to be executed after setup in production.
  Loads all data from 2016 for all the stocks offered in the game.
  """
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
  """
  Fail-safe for scheduler; triggered when scheduler fails to load
  new OHLC data at the end of day.
  """
  try:
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
      print(record['timestamp'])
      print("DONE INSERTING: " + symbol)
    return create_json({"data": "Success"})
  except Exception as e:
    print(e)
    return create_json({"Error": e})

"""
:author: Manan
"""
@app.route("/get_portfolio/<username>", methods=["GET"])
def get_user_portfolio(username):
  """
  API that is used to return data for the user's welcome screen;
  returns user's current holdings, his portfolio's net gain and his
  current balance.
  """
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
  """
  API that returns all stocks and their description, along with
  their latest closing prices, for the stock picker screen.
  Used to give buy and sell options to the user.
  """
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


@app.route("/get_current_standings", methods=["GET"])
def get_current_standings():
  """
  Returns data for the leaderboard screen; calculates portfolio net gain for
  all users and sorts in descending order, thus generating the leaderboard.
  """
  try:
    ob = repo.OhlcRepo()
    users = ob.find_record_with_projection(collection_name="users", query={}, projection={"_id": 0})
    json_response = []
    for user in users:
      print(user)
      portfolio = ob.find_records_with_query(collection_name="portfolio", query={"email_id": user['email_id'], "is_live": True})
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
          portfolio_net_gain = portfolio_net_gain + (latest_close - original)

      json_response.append({"username": user['email_id'], "name": user['name'], "portfolio_gain": portfolio_net_gain})
    json_response = sorted(json_response, key = lambda i: (i['portfolio_gain'], i['name']), reverse=True) 
    return create_json({"data": json_response, "error": None})
  except Exception as e:
    print(e)
    return create_json({"Error": e})


@app.route("/get_chart_data/<symbol>", methods=["GET"])
def get_stock_data_for_chart(symbol):
  """
  Returns the latest 1-year (252 days) datapoints i.e. timestamps
  and closing price for plotting the graph.
  """
  try:
    ob = repo.OhlcRepo()
    stock_docs = ob.find_record_with_projection_limit(collection_name=symbol, query={}, projection={"_id": 0, "close": 1, "timestamp": 1}, limit=252)
    stock_docs.reverse()
    closing = [stock['close'] for stock in stock_docs]
    dates = [stock['timestamp'].strftime('%d/%m/%Y') for stock in stock_docs]
    return create_json({'data': {'close': closing, 'date': dates}, "error": None})
  except Exception as e:
    print(e)
    return create_json({"data": None, "error": e})


@scheduler.task('cron', hour=8)
def daily_data_load():
  """
  Scheduler running every 8 hours to update new
  EOD OHLC data.
  """
  try:
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
    return create_json({"data": "Success"})
  except Exception as e:
    print(e)
    return create_json({"Error": e})


if __name__ == '__main__':
  app.run(debug=True)
