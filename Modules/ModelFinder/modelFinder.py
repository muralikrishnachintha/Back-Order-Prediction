from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score,f1_score
from Modules.DataPreprocessor import dataPreprocessor

class modelFinder:

    def __init__(self, loggerObj, log_file):
        self.loggerObj = loggerObj
        self.log_file = log_file
        self.clf = RandomForestClassifier()
        self.xgb = XGBClassifier(objective='binary:logistic')
        self.preprocess = dataPreprocessor.processData(self.loggerObj, self.train_model_logs)

    def get_best_params_for_random_forest(self,df_train_complete):
        try:
            self.log_file = self.loggerObj.write_log(self.log_file, 'Entered get_best_params_for_random_forest method of modelFinder class.')

            # initializing with different combination of parameters
            self.param_grid = {"n_estimators": [ 100, 130], "criterion": ['gini', 'entropy'],
                               "max_depth": [2,3], "max_features": ['auto', 'log2']}

            df_train_down_up_sampled = self.preprocess.up_and_down_sampling(df_train_complete, 20, 'went_on_backorder')
            X_train_sampled = df_train_down_up_sampled.drop('went_on_backorder', axis=1)
            y_train_sampled = df_train_down_up_sampled['went_on_backorder']

            #Creating an object of the Grid Search class
            self.grid = GridSearchCV(estimator=self.clf, param_grid=self.param_grid, cv=5,  verbose=3)
            #finding the best parameters
            self.grid.fit(X_train_sampled, y_train_sampled)

            #extracting the best parameters
            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.max_features = self.grid.best_params_['max_features']
            self.n_estimators = self.grid.best_params_['n_estimators']

            #creating a new model with the best parameters
            self.clf = RandomForestClassifier(n_estimators=self.n_estimators, criterion=self.criterion,
                                              max_depth=self.max_depth, max_features=self.max_features)
            # training the new model
            self.clf.fit(X_train_sampled, y_train_sampled)

            self.log_file = self.loggerObj.write_log(self.log_file, 'Best Parameters for random forest have been found.')
            self.log_file = self.loggerObj.write_log(self.log_file, 'Exiting the get_best_params_for_random_forest method of modelFinder class.')

            return self.clf

        except Exception as e:
            self.log_file = self.loggerObj.write_log(self.log_file, 'An exception has occured in the get_best_params_random_forest method of modelFinder class. The exception is ' + str(e))
            self.log_file = self.loggerObj.write_log(self.log_file,'Exiting the get_best_params_for_random_forest method of modelFinder class,')

            raise Exception()

    def get_best_params_for_xgboost(self,df_train_complete):

        try:
            # initializing with different combination of parameters
            self.log_file = self.loggerObj.write_log(self.log_file, 'get_best_params_for_xgboost has been initiated.')
            self.param_grid_xgboost = {

                'learning_rate': [0.5, 0.1],
                'max_depth': [10, 20],
                'n_estimators': [ 100, 200]

            }

            df_train_down_up_sampled = self.preprocess.up_and_down_sampling(df_train_complete, 20, 'went_on_backorder')
            X_train_sampled = df_train_down_up_sampled.drop('went_on_backorder', axis=1)
            y_train_sampled = df_train_down_up_sampled['went_on_backorder']



            # Creating an object of the Grid Search class
            self.grid= GridSearchCV(XGBClassifier(),self.param_grid_xgboost, verbose=3,cv=5)
            # finding the best parameters
            self.grid.fit(X_train_sampled, y_train_sampled)

            # extracting the best parameters
            self.learning_rate = self.grid.best_params_['learning_rate']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']

            # creating a new model with the best parameters
            self.xgb = XGBClassifier(learning_rate=self.learning_rate, max_depth=self.max_depth, n_estimators=self.n_estimators)
            # training the mew model
            self.xgb.fit(X_train_sampled, y_train_sampled)

            self.log_file = self.loggerObj.write_log(self.log_file, 'Best hyperparmeters have been found for XGBoost and the model has been trained with best hyperparamters.')
            self.log_file = self.loggerObj.write_log(self.log_file, 'Exiting the the get_best_params_for_xgboost module of the modelFinder class.')

            return self.xgb

        except Exception as e:
            self.log_file = self.loggerObj.write_log(self.log_file, 'An Exception has occured in the get_best_params_for_xgboost module of the modelFinder class. The exception is '+ str(e))
            self.log_file = self.loggerObj.write_log(self.log_file, 'Exiting the the get_best_params_for_xgboost module of the modelFinder class.')

            raise Exception()

    def get_best_model(self,df_train_complete,df_test_complete):

        self.log_file = self.loggerObj.write_log(self.log_file,'Entered the get_best_model class of the modelFinder.')
        self.log_file = self.loggerObj.write_log(self.log_file, 'Process of finding the best model has started.')

        # create best model for XGBoost
        try:
            self.log_file = self.loggerObj.write_log(self.log_file,'Initiated finding the best parameters for XGBoost model.')

            print("Inside get best model")

            self.xgboost= self.get_best_params_for_xgboost(df_train_complete)

            X_test = df_test_complete.drop('went_on_backorder', axis=1)
            y_test = df_test_complete['went_on_backorder']

            self.prediction_xgboost = self.xgboost.predict(X_test) # Predictions using the XGBoost Model

            if len(y_test.unique()) == 1:
                self.xgboost_score = accuracy_score(y_test, self.prediction_xgboost)

            else:
                self.xgboost_score = f1_score(y_test, self.prediction_xgboost, average='micro') # AUC for XGBoost
            self.log_file = self.loggerObj.write_log(self.log_file, 'Best hyperparmeters have been found for XGBoost')
            self.log_file = self.loggerObj.write_log(self.log_file, 'The score with the best hyperparmeters is '+ str(self.xgboost_score))

            # create best model for Random Forest
            self.log_file = self.loggerObj.write_log(self.log_file, 'Initiated finding the best parameters for RandomForest model.')
            self.random_forest=self.get_best_params_for_random_forest(df_train_complete)
            self.prediction_random_forest=self.random_forest.predict(X_test) # prediction using the Random Forest Algorithm

            if len(X_test.unique()) == 1:
                self.random_forest_score = accuracy_score(X_test,self.prediction_random_forest)

            else:
                self.random_forest_score = f1_score(y_test, self.prediction_random_forest,average='micro')

            self.log_file = self.loggerObj.write_log(self.log_file, 'The score with the best hyperparamters is '+ str(self.random_forest_score))

            #comparing the two models
            if(self.random_forest_score <  self.xgboost_score):

                self.log_file = self.loggerObj.write_log(self.log_file, 'Best Model after comparing the scores is XGBoost.')
                self.log_file = self.loggerObj.write_log(self.log_file, 'Exiting get_best_model method.')

                return 'XGBoost',self.xgboost
            else:
                self.log_file = self.loggerObj.write_log(self.log_file, 'Best Model after comparing the scores is Random Forest.')
                self.log_file = self.loggerObj.write_log(self.log_file, 'Exiting get_best_model method.')
                return 'RandomForest',self.random_forest

        except Exception as e:
            self.log_file = self.loggerObj.write_log(self.log_file, 'An exception has occured in the get_best_model module of the modelFinder class. The exception is  ' + str(e))
            self.log_file = self.loggerObj.write_log(self.log_file, 'Exiting get_best_model method.')
            raise Exception()



