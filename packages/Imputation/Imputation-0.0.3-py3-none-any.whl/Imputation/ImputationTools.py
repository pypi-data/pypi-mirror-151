import pandas as pd
import numpy as np
import Imputation.gain
import Imputation.utils
import random
import itertools
import matplotlib.pyplot as plt
import seaborn as sns

def unique_non_null(col_data, col_name):
    """
    Find the unique values given the data and the variable name
    :param col_data: Data in pandas series
    :param col_name: Name of the variable
    :return: A list of variables name generated from variable name combine with unique value
    """
    cat = col_data.dropna().unique()
    return [col_name + '_' + x for x in cat]


def get_all_unique_categories(df: object) -> object:
    """
    This function extract all the uniques values for each categorical column
    :param df: Data in pandas data frame
    :return: All possible unique values from each variable. For numerical variable only the name will be addded.
    """
    categories = []  # keep all categories
    for i in df.columns:
        if df[i].dtype in ['object', 'bool', 'category']:
            categories.extend(unique_non_null(df[i], i))
        else:
            categories.append(i)
    return categories


class ImputeTransformer():
    """
    A transformer used for transforming data into format ready for imputation.
    """

    def __init__(self, categories=None):
        self.categories = categories
        self.columns = []
        self.categorical_vars = []
        self.numerical_vars = []

    def fit(self, x, y=None):
        if self.categories is None:
            self.categories = get_all_unique_categories(x)
        self.columns = x.columns
        self.categorical_vars = x.select_dtypes(include=object).columns
        self.numerical_vars = x.select_dtypes(include=np.number).columns
        return self

    def transform(self, x):
        """
        Transform the original data into a format suitable for imputation
        :param x: Data to transform in pandas data frame
        :return: Transformed data
        """
        # get dummies
        x_dummies = pd.get_dummies(x)
        x_dummies = x_dummies.reindex(columns=self.categories, fill_value=0)

        # for each categorical column, change all 0 to Nan
        for c in x.columns:
            extracted_cols = [s for s in self.categories if s.startswith(c + '_')]
            if extracted_cols:
                zero_cond = (x_dummies[extracted_cols] == 0).all(axis=1)
                x_dummies.loc[zero_cond, extracted_cols] = np.nan
        return x_dummies

    def inverse_transform(self, x):
        """
        Tranform the data into original format
        :param x: Data to transform
        :return: Data in original format
        """
        gain_df = pd.DataFrame(columns=self.categorical_vars)
        for i in self.categorical_vars:
            gain_df[i] = x[x.columns[x.columns.str.startswith(i)]].idxmax(
                axis=1).str.replace(i + '_', '')
        # add in the numerical bit
        df = pd.merge(gain_df, x[self.numerical_vars], left_index=True, right_index=True)
        # reindex
        df = df.reindex(columns=self.columns)
        return df


'''
This function impute using generative adversarial network
'''


def impute_gain(df, categories=None, gain_param=None, no_set=1):
    """
    This function perform data imputation using generative adversarial network algorithm.
    :param df: Data in pandas data frame
    :param categories: A list of possible categories. This is useful when data set does not contain all possible categories.
    :param gain_param: A parameters used in GAIN algorithm
    :param no_set: Number of imputed data sets
    :return: A list of imputed data sets
    """
    if categories is None:
        im = ImputeTransformer()
    else:
        im = ImputeTransformer(categories)
    im.fit(df)
    df_trans = im.transform(df)

    if gain_param is None:
        gain_param = {'batch_size': min(len(df), 16, 32, 64, 128, 256), 'hint_rate': 0.3, 'alpha': 0.3,
                      'iterations': 100}

    imputed_data = []
    for i in range(no_set):
        imputed = Imputation.gain.gain(df_trans.to_numpy(), gain_param)
        imputed_df = pd.DataFrame(imputed, columns=im.categories, index=df.index)
        # reverse back
        imputed_data.append(im.inverse_transform(imputed_df))
    return imputed_data


def MCAR_gen(dataset, missing_rate):
    """
    A function to generate missing data (Missing Completely At Random)
    :param dataset: A complete data set in pandas data frame
    :param missing_rate: A missing rate value must be > 0
    :return: A data with missing data
    """
    if missing_rate > 0:
        df = dataset.copy()
        a_list = range(len(df))
        missing_list = [x for x in a_list if random.random() < missing_rate]
        # for esch missing index, randomly create missing data
        for i in missing_list:
            df.iloc[i, random.sample(range(len(df.columns)), 1)] = np.nan
        return df


def mae_mixed(y_true, predictions, method='all'):
    """
    Calculate the Mean Absolute Error for numerical, categorical and mixed-types data set
    :param y_true: Ground truth in pandas data frame
    :param predictions: Prediction in pandas data frame
    :param method: Use 'all' for mixed data type, 'numerical' for numerical data, 'categorical' for categorical data
    :return: Mean Absolute Error
    """
    err = []
    if method in ['categorical', 'all']:
        categorical_vars = y_true.select_dtypes(include=object).columns
        err.append(np.mean(np.mean(y_true[categorical_vars] != predictions[categorical_vars])))

    if method in ['numeric', 'all']:
        numeric_vars = y_true.select_dtypes(include=np.number).columns
        y_true, predictions = np.array(y_true[numeric_vars]), np.array(predictions[numeric_vars])
        err.append(np.mean(np.abs(y_true - predictions)))
    return np.sum(err)


def find_optimal_param(df, categories=None, batch_size=[64], hint_rate=[0.3], alpha=[0.3], iterations=[100],
                       missing_rate=0.5):
    """
    Find the optimal parameters for GAIN imputation
    :param df: Missing data set in pandas data frame
    :param categories: A list of possible categories. This is useful when data set does not contain all possible categories.
    :param batch_size: A batch size used in GAIN training
    :param hint_rate: A hint rate used in discriminator
    :param alpha: Learning rate
    :param iterations: Number of iterations
    :param missing_rate: Missing rate will be used to construct missing data set used for training
    :return: An optimal parameter, and a pandas data frame containing results from the search
    """
    complete = df.dropna()
    # introduce missingness
    missing_df = MCAR_gen(complete, missing_rate)

    # get possible param
    params = [batch_size, hint_rate, alpha, iterations]
    possible_params = list(itertools.product(*params))

    # use gain to impute
    print('Searching...')
    perf = []
    for p in possible_params:
        gain_param = {'batch_size': int(p[0]), 'hint_rate': p[1], 'alpha': p[2], 'iterations': int(p[3])}
        imputed_train = impute_gain(missing_df, categories=categories, gain_param=gain_param, no_set=1)
        gain_impute = imputed_train[0]
        # need to calculate the performance
        perf.append(mae_mixed(complete, gain_impute))

    # select the param with the smallest mae
    results = pd.DataFrame(possible_params, columns=['batch_size', 'hint_rate', 'alpha', 'iterations'])
    results.batch_size = results.batch_size.astype(int)
    results.iterations = results.iterations.astype(int)
    results['perf'] = perf
    best = results.loc[results.perf.idxmin()]
    optim = {'batch_size': int(best.batch_size), 'hint_rate': best.hint_rate, 'alpha': best.alpha,
             'iterations': int(best.iterations)}
    print(optim)
    return optim, results
