import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
import matplotlib.pyplot as plt
df = pd.read_csv('Lay1Network_new.csv')
def f(x):
    if x == 'male':
        return 1
    else:
        return 0
df['sex'] = df['sex'].apply(f)
X = df[['age','0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'place_been_to']]
y = df['trans_risk']
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.1,random_state=2)
# clf = DecisionTreeClassifier()
# clf.fit(X_train, y_train)
# clf.score(X_test, y_test)
# result = cross_val_score(clf, X, y, cv=10)
# print(result.mean())
# threshholds = np.linspace(0, 0.5, 50)
# param_grid = {'criterion':['gini', 'entropy'],
#               'min_impurity_decrease': threshholds,
#               'max_depth':range(2, 15)}
# clf = GridSearchCV(DecisionTreeClassifier())
# clf.fit(X,y)
# print("best param: {0}\nbest score: {1}".format(clf.best_params_,
#                                                 clf.best_score_))


#Random Forest
rf = RandomForestClassifier(n_estimators=90,max_features=8)
rf.fit(X_train, y_train)
score = rf.score(X_test, y_test)
result = cross_val_score(rf, X, y, cv=10)
print(result.mean())
print(score)
# rf = RandomForestClassifier(n_estimators=90)
# param_test1 = {'max_features':range(1, 10, 1)}
# gs = GridSearchCV(rf, param_test1, cv= 4)
# gs.fit(X_train, y_train)
# print(gs.cv_results_['mean_test_score'])
# print(gs.best_params_)
# print(gs.best_score_)

# scorel = []
# for i in range(0,200,10):
#     rfc = AdaBoostClassifier(n_estimators=i+1,
#                                  random_state=90)
#     score = cross_val_score(rfc,X,y,cv=10).mean()
#     scorel.append(score)
#     print(i)
#
# print(max(scorel),(scorel.index(max(scorel))*10)+1)
# plt.figure(figsize=[20,5])
# plt.plot(range(1,201,10),scorel)
# plt.show()



#adaboost
# rf = AdaBoostClassifier(n_estimators=20)
# rf.fit(X_train, y_train)
# score = rf.score(X_test, y_test)
# result = cross_val_score(rf, X, y, cv=10)
# print(result.mean())
# print(score)
