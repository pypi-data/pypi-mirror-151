# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['instrumentum',
 'instrumentum.analysis',
 'instrumentum.feature_generation',
 'instrumentum.feature_preprocess',
 'instrumentum.feature_selection',
 'instrumentum.image_processing',
 'instrumentum.model_tuning',
 'instrumentum.time_series',
 'instrumentum.utils']

package_data = \
{'': ['*']}

install_requires = \
['fastcluster>=1.2.6,<2.0.0',
 'joblib>=1.1.0,<2.0.0',
 'numpy>=1.21.2,<2.0.0',
 'optbinning>=0.13.0,<0.14.0',
 'optuna>=2.10.0,<3.0.0',
 'pandas>=1.3.3,<2.0.0',
 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'instrumentum',
    'version': '0.8.12',
    'description': 'General utilities for data science projects',
    'long_description': '# instrumentum\n\nGeneral utilities for data science projects. \n\n\nThe goal of this repository is to consolidate functionalities that are tipically not found in other packages, and can facilitate some steps during a data science project. \n\nThe classes created in instrumentum -tipically- inherit from sklearn, which makes them easier to work with, and reuse some code that has been extensively battle-tested. \nClasses use parallelism whenever possible.\n\n\n1. Feature Generation\n2. Model Tuning\n3. Feature Selection \n4. Dashboards & Plots\n   \n\n## Feature Generation\n\nClass Interactions offers an easy way to create combinatiors of existing features. It is a lightweight class that can be extended with minimum effort.\n\nThis simple example showcase how this class can be used with a small DataFrame. The degree indicates how the different columns will be combined (careful, it grows exponentially)\n\n```python\narr = np.array([[5, 2, 3], [5, 2, 3], [1, 2, 3]])\narr = pd.DataFrame(arr, columns=["a", "b", "c"])\n\ninteractions = Interactions(operations=["sum", "prod"], degree=(2, 3), verbose=logging.DEBUG)\ninteractions.fit(arr)\n\n\npd.DataFrame(interactions.transform(arr), columns=interactions.get_feature_names_out())\n```\nDepending on the verbosity, the output can provide a large degree of information\n\n<img src="images/interactions.png"> \n\n## Model Tuning\n\nClass OptunaSearchCV implements a sklearn wrapper for the great Optuna class. It provides a set of distribution parameters that can be easily extended. In this example it makes use of the dispatcher by fetching a decision tree (which is named after the Sklearn class)\n\n```python\nsearch_function = optuna_param_disp[DecisionTreeClassifier.__name__]\ncv = RepeatedStratifiedKFold(n_splits=5, n_repeats=2)\n\nos = OptunaSearchCV(\n    estimator=DecisionTreeClassifier(),\n    scoring="roc_auc",\n    cv=cv,\n    search_space=search_function,\n    n_iter=5,\n)\nos.fit(X_train, y_train)\n```\n\nThe output presents all the details depending on the verbosity\n\n<img src="images/OptunaWrapper.png"> \n\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`instrumentum` was created by Federico Montanana. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`instrumentum`  uses:\n- Optbining for bining the visuals: https://github.com/guillermo-navas-palencia/optbinning\n',
    'author': 'Federico Montanana',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
