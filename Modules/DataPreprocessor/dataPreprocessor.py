import ast
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import resample


class processData:
    """
                            Class Name: processData
                            Description: Preprocess the data.
                            Input: logger_obj, log_file
                            On Failure: Raise Exception

                            Written By: Vaishnavi Ambati
                            Version: 1.0
                            Revisions: None
    """

    def __init__(self, logger_object, log_file):

        self.loggerObj = logger_object
        self.log_file = log_file


    def preprocess_training_data(self, dataframe):
        """
             Method Name: preprocess_training_data
             Description: Preprocess the training data.
             Input: dataframe
             Input Type: dataframe
             Onput: Returns a processsed dataframe.

             Written By: Vaishnavi Ambati
             Version: 1.0
             Revisions: None
        """

        try:

            self.log_file = self.loggerObj.write_log(self.log_file, 'Entered preprocess_training_data of dataProcessor class')
            self.log_file = self.loggerObj.write_log(self.log_file, 'Data preprocessing has been initiated.')

            # Converting categorical columns into binary as there are only 2 classes for these columns
            cat_vars = ['potential_issue', 'deck_risk', 'oe_constraint', 'ppap_risk', 'stop_auto_buy', 'rev_stop',
                        'went_on_backorder']

            for var in cat_vars:
                dataframe[var] = dataframe[var].map({'No': 0, 'Yes': 1})

            # Replace NaNs in the dataset with

            # perf_6_month_avg
            dataframe.perf_6_month_avg = dataframe.perf_6_month_avg.fillna(dataframe.perf_6_month_avg.median())

            # perf_12_month_avg
            dataframe.perf_12_month_avg = dataframe.perf_12_month_avg.fillna(dataframe.perf_12_month_avg.median())

            # lead_time
            dataframe.lead_time = dataframe.lead_time.fillna(dataframe.lead_time.median())

            features = ['sku', 'national_inv', 'lead_time', 'sales_1_month', 'pieces_past_due',
                        'perf_6_month_avg', 'local_bo_qty', 'deck_risk', 'oe_constraint',
                        'ppap_risk', 'stop_auto_buy', 'rev_stop','went_on_backorder']

            df_features = dataframe[features]

            # dropping the null values in other features
            df_features = df_features.dropna()

            self.log_file = self.loggerObj.write_log(self.log_file,'Data Preprocessing has completed. Exiting the preprocess_training_data method of dataPreprocessor class.')

            return df_features

        except Exception as e:

            self.log_file = self.loggerObj.write_log(self.log_file,'An error occured in the preprocess_training_data method of dataPreprocessor class. The exception is ' + str(e))
            self.log_file = self.loggerObj.write_log(self.log_file,'Exiting the preprocess_training_data method of dataPreprocessor class.')
            self.log_file.to_csv("Logs\\Prediction Logs\\prediction_logs.csv")

            raise Exception


    def scaling_training_data_columns(self, dataframe,features_list):
        """
             Method Name: scaling_training_data_columns
             Description: scales columns of training data.
             Input: dataframe
             Input Type: dataframe
             Output: Returns a scaled dataframe.

             Written By: Vaishnavi Ambati
             Version: 1.0
             Revisions: None
        """

        try:

            self.log_file = self.loggerObj.write_log(self.log_file, 'Entered scaling_training_data_columns of dataProcessor class')
            self.log_file = self.loggerObj.write_log(self.log_file, 'Scaling training data has been initiated.')

            pp_method = MinMaxScaler()
            pp_method.fit(dataframe)

            reduced_df = pp_method.transform(dataframe)
            reduced_df = pd.DataFrame(reduced_df, columns=features_list)

            self.log_file = self.loggerObj.write_log(self.log_file,'Scaling training data has completed. Exiting the scaling_training_data_columns method of dataPreprocessor class.')

            return reduced_df

        except Exception as e:

            self.log_file = self.loggerObj.write_log(self.log_file,'An error occured in the scaling_training_data_columns method of dataPreprocessor class. The exception is ' + str(e))
            self.log_file = self.loggerObj.write_log(self.log_file,'Exiting the scaling_training_data_columns method of dataPreprocessor class.')
            self.log_file.to_csv("Logs\\Prediction Logs\\prediction_logs.csv")

            raise Exception

    def up_and_down_sampling(self, dataframe,multiply_factor,target_clm):
        """
             Method Name: up_and_down_sampling
             Description: scales columns of training data.
             Input: dataframe
             Input Type: dataframe
             Output: Returns a scaled dataframe.

             Written By: Vaishnavi Ambati
             Version: 1.0
             Revisions: None
        """

        try:

            self.log_file = self.loggerObj.write_log(self.log_file, 'Entered up_and_down_sampling of dataProcessor class')
            self.log_file = self.loggerObj.write_log(self.log_file, 'Up sampling and down sampling training data has been initiated.')

            # Downsampling
            target = target_clm
            df_majority = dataframe[dataframe[target] == 0]
            df_minority = dataframe[dataframe[target] == 1]
            n_samples = len(dataframe) - (len(df_minority) * multiply_factor)
            # Downsample majority class
            df_majority_undersampled = resample(df_majority,
                                                replace=True,
                                                n_samples=n_samples,
                                                random_state=2)

            # Combine minority class with Downsampled df
            df_undersampled = pd.concat([df_majority_undersampled, df_minority])

            # Display new class counts
            print("Target value counts after downsampling: \n", df_undersampled[target].value_counts())

            # Upsampling
            df_majority = df_undersampled[df_undersampled[target] == 0]
            df_minority = df_undersampled[df_undersampled[target] == 1]
            n_samples = len(df_minority) * multiply_factor
            # Upsample minority class
            df_minority_upsampled = resample(df_minority,
                                             replace=True,
                                             n_samples=n_samples,
                                             random_state=2)

            # Combine majority values with upsampled minority df
            df_upsampled = pd.concat([df_majority, df_minority_upsampled])

            # Display new class counts
            print("\nTarget value counts after upsampling: \n", df_upsampled[target].value_counts())

            self.log_file = self.loggerObj.write_log(self.log_file,'Up sampling and down sampling of training data has completed. Exiting the up_and_down_sampling method of dataPreprocessor class.')

            return df_upsampled

        except Exception as e:

            self.log_file = self.loggerObj.write_log(self.log_file,'An error occured in the up_and_down_sampling method of dataPreprocessor class. The exception is ' + str(e))
            self.log_file = self.loggerObj.write_log(self.log_file,'Exiting the up_and_down_sampling method of dataPreprocessor class.')
            self.log_file.to_csv("Logs\\Prediction Logs\\prediction_logs.csv")

            raise Exception


    def remove_columns(self, dataframe, columns):
        """
             Method Name: remove_columns
             Description: Drops the specified columns
             Input: dataframe, columns
             Input Type: dataframe - dataframe, columns - list
             Output: Returns a dataframe without the specified columns.

             Written By: Vaishnavi Ambati
             Version: 1.0
             Revisions: None
        """

        dataframe_dropped = dataframe.drop(columns, axis=1)
        self.log_file = self.loggerObj.write_log(self.log_file,
                                                 'Columns ' + columns + ' have been removed succesfully.')

        return dataframe_dropped

    def null_value_check(self, dataframe):
        """
             Method Name: null_value_check
             Description: Checks for null values in the dataset.
             Input: dataframe
             Input Type: dataframe - dataframe
             Output: Null Value dictionary containing the columns in which null values are present and its value, True/False

             Written By: Vaishnavi Ambati
             Version: 1.0
             Revisions: None
        """

        self.log_file = self.loggerObj.write_log(self.log_file,
                                                 'Entered null_value_check method of dataPreprocessor class.')
        self.log_file = self.loggerObj.write_log(self.log_file, 'Null value check has started.')

        try:
            null_value_dict = dict()

            for column, value in dataframe.isnull().sum().items():
                if value != 0:
                    null_value_dict[column] = value

            if len(null_value_dict) > 0:
                self.log_file = self.loggerObj.write_log(self.log_file,
                                                         'Null values been checked. There are null values in the data.')
                self.log_file = self.loggerObj.write_log(self.log_file,
                                                         'Exiting the null_value_check method of the dataPreprocessor class.')
                return null_value_dict, True
            else:
                self.log_file = self.loggerObj.write_log(self.log_file,
                                                         'Null values been checked. There are no null values in the data.')
                self.log_file = self.loggerObj.write_log(self.log_file,
                                                         'Exiting the null_value_check method of the dataPreprocessor class.')
                return null_value_dict, False

        except Exception as e:
            self.log_file = self.loggerObj.write_log(self.log_file,
                                                     'An Exception has occured in the null_value_check method of dataPreprocessor class. The Exception is ' + str(
                                                         e))
            self.log_file = self.loggerObj.write_log(self.log_file,
                                                     'Exting the null_value_check method of the dataProcessor class.')
            self.log_file.to_csv("Logs\\Prediction Logs\\prediction_logs.csv")

            raise Exception

    def separate_label_feature(self, dataframe, label_column_name):
        """
             Method Name: separate_label_feature
             Description: Separates the input dataframe into two dataframe. One containing the only the specified column.
             Input: dataframe, label_column_name
             Input Type: dataframe - dataframe, label_column_name - string
             Output: Returns two dataframes X,Y

             Written By: Vaishnavi Ambati
             Version: 1.0
             Revisions: None
        """

        try:
            self.log_file = self.loggerObj.write_log(self.log_file, 'Seperating labels has started.')
            self.log_file = self.loggerObj.write_log(self.log_file,
                                                     'Entered seperate_label_feature of the dataPreprocessor class.')

            X = dataframe.drop(labels=label_column_name, axis=1)
            Y = dataframe[label_column_name]

            self.log_file = self.loggerObj.write_log(self.log_file, 'Data has been seperated succesfully.')
            self.log_file = self.loggerObj.write_log(self.log_file,
                                                     'Exiting the seperate_label_feature method of the dataPreprocessor class.')

            return X, Y
        except Exception as e:
            self.log_file = self.loggerObj.write_log(self.log_file,
                                                     'An exception occured in seperate_label_feature method of the dataPreprocessor class. The Exception is ' + str(
                                                         e))
            self.log_file = self.loggerObj.write_log(self.log_file,
                                                     'Exiting the seperate_label_feature method of the dataPreprocessor class.')
            self.log_file.to_csv("Logs\\Prediction Logs\\prediction_logs.csv")

            raise Exception()

    def preprocess_prediction_data(self, dataframe):
        """
             Method Name: preprocess_prediction_data
             Description: Preprocesses the prediction data.
             Input: dataframe
             Input Type: dataframe - dataframe
             Output: Returns dataframe

             Written By: Vaishnavi Ambati
             Version: 1.0
             Revisions: None
        """

        try:

            self.log_file = self.loggerObj.write_log(self.log_file,
                                                     'Entered preprocess_prediction_data of dataProcessor class')
            self.log_file = self.loggerObj.write_log(self.log_file, 'Data preprocessing has been initiated.')

            # sku is an id, so drop id
            # dataframe.drop('sku', axis=1, inplace=True)

            # Converting categorical columns into binary as there are only 2 classes for these columns
            cat_vars = ['potential_issue', 'deck_risk', 'oe_constraint', 'ppap_risk', 'stop_auto_buy', 'rev_stop']

            for var in cat_vars:
                dataframe[var] = dataframe[var].map({'No': 0, 'Yes': 1})

            # Replace NaNs in the dataset with

            # perf_6_month_avg
            dataframe.perf_6_month_avg = dataframe.perf_6_month_avg.fillna(dataframe.perf_6_month_avg.median())

            # perf_12_month_avg
            dataframe.perf_12_month_avg = dataframe.perf_6_month_avg.fillna(dataframe.perf_12_month_avg.median())

            # lead_time
            dataframe.lead_time = dataframe.lead_time.fillna(dataframe.lead_time.median())

            features = ['sku','national_inv', 'lead_time', 'sales_1_month', 'pieces_past_due',
                        'perf_6_month_avg','local_bo_qty', 'deck_risk', 'oe_constraint',
                        'ppap_risk', 'stop_auto_buy', 'rev_stop']

            df_features = dataframe[features]

            # dropping the null values in other features
            df_features = df_features.dropna()


            self.log_file = self.loggerObj.write_log(self.log_file,'Data Preprocessing has completed. Exiting the preprocess_prediction_data method of dataPreprocessor class.')

            return df_features

        except Exception as e:

            self.log_file = self.loggerObj.write_log(self.log_file, "Exception occured in preprocess_prediction_data method of dataPreprocessor class. Exception is " + str(e))
            self.log_file = self.loggerObj.write_log(self.log_file,'Exiting the preprocess_prediction_data method of dataPreprocessor class.')

            self.log_file.to_csv("Logs\\Prediction Logs\\prediction_logs.csv")

            raise Exception
