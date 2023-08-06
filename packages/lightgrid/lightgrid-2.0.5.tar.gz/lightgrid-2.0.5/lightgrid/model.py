import time
import json
import warnings


def R2_score(y_pred, y_val):
    """
    Function to get R2-score
    :param y_pred: predict sequence
    :param y_val: real sequence
    :return: R2_score
    """
    total1 = 0
    for i in range(len(y_val)):
        total1 = total1 + y_val[i]
    total2 = 0
    total3 = 0
    for i in range(len(y_val)):
        total2 = total2 + (y_val[i] - total1/len(y_val)) ** 2
        total3 = total3 + (y_val[i] - y_pred[i]) ** 2
    r2 = 1 - total3/total2
    return r2


def succe_percent(y_pred, y_val):
    """
    Function to get success percent
    :param y_pred: predict sequence
    :param y_val: real sequence
    :return:  success percent
    """
    customCount = 0
    for i in range(len(y_pred)):
        if y_pred[i] == y_val[i]:
            customCount = customCount + 1
    denominator = len(y_pred)
    return (customCount / denominator)


def timer(func):
    """
    Annotation to get  function run time
    :return:  function run time
    """
    def count_time(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print('function run time:{:.5f}s'.format(end_time - start_time))

    return count_time


def paramIterator(dictValues, resList, dictKeys, jude=True):
    """
    Procedure to get dictionary parameter collection
    :param dictValues: dcitionary values list(IN)
    :param dictKeys: dcitionary keys list (IN)
    :param jude: recursive termination condition(IN)
    :param resList:  dictionary parameter collection(OUT)
    """
    if jude: dictValues = [[[i] for i in dictValues[0]]] + dictValues[1:]
    if len(dictValues) > 2:
        for i in dictValues[0]:
            for j in dictValues[1]:
                paramIterator([[i + [j]]] + dictValues[2:], resList, dictKeys, False)
    elif len(dictValues) == 2:
        for i in dictValues[0]:
            for j in dictValues[1]:
                resList.append(dict(zip(dictKeys, i + [j])))


class lightgrid():

    def __init__(self,
                 function,
                 paramList,
                 crossParamList={},
                 optimal_fun='succe_percent',
                 valid_times = 3,
                 silent=True,
                 save_model=False):
        """auto adjust parameter  . author YSW

        Parameters
        ----------
        :param function: you should input a class name such as : test
        :param paramList: independent features assemble . type as dict ,such as {'a':[1,2,3]}
        :param crossParamList: features be valid in a crossed way  . type as dict ,such as {'a':[1,2,3]}
        :param optimal_fun: optimal function ,option invoke 'R2_score' or 'succe_percent'
        :param silent: boolean,Whether to output logs during program operation
        :param save_model: boolean,save model or not

        Examples
        --------
        >>> from sklearn.tree import DecisionTreeClassifier 
        >>> from sklearn.datasets import load_breast_cancer
        >>> import lightgrid
        >>> data = load_breast_cancer()
        >>> x_train = data['data'][:400, :]
        >>> y_train = data['target'][:400]
        >>> x_val = data['data'][400:, :]
        >>> y_val = data['target'][400:]
        >>> dc.fit(x_train, y_train)
        >>> y_pred = dc.predict(x_val)
        >>> param_grid = {'max_depth': [10, 20, 30, 40, 100],
        >>> 'min_samples_split': [2, 4, 6, 8, 10],
        >>> 'min_samples_leaf': [1, 3, 5],
        >>> 'splitter': ['best', 'random']
        >>> } 
        >>> lightgrid = lightgrid.lightgrid(DecisionTreeClassifier, param_grid)
        >>> lightgrid.fit(x_train=x_train, y_train=y_train, x_val=x_val, y_val=y_val)
        >>> lightgrid.bst_param
        ...                             # doctest: +SKIP
        ...
        {'max_depth': 10,'min_samples_split': 8,'min_samples_leaf': 3,'splitter': 'random'}
        """

        super(lightgrid, self).__init__()
        self.function = function
        self.paramList = paramList
        self.crossParamList = crossParamList
        self.optimal_fun = optimal_fun
        self.valid_times = int(valid_times)
        self.silent = silent
        self.save_model = save_model
        self.bst_param = None
        self.bst_score = None
        
        if len(list(self.crossParamList.values())) == 1:
            raise ValueError('crossParamList length should be greater than 1')     
        if len(list(set(list(paramList.keys())) & set(list(crossParamList.keys()))))  > 0:
            raise ValueError('paramList and crossParamList cannot intersect')     
        if (optimal_fun != 'R2_score') and (optimal_fun != 'succe_percent'):
            raise ValueError('optimal_fun is not exist')     
        if valid_times < 1:
            raise ValueError('valid_times should be greater than 0. You entered' + str(valid_times))
        if (silent is not True) and (silent is not False):
            raise ValueError('silent should be a boolean value. You entered' + str(silent))
        if (save_model is not True) and (save_model is not False):
            raise ValueError('save_model should be a boolean value. You entered' + str(save_model))
    @timer
    def fit(self, x_train, y_train, x_val, y_val):

        bst_param = {}
        err_log = {}

        # ordinal  search
        for key in self.paramList.keys():
            sr_flag = 0
            param_flag = 0
            for value in self.paramList[key]:
                try:
                    param = {}
                    param[key] = value
                    model = self.function(**param)

                    sr = 0
                    for i in range(self.valid_times):
                        model.fit(x_train, y_train)
                        y_pred = model.predict(x_val)
                        sr = sr + globals()[self.optimal_fun](y_pred, y_val)
                    sr = sr/self.valid_times

                    if self.silent:
                        print('[lightgrid]  ordinal test key:' + str(key) + '  value:' + str(value) +
                              '  score:' + str(sr))
                    if sr > sr_flag:
                        sr_flag = sr
                        param_flag = value
                except Exception as e:
                    print('[lightgrid]  error come in where key=' + str(key) + ' and value =' + str(value) + ' ,exception : ' + str(e))
                    err_log['key:' + str(key) + ' value:' + str(value)] = 'exception:' + str(e)
                    continue
            bst_param[key] = param_flag

        # crossed  search
        param_flag = {}
        if len(list(self.crossParamList.values())) > 1:
            resList = []
            paramIterator(list(self.crossParamList.values()), resList, list(self.crossParamList.keys()))
            sr_flag = 0
            for i in range(len(resList)):
                try:
                    model = self.function(**resList[i])

                    sr = 0
                    for i in range(self.valid_times):
                        model.fit(x_train, y_train)
                        y_pred = model.predict(x_val)
                        sr = sr + globals()[self.optimal_fun](y_pred, y_val)
                    sr = sr / self.valid_times

                    if self.silent:
                        print('[lightgrid]  crossed test dict: ' + str(resList[i]) + '  score:' + str(sr))
                    if sr > sr_flag:
                        sr_flag = sr
                        param_flag = resList[i]
                except Exception as e:
                    print('[lightgrid]  error come in where dict= ' + str(resList[i]) + ' ,exception:' + str(e))
                    err_log['dict:' + str(resList[i])] = 'exception:' + str(e)
                    continue


        bst_param = {**bst_param, **param_flag}

        self.bst_param = bst_param
        sr = 0
        model = self.function(**bst_param)
        for i in range(self.valid_times):
            model.fit(x_train, y_train)
            y_pred = model.predict(x_val)
            sr = sr + globals()[self.optimal_fun](y_pred, y_val)
        sr = sr / self.valid_times             
        self.bst_score = sr

        if self.save_model:
            tf = open("./lightgrid.json", "w")
            json.dump(self.bst_param, tf)
            tf.close()
            print('[lightgrid]  model saved success')

        if err_log == {}:
            print('[lightgrid]  everything is OK')
        else:
            tf = open("./errlog.json", "w")
            json.dump(err_log, tf)
            tf.close()
            warnings.warn('[lightgrid]  exception has occured , detail in errlog.json')

        return

    