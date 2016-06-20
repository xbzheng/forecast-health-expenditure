from flask import render_template
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import numpy as np
import psycopg2
from flask import request


# from a_Model import ModelIt

user = 'xb' #add your username here (same as previous postgreSQL)            
host = 'localhost'
dbname = 'meps_mvp_db'
pswd = '123456'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user, host =host,  password=pswd)
#con = mysql.connect(database = dbname, user = user)
# plot_data

@app.route('/')
@app.route('/index')
def index():
  return render_template("insight_project.html")

@app.route('/home')
def home_page():
  return render_template("insight_project.html")

@app.route('/insight_project')
def insight_input():
    return render_template("insight_project.html")

@app.route('/good_health_cond')
def insight_input_good_cond():
    return render_template("good_health_cond.html")
  

@app.route('/bad_health_cond')
def insight_input_bad_cond():
    return render_template("bad_health_cond.html")

@app.route('/project_slides')
def project_slides():
    return render_template("slides.html")

@app.route('/bio')
def bio_info():
    return render_template("insight_project.html")


@app.route('/forcast')
def glm_output():
  blood_pres_input = int(request.args.get('blood_pres_input'))
  adl_care_input = int(request.args.get('adl_care_input'))
  specialist_input = int(request.args.get('specialist_input'))
  asthma_input = int(request.args.get('asthma_input'))
  diabetes_input = int(request.args.get('diabetes_input'))
  wage_input = int(request.args.get('wage_input'))
  discharge_input = int(request.args.get('discharge_input'))
  routine_input = int(request.args.get('routine_input'))
  act_input = int(request.args.get('act_input'))
  gender_var = request.args.get('gender_input')
  age_var = request.args.get('age_input')

  query = "SELECT avg(exp) FROM mvp_data_table WHERE age31x={0} AND sex = {1}".format(age_var,gender_var)
  print (query)
  query_results=pd.read_sql_query(query,con)
  print (query_results)

  age_input = int(age_var)
  gender_input = int(gender_var)
  #break down the race answer so can be fitted into model
  ethnicity_input = int(request.args.get('ethnicity_input'))
  ##default setting for white and hispan ethnicity
  white = 0;
  hispan = 0;
  if ethnicity_input == 1:
    white = 1
  if ethnicity_input == 4:
    hispan = 1

  ##feed the inputs into model to compute the estimate expenditure Y in log form
  belta_array = [1.65793597,  2.50448903,  0.56178972,  0.61748682,  0.27844649, 0.48529412,  0.24846022,  0.32687906,  0.02479726,  0.24441821, 0.86527754,  0.34268292,  0.1317265 ,  0.41348887,  0.61133755, -0.53609768, -0.14073792,  0.61437919, -0.44943438,  0.06559937, -0.15027342,  1.58084542,  0.38047624, -0.57064548, -0.79483468, 0.90008942, -0.39190336,  0.20767255,  0.76338522, -0.1027692 , 0.14933694,  0.3702343 ,  0.46789753,  0.06789939, -0.41127266, 0.171023  , -0.30246779,  0.02798932]
  log_y = belta_array[0] + belta_array[2] * blood_pres_input  + belta_array[5]*adl_care_input + belta_array[6]*specialist_input + belta_array[7] *asthma_input  + belta_array[13]* diabetes_input  + belta_array[17]*hispan + belta_array[18]* wage_input + belta_array[21]* discharge_input + belta_array[26]*routine_input + belta_array[29]*act_input+ belta_array[34]*white + belta_array[35]*gender_input+ belta_array[37]*age_input + 2

  ##transformated Y from log representation to dollar representation
  mse = 5.46
  est_y = int(np.exp(log_y + 0.5 * mse))
  var = int(query_results.iloc[0]['avg'])
  output = []
  output.append(dict(predict= est_y, aver = var))
  the_results =''
  return render_template("insight_project_out.html",  outputs = output, the_result = the_results)

# @app.route('/myplot')
# def getplot():
#   fig = plt.figure()
#   plt.plot(range(3))
#   canvas = FigureCanvas(fig)
#   img = BytesIO()
#   fig.savefig(img)
#   img.seek(0)
#   return send_file(img, mimetype='image/png')




