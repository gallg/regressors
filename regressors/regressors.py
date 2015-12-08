# -*- coding: utf-8 -*-

"""This module contains core classes for regression models."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from sklearn import decomposition as dcomp
from sklearn import linear_model as lm
from sklearn import preprocessing

from . import stats


class PCR(object):
    """Principle components regression model.

    This model solves a regression model after standard scaling the X
    data and performing PCA to reduce the dimensionality of X. This class
    simply creates a pipeline that utilizes:

        1. sklearn.preprocessing.StandardScaler
        2. sklearn.decomposition.PCA
        3. a supported sklearn.linear_model

    Attributes of the class mimic what is provided by scikit-learn's PCA and
    linear model classes. Additional attributes specifically relevant to PCR
    are also provided, such as :py:attr:`.PCR.beta_coef_`.

    Parameters
    ----------
    n_components : int, float, None, str
        Number of components to keep when performing PCA. If n_components
        is not set all components are kept::

            n_components == min(n_samples, n_features)

        If n_components == 'mle', Minka\'s MLE is used to guess the
        dimension. If ``0 < n_components < 1``, selects the number of
        components such that the amount of variance that needs to be
        explained is greater than the percentage specified by n_components.
    regression_type : str
        The type of regression classifier to use. Must be one of 'ols',
        'lasso', 'ridge', or 'elasticnet'.
    n_jobs : int (optional)
        The number of jobs to use for the computation. If ``n_jobs=-1``, all
        CPUs are used. This will only increase speed of computation for
        n_targets > 1 and sufficiently large problems.
    alpha : float (optional)
        Used when regression_type is 'lasso', 'ridge', or 'elasticnet'.
        Represents the constant that multiplies the penalty terms. Setting
        ``alpha=0`` is equivalent to ordinary least square and it is advised
        in that case to instead use ``regression_type='ols'``. See the
        scikit-learn documentation for the chosen regression model for more
        information in this parameter.
    l1_ratio : float (optional)
        Used when regression_type is 'elasticnet'. The ElasticNet mixing
        parameter, with ``0 <= l1_ratio <= 1``. For ``l1_ratio = 0`` the
        penalty is an L2 penalty. ``For l1_ratio = 1`` it is an L1 penalty.
        For ``0 < l1_ratio < 1``, the penalty is a combination of L1 and L2.

    Attributes
    ----------
    scaler : sklearn.preprocessing.StandardScaler, None
        The StandardScaler object used to center the X data and scale to unit
        variance. Must have ``fit()`` and ``transform()`` methods.
        Can be overridden prior to fitting to use a different scaler::

            pcr = PCR()
            # Change StandardScaler options
            pcr.scaler = StandardScaler(with_mean=False, with_std=True)
            pcr.fit(X, y)

        The scaler can also be removed prior to fitting (to not scale X during
        fitting or predictions) with `pcr.scaler = None`.
    prcomp : sklearn.decomposition.PCA
        The PCA object use to perform PCA. This can also be accessed in the same
        way as the scaler.
    regression : sklearn.linear_model
        The linear model object used to perform regression. Must have ``fit()``
        and ``predict()`` methods. This defaults to OLS using scikit-learn's
        LinearRegression classifier, but can be overridden either using the
        `regression_type` parameter when instantiating the class, or
        by replacing the regression model with a different on prior to fitting::

            pcr = PCR(regression_type='ols')
            # Examine the current regression model
            print(pcr.regression)
            LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1,
                normalize=False)
            # Use Lasso regression with cross-validation instead of OLS
            pcr.regression = linear_model.LassoCV(n_alphas=200)
            print(pcr.regression)
            LassoCV(alphas=None, copy_X=True, cv=None, eps=0.001,
                fit_intercept=True, max_iter=1000, n_alphas=200, n_jobs=1,
                normalize=False, positive=False, precompute='auto',
                random_state=None, selection='cyclic', tol=0.0001,
                verbose=False)
            pcr.fit(X, y)
    """

    def __init__(self, n_components=None, regression_type='ols',
                 alpha=1.0, l1_ratio=0.5, n_jobs=1):
        # Store class parameters
        self.n_components = n_components
        self.n_jobs = n_jobs
        # Create scaler and PCA models
        self.scaler = preprocessing.StandardScaler()
        self.prcomp = dcomp.PCA()
        # Create regression classifier
        regression_class = {'ols': lm.LinearRegression, 'lasso': lm.Lasso,
                            'ridge': lm.Ridge, 'elasticnet': lm.ElasticNet}
        self.regression = regression_class[regression_type]()

    @property
    def beta_coef_(self):
        """
        Returns
        -------
        numpy.ndarray
            Beta coefficients, corresponding to coefficients in the original
            space and dimension of X. These are calculated as
            :math:`B = A \cdot P`, where :math:`A` is a vector of the
            coefficients obtained from regression on the principle components
            and :math:`P` is the matrix of loadings from PCA.
        """
        return stats.pcr_beta_coef(self.regression, self.prcomp)

    def fit(self, X, y):
        if self.scaler is not None:
            x_scaled = self.scaler.fit_transform(X)
        else:
            x_scaled = X
        x_reduced = self.prcomp.fit_transform(x_scaled)
        self.regression.fit(x_reduced, y)

    def predict(self, X):
        if self.scaler is not None:
            x_scaled = self.scaler.fit_transform(X)
        else:
            x_scaled = X
        x_reduced = self.prcomp.transform(x_scaled)
        self.regression.predict(x_reduced)

    def score(self):
        pass

