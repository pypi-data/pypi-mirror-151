# Modelify

Modelify takes over all devops jobs from data scientists and machine learning practitioners and brings their models to production.

## Install 

```
pip install modelify
```

## Usage

Deploying LightGBM Model

```python
import pandas as pd
from sklearn.datasets import load_iris
from lightgbm import LGBMClassifier, Dataset, train as train_lgbm
import modelify
from modelify import ModelInference
from modelify.helpers import create_schema

# import data
iris = load_iris()
df= pd.DataFrame(data= np.c_[iris['data'], iris['target']],
                     columns= iris['feature_names'] + ['target'])

# train test split
train, test = train_test_split(df, test_size=0.2 )
y_train = df["target"]
X_train = df.drop(columns=["target"])

# build your model
clr = LGBMClassifier()
clr.fit(X_train, y_train)

# deployment
inference = ModelInference(model=model, framework="LIGHTGBM", inputs=create_schema(X_train))

modelify.connect("YOUR_API_KEY")

modelify.deploy(inference, app_uid="YOUR_APP_UID")

```
