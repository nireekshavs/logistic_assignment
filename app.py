
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            women_occupation=float(request.form['women_occupation'])
            men_occupation = float(request.form['men_occupation'])
            rate_marriage = float(request.form['rate_marriage'])
            age = float(request.form['age'])
            yrs_married = float(request.form['yrs_married'])
            children = float(request.form['children'])
            religious = float(request.form['religious'])
            education = float(request.form['education'])
            if women_occupation == 2:
                data = {'occ_2':1.0,'occ_3':0.0,'occ_4':0.0,'occ_5':0.0,'occ_6':0.0}
            elif women_occupation == 3:
                data = {'occ_2': 0.0, 'occ_3': 1.0, 'occ_4': 0.0, 'occ_5': 0.0, 'occ_6': 0.0}
            elif women_occupation == 4:
                data = {'occ_2': 0.0, 'occ_3': 0.0, 'occ_4': 1.0, 'occ_5': 0.0, 'occ_6': 0.0}
            elif women_occupation == 5:
                data = {'occ_2': 0.0, 'occ_3': 0.0, 'occ_4': 0.0, 'occ_5': 1.0, 'occ_6': 0.0}
            else:
                data = {'occ_2': 0.0, 'occ_3': 0.0, 'occ_4': 0.0, 'occ_5': 0.0, 'occ_6': 1.0}
            print(data)
            if men_occupation == 2:
                data1 = {'occ_husb_2':1.0,'occ_husb_3':0.0,'occ_husb_4':0.0,'occ_husb_5':0.0,'occ_husb_6':0.0}
            elif men_occupation == 3:
                data1 = {'occ_husb_2': 0.0, 'occ_husb_3': 1.0, 'occ_husb_4': 0.0, 'occ_husb_5': 0.0, 'occ_husb_6': 0.0}
            elif men_occupation == 4:
                data1 = {'occ_husb_2': 0.0, 'occ_husb_3': 0.0, 'occ_husb_4': 1.0, 'occ_husb_5': 0.0, 'occ_husb_6': 0.0}
            elif men_occupation == 5:
                data1 = {'occ_husb_2': 0.0, 'occ_husb_3': 0.0, 'occ_husb_4': 0.0, 'occ_husb_5': 1.0, 'occ_husb_6': 0.0}
            else:
                data1 = {'occ_husb_2': 0.0, 'occ_husb_3': 0.0, 'occ_husb_4': 0.0, 'occ_husb_5': 0.0, 'occ_husb_6': 1.0}
            data.update(data1)
            data.update({'rate_marriage':rate_marriage,'age':age,'yrs_married':yrs_married,'children':children,'religious':religious,
                         'education':education})
            filename = 'logisticprediction.sav'
            data_final = data.values()
            values_list = list(data_final)
            values_list = [1.0] + values_list
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            prediction=loaded_model.predict([values_list])
            print(prediction[0])
            if prediction[0] == 0.0:
                prediction = "women doesn't have an affair"
            else:
                prediction = 'women have an affair'
            print('prediction is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html',prediction=prediction)
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app