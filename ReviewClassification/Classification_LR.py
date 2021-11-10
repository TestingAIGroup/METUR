# coding:utf-8
import os
import re

import warnings

warnings.simplefilter("ignore", UserWarning)
from matplotlib import pyplot as pet
import pandas as pd

pd.options.mode.chained_assignment = None
import xlwt
import numpy as np
import cmath
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, auc, roc_auc_score, recall_score
from sklearn.externals import joblib


def readFile():
    # cleanFilePath=""
    data = pd.read_csv('',
                       encoding='latin1', usecols=['label', 'review'])
    data.columns = ['label', 'review']
    data = data.sample(frac=1,random_state=40)
    print(data.shape)
    for row in data.head(10).iterrows():
        print(row[1]['label'], row[1]['review'])

    x_train, x_test, y_train, y_test = train_test_split(data['review'],
                                                        data['label'],
                                                        test_size=0.1,
                                                        random_state=40,
                                                        stratify=data['label'])

    print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
 

    file_path = ""
    predictResult_path = file_path + "lr_word_ngram.csv"

    pd.DataFrame(y_test).to_csv(file_path + "y_true.csv", index=True, encoding='utf-8')
    vectorizer_word = TfidfVectorizer(max_features=80000,
                                      min_df=2,
                                      max_df=0.8,
                                      analyzer='word',
                                      stop_words='english',
                                      encoding='utf-8',
                                      ngram_range=(1, 3))

    vectorizer_word.fit(x_train)

    tfidf_matrix_word_train = vectorizer_word.transform(x_train)
    tfidf_matrix_word_test = vectorizer_word.transform(x_test)

    lr_word = LogisticRegression(solver='newton-cg', max_iter=200,verbose=2, multi_class='multinomial',random_state=40)
    lr_word.fit(tfidf_matrix_word_train, y_train)
    joblib.dump(lr_word, file_path + "lr_word_4gram.pkl")

    y_pred_word = lr_word.predict(tfidf_matrix_word_test)
    pd.DataFrame(y_pred_word, columns=['y_pred']).to_csv(predictResult_path, index=False)

    y_pred_word = pd.read_csv(predictResult_path)
    pd.set_option('display.max_columns', 1000) 
    print(y_test)
    evaluation(y_test, y_pred_word, file_path)

def evaluation(y_true, y_pred, file_path):

    accuracy = accuracy_score(y_true, y_pred)
    #file_other="other";file_evaluation="featureEvaluation";file_request="featureRequest";file_issue="issueReport";file_usage="usageScenario";
    for list in range(0,5):
        TP = 0; FP = 0;  FN = 0;
        ts = pd.Series(y_pred['y_pred'].values)
        i = 0
        for row_true in y_true:
            if row_true == list and ts[i] == list:
                TP = TP + 1
            if row_true != list and ts[i] == list:
                FP = FP + 1
            if row_true == list and ts[i] != list:
                FN = FN + 1
            i = i + 1
        print("metrics:\t");
        print(TP, FP, FN)

        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        F1score = 2 * precision * recall / (precision + recall)

        print("precision:\t"); print(precision)
        print("recall:\t"); print(recall)
        print("F1score:\t"); print(F1score)
        resultDict = {}
        resultDict['TP'] = TP; resultDict['FP'] = FP; resultDict['FN'] = FN;

        resultDict['precision'] = precision;  resultDict['recall'] = recall; resultDict['F1score'] = F1score;
        result2file(resultDict, list,file_path)

def result2file(resultDict, list,file_path):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
    i = 0
    for c, v in resultDict.items():
        sheet1.write(i, 0, c)
        sheet1.write(i, 1, v)
        i = i + 1
    f.save(file_path + str(list)+"_result.xls")


if __name__ == '__main__':
    readFile()

