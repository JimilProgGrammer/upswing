from pymongo import *

mng_client = MongoClient('localhost', 27017)
db = mng_client.arjun

# <------------------------------------- Artificial Intelligence Quiz ----------------------------------->

question = {"question_number": 1, 
            "level": 1,
            "question": "Which of the following is true related to ‘Satisfiable’ property?", 
            "question_type": 'mcq', 
            "options": ["A statement is satisfiable if there is some interpretation for which it is false",
                        "A statement is satisfiable if there is some interpretation for which it is true",
                        "A statement is satisfiable if there is no interpretation for which it is true",
                        "A statement is satisfiable if there is no interpretation for which it is false"
            ]
            ,"correct_answer": "A statement is satisfiable if there is some interpretation for which it is true",
            "domain": 'artificial intelligence'
}

db['quiz'].insert_one(question)

question = {"question_number": 2, 
            "level": 1,
            "question": "Third component of a planning system is to", 
            "question_type": 'mcq', 
            "options": ["Detect when a solution has been found",
                        "Detect when solution will be found",
                        "Detect whether solution exists or not",
                        "Detect whether multiple solutions exist"
            ]
            ,"correct_answer": "Detect when a solution has been found",
            "domain": 'artificial intelligence'
}

db['quiz'].insert_one(question)

question = {"question_number": 3, 
            "level": 1,
            "question": "Which of the following is true in Statistical reasoning?", 
            "question_type": 'mcq', 
            "options": ["The representation is extended to allow some kind of numeric measure of certainty to be associated with each statement",
                        "The representation is extended to allow ‘TRUE or FALSE’ to be associated with each statement",
                        "The representation is extended to allow some kind of numeric measure of certainty to be associated common to all statements",
                        "The representation is extended to allow ‘TRUE or FALSE’ to be associated common to all statements"
            ]
            ,"correct_answer": "The representation is extended to allow some kind of numeric measure of certainty to be associated with each statement",
            "domain": 'artificial intelligence'
}

db['quiz'].insert_one(question)

question = {"question_number": 4, 
            "level": 2,
            "question": "What is rational at any given time depends on", 
            "question_type": 'mcq', 
            "options": ["The performance measure that defines the criterion of success",
                        "The agent’s prior knowledge of the environment",
                        "The actions that the agent can perform",
                        "All of the above mentioned"
            ]
            ,"correct_answer": "All of the above mentioned",
            "domain": 'artificial intelligence'
}

db['quiz'].insert_one(question)

question = {"question_number": 5, 
            "level": 2,
            "question": "The Task Environment of an agent consists of", 
            "question_type": 'mcq', 
            "options": ["Sensors",
                        "Actuators",
                        "Performance Measures",
                        "All of the mentioned"
            ]
            ,"correct_answer": "All of the mentioned",
            "domain": 'artificial intelligence'
}

db['quiz'].insert_one(question)

question = {"question_number": 6, 
            "level": 2,
            "question": "What among the following constitutes to the incremental formulation of CSP?", 
            "question_type": 'mcq', 
            "options": ["Path cost",
                        "Goal cost",
                        "Successor function",
                        "All of the mentioned"
            ]
            ,"correct_answer": "All of the mentioned",
            "domain": 'artificial intelligence'
}

db['quiz'].insert_one(question)

question = {"question_number": 7, 
            "level": 3,
            "question": "____________ is/are useful when the original formulation of a problem is altered in some way, typically because the set of constraints to consider evolves because of the environment.", 
            "question_type": 'mcq', 
            "options": ["Static CSPs",
                        "Dynamic CSPs",
                        "Flexible CSPs",
                        "None of the above"
            ]
            ,"correct_answer": "Dynamic CSPs",
            "domain": 'artificial intelligence'
}

db['quiz'].insert_one(question)

question = {"question_number": 8, 
            "level": 3,
            "question": "The main components of the expert systems is/are,", 
            "question_type": 'mcq', 
            "options": ["Inference Engine",
                        "Knowledge Base",
                        "Inference Engine & Knowledge Base",
                        "None of the above"
            ]
            ,"correct_answer": "Inference Engine & Knowledge Base",
            "domain": 'artificial intelligence'
}

db['quiz'].insert_one(question)

question = {"question_number": 9, 
            "level": 3,
            "question": "The CAI (Computer-Assisted Instruction) technique based on programmed instruction is:", 
            "question_type": 'mcq', 
            "options": ["frame-based CAI",
                        "generative CAI",
                        "problem-solving CAI",
                        "intelligent CAI"
            ]
            ,"correct_answer": "frame-based CAI",
            "domain": 'artificial intelligence'
}

db['quiz'].insert_one(question)


# <------------------------------------- Big Data Quiz ----------------------------------->

question = {"question_number": 1,
           "level": 1,
           "question": "__________ can best be described as a programming model used to develop Hadoop-based applications that can process massive amounts of data.",
           "question_type": 'mcq',
           "options": ["MapReduce",
                       "Mahout",
                       "Oozie",
                       "All of the mentioned"
           ]
           ,"correct_answer": "MapReduce",
           "domain": 'big data analytics'
}

db['quiz'].insert_one(question)

question = {"question_number": 2,
           "level": 1,
           "question": "Which of these is the main component of Big Data?",
           "question_type": 'mcq',
           "options": ["YARN",
                       "MapReduce",
                       "HDFS",
                       "All of the above"
           ]
           ,"correct_answer": "YARN",
           "domain": 'big data analytics'
}

db['quiz'].insert_one(question)

question = {"question_number": 3,
           "level": 1,
           "question": "Which of these is best suited for assigning resources to a highly parallel application?",
           "question_type": 'mcq',
           "options": ["HDFS",
                       "Hadoop",
                       "Spark",
                       "YARN"
           ]
           ,"correct_answer": "MapR",
           "domain": 'big data analytics'
}

db['quiz'].insert_one(question)

question = {"question_number": 4,
           "level": 2,
           "question": "Hadoop can run in the following modes except",
           "question_type": 'mcq',
           "options": ["Pseuo-Distributed Mode",
                       "Standalone Mode",
                       "Multiple Cluster Node",
                       "Separate mode"
           ]
           ,"correct_answer": "Separate mode",
           "domain": 'big data analytics'
}

db['quiz'].insert_one(question)

question = {"question_number": 5,
           "level": 2,
           "question": "According to analysts, for what can traditional IT systems provide a foundation when they're integrated with big data technologies like Hadoop ?",
           "question_type": 'mcq',
           "options": ["Data Warehousing and business intelligence",
                       "Collecting and Storing unstructured data",
                       "Management of hadoop clusters",
                       "Big Data management and data mining"
           ]
           ,"correct_answer": "Big Data management and data mining",
           "domain": 'big data analytics'
}

db['quiz'].insert_one(question)

question = {"question_number": 6,
           "level": 2,
           "question": "What is a unit of data that flows through a Flume agent?",
           "question_type": 'mcq',
           "options": ["Log",
                       "Event",
                       "Row",
                       "None of the above"
           ]
           ,"correct_answer": "Event",
           "domain": 'big data analytics'
}

db['quiz'].insert_one(question)

question = {"question_number": 7,
           "level": 3,
           "question": "What makes Big Data analysis difficult to optimize?",
           "question_type": 'mcq',
           "options": ["Not difficult to optimize",
                       "Both data and cost effective ways to mine data to make business sense out of it",
                       "The technology to mine Data",
                       "all of the above"
           ]
           ,"correct_answer": "Both data and cost effective ways to mine data to make business sense out of it",
           "domain": 'big data analytics'
}

db['quiz'].insert_one(question)

question = {"question_number": 8,
           "level": 3,
           "question": "Which of the following hides the limitations of Java behind a powerful and concise Clojure API for Cascading.",
           "question_type": 'mcq',
           "options": ["Hcatalog",
                       "Hcalding",
                       "Scaldng",
                       "Cascalog"
           ]
           ,"correct_answer": "Cascalog",
           "domain": 'big data analytics'
}

db['quiz'].insert_one(question)

question = {"question_number": 9,
           "level": 3,
           "question": "Listed below are the three steps that are followed to deploy a Big Data Solution except",
           "question_type": 'mcq',
           "options": ["Data Ingestion",
                       "Data Processing",
                       "Data dissemination",
                       "Data Storage"
           ]
           ,"correct_answer": "Data dissemination",
           "domain": 'big data analytics'
}

db['quiz'].insert_one(question)