# lightgrid


A Fast model parameter adjustment tool 
.author email: yan_shw@dlmu.edu.cn 

- Applicable to all machine learning algorithms and deep learning algorithms conforming to sklearn code specification such as SVM,DecisionTree,XGBoost,lightGBM,RandomForest,catBoost and so on
- Only rely on Python native code packages
- Grid search speed is extremely fast than [gridsearchCV](https://scikit-learn.org/0.16/modules/generated/sklearn.grid_search.GridSearchCV.html)
- Adapt single parameter search and multiple parameter search .even both them can be setted to run in same process
- Use given train data and test data to get the best parameter collection
- Auto save Operation results and error log , facilitate offline training

# Installation

Easiest way is to use `pip`:
```
	pip install lightgrid
```

# Usage
To use the tool, the importance content is  comprehend the difference between  `paramList` and `crossParamList`.All keys in `paramList` are irrelevant. When the program runs, it will only search the optimal value of one key at a time, and then turn to the next. All keys in the `crossParamList` are related. When the program runs, it will search for the optimal value of the free combination of all keys in the `crossParamList`. Therefore, the conclusion of `crossParamList` is often more accurate but slower. Lightgrid allows you to set `paramList` and `crossParamList` at the same time to get the best effect, but it should be noted that there can be no key intersection between `paramList` and `crossParamList`, and the number of elements in `crossParamList` should be greater than 2. detail and example is given as bellow: <br /> 

## Parameters

IN
- function: you should input a class name such as : test
- paramList: independent features assemble . type as dict ,such as {'a':[1,2,3]}
- crossParamList: features be valid in a crossed way  . type as dict ,such as {'a':[1,2,3],'b':[1,2,3]} . default: {}
- optimal_fun: optimal function ,option invoke 'R2_score' or 'succe_percent'. default :'succe_percent'
- silent: boolean,Whether to output logs during program operation. default :True
- save_model: boolean,save model or not. default :False
- x_train :train collection feature data
- y_train :train collection object data
- x_val :test collection feature data
- y_val :test collection object data

OUT
- bst_param :the best parameter collection
- bst_score :model performance under the best parameter collection and given test data

## code example
```python
from sklearn.tree import DecisionTreeClassifier  
from sklearn.datasets import load_breast_cancer
import lightgrid
data = load_breast_cancer()
x_train = data['data'][:400,:]
y_train = data['target'][:400]
x_val = data['data'][400:,:]
y_val = data['target'][400:]
DecisionTreeClassifier()

param_grid = {'max_depth':[10,20],
             'min_samples_split':[2,4,6,8,10],
             'min_samples_leaf':[1,3,5]
             }
autograd = lightgrid.lightgrid(DecisionTreeClassifier,param_grid,valid_times=1,save_model=False)
autograd.fit(x_train=x_train,y_train=y_train,x_val=x_val,y_val=y_val)
print('the best param is '+str(autograd.bst_param))
print('the best score is '+str(autograd.bst_score))
```

## Algorithm Performance  

Under different data sets, the comparison between lightgrid and gridsearchCV algorithm is shown in the table below. The reason for this situation is that lightgrid algorithm is more flexible and avoids meaningless calculation

All tests are run on a 12 core (hyperthreaded) Intel(R) Xeon(R) CPU E5-2678 v3.

|Data Set | Target | lightgrid Time| gridSearchCV Time |lightgrid score|gridSearchCV score|
| ------- | ------ | -----------| ---- | ---- | ---- | 
|[breast_cancer](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html) |0-1|0.76817s  | 1.93696s | 0.91420| 0.89940 |
|[digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html#sklearn.datasets.load_digits)|0-9| 1.50722s  | 3.25618s   | 0.77365 | 0.7728 |
|[wine](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_wine.html#sklearn.datasets.load_wine)|0-3| 0.11532s  | 0.50491s   | 0.38461 | 0.30769 |