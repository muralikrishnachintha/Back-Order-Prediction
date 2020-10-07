import numpy as np


class validate_raw_data:
    """
                            Class Name: validate_raw_data
                            Description: Validates the prediction data.
                            On Failure: Raise Exception

                            Written By: Murali Krishna Chintha
                            Version: 1.0
                            Revisions: None
    """

    def __init__(self, logger_obj, log_file):

        self.raw_prediction_validation_logs = log_file
        self.logger = logger_obj

    def column_validate(self, dataframe):
        """
                                Module Name: column_validate
                                Description: Validates the number of columns and the column names.
                                Input: dataframe
                                Output: True/False
                                On Failure: Raise Exception

                                Written By: Vaishnavi Ambati
                                Version: 1.0
                                Revisions: None
        """
        try:
            self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs, 'Entered column_validate module of validateRawPredictionData class.')
            self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs, 'Data Validation for columns has Stared.')

            columns = list(dataframe.columns)

            actual_columns = ['sku','national_inv','lead_time','in_transit_qty',
                              'forecast_3_month','forecast_6_month','forecast_9_month',
                              'sales_1_month','sales_3_month','sales_6_month',
                              'sales_9_month','min_bank','potential_issue',
                              'pieces_past_due','perf_6_month_avg','perf_12_month_avg',
                              'local_bo_qty','deck_risk','oe_constraint','ppap_risk',
                              'stop_auto_buy','rev_stop']

            # checking for column data types
            object_column_list = ['potential_issue',  'deck_risk','oe_constraint','ppap_risk',
                              'stop_auto_buy','rev_stop']

            float_column_list = ['national_inv','lead_time', 'sales_1_month', 'pieces_past_due',
                                 'perf_6_month_avg','local_bo_qty']

            object_columns = list(dataframe.dtypes[dataframe.dtypes == np.object].index)
            float_columns = list(dataframe.dtypes[dataframe.dtypes == np.float64].index)

            if object_columns == object_column_list and float_columns == float_column_list:
                data_type_validate = True
            else:
                data_type_validate = False

            if columns == actual_columns and data_type_validate:
                self.logger.write_log(self.raw_prediction_validation_logs, 'Columns in the data are valid.')
                self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs,'Exited column_validate module of validateRawPredictionData class.')

                return True
            elif columns == actual_columns and not data_type_validate:
                self.logger.write_log(self.raw_prediction_validation_logs, 'Columns in the dataset are valid but the column data types are not valid.')
                self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs,'Exited column_validate module of validateRawPredictionData class.')

                return False
            else:
                self.logger.write_log(self.raw_prediction_validation_logs, 'Columns in the data are not valid.')
                self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs,'Exited column_validate module of validateRawPredictionData class.')

                return False


        except Exception as e:
            self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs,'An Exception has occured in column_validate of validateRawPredicitonData class. The Exception is ' + str(e))
            self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs, 'Exting column_validate of validateRawPredicitonData class.')
            self.raw_prediction_validation_logs.to_csv("Logs\\Prediction Validation\\prediction_validation_logs.csv")

            raise Exception




    def precentage_column_null_value_check(self, dataframe):

        """
                                Module Name: entire_column_null_value_check
                                Description: Validates the number of columns and the column names.
                                Input: dataframe
                                Output: True/False
                                On Failure: Raise Exception

                                Written By: Vaishnavi Ambati
                                Version: 1.0
                                Revisions: None
        """

        self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs, 'Entered entire_column_null_value_check of validateRawPredicitonData class.')
        self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs, 'Null Values Check has started.')
        try:

            null_values_counts = dataframe.isnull().sum()
            length_of_dataframe = dataframe.shape[0]

            column_null_check = []

            for column, null_value_count in null_values_counts.items():
                if null_value_count >= 0.75 * length_of_dataframe:
                    self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs,
                                                                                'The Column ' + str(column) + ' has only values. The Dataset Cannot be Accepted.')
                    self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs,
                                                                                'Entire Row null value check has completed.')
                    self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs,
                                                                                'Exting entireColumnNullValueCheck of validateRawPredicitonData class.')

                    column_null_check.append(True)
                else:
                    self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs,
                                                                                'No column in the Dataset has complete null values.')
                    self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs,
                                                                                'Exting entire_column_null_value_check of validateRawPredicitonData class.')

                    column_null_check.append(False)

            if False in column_null_check:
                return False
            else:
                return True

        except Exception as e:
            self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs,'An Exception has occured in entire_column_null_value_check of validateRawPredicitonData class. The Exception is ' + str(e))
            self.raw_prediction_validation_logs = self.logger.write_log(self.raw_prediction_validation_logs,'Exting entire_column_null_value_check of validateRawPredicitonData class.')
            self.raw_prediction_validation_logs.to_csv("Logs\\Prediction Validation\\prediction_validation_logs.csv")

            raise Exception