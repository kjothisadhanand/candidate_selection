#import numpy as np
import datetime
from flask import Flask, request, jsonify, render_template
#import pickle

app = Flask(__name__)
#model = pickle.load(open('model.pkl', 'rb'))

#Converting self rating (sr) to integer values
def convert_sr_to_int(rating):
    self_rating_dict = {1:3, 2:7, 3:10, 0: 0}
    return self_rating_dict[rating]

#Converting Other Skill to integer values
def other_skill_to_int(affirm):
    other_skill_dict = {0:0, 1:3}
    return other_skill_dict[affirm]

  
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    features = [str(x) for x in request.form.values()]
    #flag_ug=True
    #flag_pg=True
    #if(features[])
    
    #logic to 
    #calculate years since ug and years since pg
    
    
    now = datetime.datetime.now()
    running_year=int(now.year)
    
    
    
    
    wt_ug=0
    years_since_ug=0
    wt_pg=0
    years_since_pg=0
    ug=features[2]
    pg=features[4]
    
    #logic to give weightage to ug and pg
    if(("B.Tech" in ug) or ("B.E" in ug)):
        #logic to 
        #calculate years since ug
        year_ug=int(features[3])
        years_since_ug=running_year-year_ug
        if(years_since_ug==0):#fresher
            wt_ug=10
        elif(years_since_ug==1):#1yr old
            wt_ug=8
        elif(years_since_ug>1):#more than 1 year
            wt_ug=5
    
    if(("M.Tech" in pg) or ("M.Sc" in pg)):
        #logic to 
        #calculate years since pg
        year_pg=int(features[5])
        years_since_pg=running_year-year_pg
        
        if(years_since_pg==0):#fresher
            wt_pg=7
        else:#1yr old and more
            wt_pg=3
    
    #weightage to self rating for Python,R and Data Science
    wt_self_rating=[0,0,0]
    for i in range(0,3):
        wt_self_rating[i]=convert_sr_to_int(int(features[i+6]))

    #weightage to other skills
    wt_other_skills=[0,0,0,0,0,0,0]
    for i in range(0,7):
        wt_other_skills[i]=other_skill_to_int(int(features[i+9]))
    
    #finally calculate total score
    tot_score=wt_ug+wt_pg+sum(wt_self_rating)+sum(wt_other_skills)
    str_result=''
    if(tot_score>=40):
        str_result="Congratulation ! \n Your profile has been shortlisted for Data Scientist"
    else:
        str_result="Sorry ! \n Your profile did not qualify for further discussion"

    
    #final_features = [np.array(int_features)]
    #prediction = model.predict(final_features)

    #output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='{}'.format(str_result))


if __name__ == "__main__":
    app.run(debug=True)