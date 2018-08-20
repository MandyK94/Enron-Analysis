#!/usr/bin/python

import sys
import pickle
import pandas as pd
sys.path.append("/tools/")

from tools.feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi', 'bonus'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)

data = pd.DataFrame.from_dict(data_dict, orient="index")
column_list = ['salary', 'to_messages', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 'restricted_stock_deferred', 
               'deferred_income', 'total_stock_value', 'expenses', 'from_poi_to_this_person', 'exercised_stock_options', 'from_messages',
               'other', 'from_this_person_to_poi', 'long_term_incentive', 'shared_receipt_with_poi', 'restricted_stock', 'director_fees']
for col in column_list:
    data[col] = data[col].astype(float)

### Task 2: Remove outliers

data = data.drop(data.salary.idxmax())

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
data['from_this_person_to_poi_pp'] = data.from_this_person_to_poi/ data.to_messages
data['from_poi_to_this_person_pp'] = data.from_poi_to_this_person/ data.from_messages
data['shared_receipt_with_poi_pp'] = data.shared_receipt_with_poi/ data.from_messages
data=data.fillna(0.0)
my_dataset = data.T.to_dict()

### Extract features and labels from dataset for local testing
features_list.extend(['total_payments', 'expenses', 
             'from_this_person_to_poi_pp', 'from_poi_to_this_person_pp' , 
             'exercised_stock_options'])

data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(random_state=23445, criterion="entropy")

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)