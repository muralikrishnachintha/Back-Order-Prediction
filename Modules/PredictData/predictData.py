from Modules.appLogger import application_logger
from Modules.DataLoader import predictionDataLoader
from Modules.SaveLoadModel import saveLoadModel
from Modules.DataPreprocessor import dataPreprocessor
import pandas as pd

class predictData:
    """
                            Class Name: predictData
                            Description: Predicts the rating of a restaurant based on the inputs.
                            Input: None
                            Output: CSV file containing the ratings of the restaurants given in the input file.
                            On Failure: Raise Exception

                            Written By: Vaishnavi Ambati
                            Version: 1.0
                            Revisions: None
    """

    def __init__(self):

        try:
            self.prediction_logs = pd.read_csv('Logs\\Prediction Logs\\prediction_logs.csv')
            self.prediction_logs.drop('Unnamed :0', axis = 1, inplace= True)
        except:
            self.prediction_logs = pd.DataFrame(columns=['date','time','logs'])

        self.loggerObj = application_logger.logger()
        self.data_loaderObj = predictionDataLoader.predictionDataLoader(logger_obj= self.loggerObj, log_file = self.prediction_logs)
        self.load_modelObj = saveLoadModel.saveLoadModel(loggerObj= self.loggerObj, log_file = self.prediction_logs)
        self.preprocessObj = dataPreprocessor.processData(logger_object= self.loggerObj, log_file = self.prediction_logs)

    def predict_data(self, filename):
        """
                                Class Name: predict_data
                                Description: Predicts the rating of a restaurant based on the inputs.
                                Input: None
                                Output: CSV file containing the ratings of the restaurants given in the input file.
                                On Failure: Raise Exception

                                Written By: Vaishnavi Ambati
                                Version: 1.0
                                Revisions: None
        """

        try:
            self.prediction_logs = self.loggerObj.write_log(self.prediction_logs, "Prediction of data has started")
            self.prediction_logs = self.loggerObj.write_log(self.prediction_logs,"Entered predict_data of predictData class")

            prediction_data = self.data_loaderObj.load_prediction_data(filename)

            #preprocess the data before loading the model
            preprocessed_prediction_data = self.preprocessObj.preprocess_prediction_data(prediction_data)

            sku_ids = preprocessed_prediction_data['sku']
            preprocessed_prediction_data.drop('sku', axis=1, inplace= True)

            #loading the model.
            model = self.load_modelObj.load_model()

            #predciting using the loaded model.
            predictions = model.predict(preprocessed_prediction_data)

            predictions_dataframe = pd.DataFrame(predictions,columns= ['went_on_backorder'])

            sku_ids_dataframe = pd.DataFrame(sku_ids)

            # concatenating ratings and dataframes.
            sku_ids_dataframe.reset_index(inplace=True)
            predictions_dataframe.reset_index(inplace=True)

            #concatenating ratings and dataframes.
            predictions_csv = pd.concat([sku_ids_dataframe['sku'],predictions_dataframe['went_on_backorder']], axis=1)

            predictions_csv.to_csv('Prediction_Output_Files\\predictions.csv')

            self.prediction_logs = self.loggerObj.write_log(self.prediction_logs, "Prediction of Data is a success.")
            self.prediction_logs = self.loggerObj.write_log(self.prediction_logs, "Exiting the predict_data method of predictData class.")

            self.prediction_logs.to_csv("Logs\\Prediction Logs\\prediction_logs.csv", index= False)

            return "Success"

        except Exception as e:

            self.prediction_logs = self.loggerObj.write_log(self.prediction_logs, "Exception occured in predict_data method of predictData class. The exception is " + str(e))
            self.prediction_logs = self.loggerObj.write_log(self.prediction_logs,'Exiting the predict_data method of predictData class.')
            self.prediction_logs.to_csv("Logs\\Prediction Logs\\prediction_logs.csv", index= False)

            raise Exception

    def predict_single_value_manual(self, info_list):
        """
                                       Class Name: predict_data
                                       Description: Predicts the rating of a restaurant based on the input.
                                       Input: None
                                       Output: Rating.
                                       On Failure: Raise Exception

                                       Written By: Vaishnavi Ambati
                                       Version: 1.0
                                       Revisions: None
               """
        try:
            self.prediction_logs = self.loggerObj.write_log(self.prediction_logs, "Prediction of data has started")
            self.prediction_logs = self.loggerObj.write_log(self.prediction_logs, "Entered predict_single_value_manual of predictData class")

            sku, X_values = info_list[0], info_list[1:]

            model = self.load_modelObj.load_model()

            features = ['national_inv', 'lead_time', 'sales_1_month', 'pieces_past_due',
                        'perf_6_month_avg', 'local_bo_qty', 'deck_risk', 'oe_constraint',
                        'ppap_risk', 'stop_auto_buy', 'rev_stop']

            value_dict = dict(zip(features, X_values))

            dataframe = pd.DataFrame(data=value_dict, index = [0])

            result = model.predict(dataframe)

            print(result)

            self.prediction_logs = self.loggerObj.write_log(self.prediction_logs, "Prediction of Data is a success.")
            self.prediction_logs = self.loggerObj.write_log(self.prediction_logs,"Exiting the predict_single_value_manual method of predictData class.")

            self.prediction_logs.to_csv("Logs\\Prediction Logs\\prediction_logs.csv", index=False)

            return sku, result

        except Exception as e:

            self.prediction_logs = self.loggerObj.write_log(self.prediction_logs,"Exception occured in predict_single_value_manual method of predictData class. The exception is " + str(e))
            self.prediction_logs = self.loggerObj.write_log(self.prediction_logs,'Exiting the predict_single_value_manual method of predictData class.')
            self.prediction_logs.to_csv("Logs\\Prediction Logs\\prediction_logs.csv", index=False)

            raise Exception




