from flask import Flask,render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
import os
import pandas as pd
from Modules.PredictData import predictData
from Modules.Validation import trainValidation, predictionValidation
from Modules.TrainModel import trainModel

# UPLOAD_FOLDER = "C:\\Users\\ambat\\Desktop\\My_Django_stuff\\flask_restaurants\\files"
#     # C:\\Users\\ambat\\Desktop\\My_Django_stuff\\flask_restaurants\\files
#
app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# os.makedirs(os.path.join(app.instance_path, 'files'), exist_ok=False)

class data:
    name: str
    rating: int


@app.route('/')
def index():
    return render_template("main.html")

@app.route('/bulk.html')
def bulk():
    return render_template('bulk.html')

def prediction(filename):

    predict_valid_obj = predictionValidation.prediction_validation()
    validation = predict_valid_obj.validate_predict_data(filename)

    if validation:
        predict_obj = predictData.predictData()
        message = predict_obj.predict_data(filename)

        print(message)
        return message
    else:
        message = "Failure"
        print(message)
        return message

@app.route('/bulk_results', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['filename']
      filename = secure_filename(f.filename)
      # f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
      print(app.instance_path)
      f.save(os.path.join(app.instance_path, 'files', secure_filename(f.filename)))

      print("Filename is ", f.filename)

      message = prediction(f.filename)

      if message == 'Success':
          return render_template('bulk_results.html')

      else:
          return render_template('errors.html')
   else:
       return render_template('errors.html')


@app.route('/retrain.html', methods = ['GET', 'POST'])
def retrain():

    return render_template("retrain.html")

@app.route('/single.html', methods = ['GET', 'POST'])
def single():

    return render_template("single.html")


@app.route('/single_csv.html', methods = ['GET', 'POST'])
def single_csv():

    return render_template("single_csv.html")

@app.route('/single_inputs.html', methods = ['GET', 'POST'])
def single_inputs():

    return render_template("single_inputs.html")

@app.route('/single_results_manual.html', methods = ['GET', 'POST'])
def single_results_manual():

    if request.method == "POST":

        sku = int(request.form["sku"])
        national_inv = int(request.form["natinv"])
        lead_time = int(request.form["lt"])
        sales_1_month = int(request.form["s1m"])
        pieces_past_due = int(request.form["pieces_past_due"])
        perf_6_month_avg = int(request.form["perf_6_month_avg"])
        local_bo_qty = int(request.form["local_bo_qty"])
        deck_risk = int(request.form["deck_risk"])
        oe_constraint = int(request.form["oe_constraint"])
        ppap_risk = int(request.form["ppap_risk"])
        stop_auto_buy = int(request.form["stop_auto_buy"])
        rev_stop = int(request.form["rev_stop"])

        feature_list = [sku, national_inv, lead_time, sales_1_month, pieces_past_due, perf_6_month_avg, local_bo_qty, deck_risk, oe_constraint, ppap_risk,
                        stop_auto_buy, rev_stop]

        prediction_obj = predictData.predictData()
        sku, result = prediction_obj.predict_single_value_manual(feature_list)
        print(sku,result)


    return render_template("single_results_manual.html")

def train(filename):

    train_val_obj = trainValidation.train_validation()  # object initialization

    validation = train_val_obj.validate_train(filename)  # calling the training_validation function

    if validation:
        train_model_obj = trainModel.trainModel()  # object initialization
        train_model_obj.train_model(filename)  # training the model for the files in the table

        return 'Model has been trained successfully.'
    else:
        print('Model training is a failure.')
        return 'Data is not valid'


@app.route('/retrain_results', methods = ['GET', 'POST'])
def retrain_results():

    if request.method == 'POST':
        f = request.files['filename']
        filename = secure_filename(f.filename)
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        print(app.instance_path)
        f.save(os.path.join(app.instance_path, 'files', secure_filename(f.filename)))

        print("Filename for Train is ",f.filename)

        message = train(f.filename)

        if message == 'success':
            return render_template('retrain_results.html')

        else:
            return render_template('errors.html')


@app.route('/errors.html', methods = ['GET', 'POST'])
def errors():

    return render_template("errors.html")

@app.route('/main.html', methods = ['GET', 'POST'])
def home_main():

    return render_template("main.html")

@app.route('/home.html', methods = ['GET', 'POST'])
def home():

    return render_template("main.html")

@app.route('/top5.html', methods = ['GET', 'POST'])
def top5():

    pred_data = pd.read_csv("Prediction_Output_Files\\predictions.csv").head()
    names_list = list(pred_data['sku'])
    age_list = list(pred_data['went_on_backorder'])

    dest1 = data()
    dest1.name = names_list[0]
    dest1.rating = age_list[0]

    dest2 = data()
    dest2.name = names_list[1]
    dest2.rating = age_list[1]

    dest3 = data()
    dest3.name = names_list[2]
    dest3.rating = age_list[2]

    dest4 = data()
    dest4.name = names_list[3]
    dest4.rating = age_list[3]

    dest5 = data()
    dest5.name = names_list[4]
    dest5.rating = age_list[4]

    final_list = [dest1, dest2, dest3, dest4, dest5]

    # return render(request, "top5.html", {'result':final_list})
    return render_template("top5.html", tasks = final_list)

@app.route('/bottom5.html', methods = ['GET', 'POST'])
def bottom5():

    pred_data = pd.read_csv("Prediction_Output_Files\\predictions.csv").tail()
    names_list = list(pred_data['sku'])
    age_list = list(pred_data['went_on_backorder'])

    dest1 = data()
    dest1.name = names_list[0]
    dest1.rating = age_list[0]

    dest2 = data()
    dest2.name = names_list[1]
    dest2.rating = age_list[1]

    dest3 = data()
    dest3.name = names_list[2]
    dest3.rating = age_list[2]

    dest4 = data()
    dest4.name = names_list[3]
    dest4.rating = age_list[3]

    dest5 = data()
    dest5.name = names_list[4]
    dest5.rating = age_list[4]

    final_list = [dest1, dest2, dest3, dest4, dest5]

    # return render(request, "top5.html", {'result':final_list})
    return render_template("top5.html", tasks = final_list)


if __name__ == "__main__":
    app.run(debug=True)