# -*- coding: utf-8 -*-
"""ibm_hr_attrition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aPGzsS2FHggb6G_mpGeubBK9h4hxcvFV

Chaitanya Tammineni   _______  CSC - 2017  _______   1700122C202

# IBM HR Analytics Employee Attrition & Performance.

## 1 ) Exploratory Data Analysis

## 1.1 ) Importing Various Modules
"""

# Commented out IPython magic to ensure Python compatibility.
# Ignore  the warnings
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

# data visualisation and manipulation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
import missingno as msno

#configure
# sets matplotlib to inline and displays graphs below the corressponding cell.
# % matplotlib inline  
style.use('fivethirtyeight')
sns.set(style='whitegrid',color_codes=True)

#import the necessary modelling algos.
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB

#model selection
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score,precision_score,recall_score,confusion_matrix,roc_curve,roc_auc_score
from sklearn.model_selection import GridSearchCV

from imblearn.over_sampling import SMOTE

#preprocess.
from sklearn.preprocessing import MinMaxScaler,StandardScaler,LabelEncoder,OneHotEncoder
#from sklearn.preprocessing import Imputer
from sklearn.impute import SimpleImputer

#!pip install -q matplotlib-venn
#!apt-get -qq install -y libfluidsynth

"""## 1.2 ) Reading the data from a CSV file"""

df=pd.read_csv(r'WA_Fn-UseC_-HR-Employee-Attrition.csv')

df.head()

df.shape

df.columns

"""## 1.3 ) Missing Values Treatment"""

df.info()  # no null or Nan values.

df.isnull().sum()

msno.matrix(df) # just to visualize.

"""## 1.4 ) The Features and the 'Target'"""

df.columns

df.head()

"""## 1.5 ) Univariate Analysis"""

df.describe()

"""Let us first analyze the various numeric features. To do this we can actually plot a boxplot showing all the numeric features."""

sns.factorplot(data=df,kind='box',size=10,aspect=3)

"""Note that all the features have pretty different scales and so plotting a boxplot is not a good idea. Instead what we can do is plot histograms of various continuously distributed features.
 

> We can also plot a kdeplot showing the distribution of the feature. Below I have plotted a kdeplot for the 'Age' feature. Similarly we plot for other numeric features also. Similarly we can also use a distplot from seaborn library.
"""

sns.kdeplot(df['Age'],shade=True,color='#ff4125')

sns.distplot(df['Age'])

"""Similarly we can do this for all the numerical features. Below I have plotted the subplots for the other features."""

warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

fig,ax = plt.subplots(5,2, figsize=(9,9))                
sns.distplot(df['TotalWorkingYears'], ax = ax[0,0]) 
sns.distplot(df['MonthlyIncome'], ax = ax[0,1]) 
sns.distplot(df['YearsAtCompany'], ax = ax[1,0]) 
sns.distplot(df['DistanceFromHome'], ax = ax[1,1]) 
sns.distplot(df['YearsInCurrentRole'], ax = ax[2,0]) 
sns.distplot(df['YearsWithCurrManager'], ax = ax[2,1]) 
sns.distplot(df['YearsSinceLastPromotion'], ax = ax[3,0]) 
sns.distplot(df['PercentSalaryHike'], ax = ax[3,1]) 
sns.distplot(df['YearsSinceLastPromotion'], ax = ax[4,0]) 
sns.distplot(df['TrainingTimesLastYear'], ax = ax[4,1]) 
plt.tight_layout()
plt.show()

"""Let us now analyze the various categorical features. Note that in these cases the best way is to use a count plot to show the relative count of observations of different categories."""

cat_df=df.select_dtypes(include='object')

cat_df.columns

def plot_cat(attr,labels=None):
    if(attr=='JobRole'):
        sns.factorplot(data=df,kind='count',size=5,aspect=3,x=attr)
        return
    
    sns.factorplot(data=df,kind='count',size=5,aspect=1.5,x=attr)

"""I have made a function that accepts the name of a string. In our case this string will be the name of the column or attribute which we want to analyze. The function then plots the countplot for that feature which makes it easier to visualize."""

plot_cat('Attrition')

"""######  Note that the number of observations belonging to the 'No'  category is way greater than that belonging to 'Yes' category. Hence we have skewed classes and this is a typical example of the 'Imbalanced Classification Problem'. To handle such types of problems we need to use the over-sampling or under-sampling techniques. I shall come back to this point later.

Let us now similalry analyze other categorical features.
"""

plot_cat('BusinessTravel')

"""The above plot clearly shows that most of the people belong to the 'Travel_Rarely' class. This indicates that most of the people did not have a job which asked them for frequent travelling."""

plot_cat('OverTime')

plot_cat('Department')

plot_cat('EducationField')

plot_cat('Gender')

"""Note that males are presnt in higher number."""

plot_cat('JobRole')

"""######  Similarly we can continue for other categorical features.

###### Note that the same function can also be used to better analyze the numeric discrete features like 'Education' ,'JobSatisfaction' etc...
"""

num_disc=['Education','EnvironmentSatisfaction','JobInvolvement','JobSatisfaction','WorkLifeBalance','RelationshipSatisfaction','PerformanceRating']
for i in num_disc:
     plot_cat(i)

# similarly we can intrepret these graphs.

"""## 2 ) Corelation b/w Features"""

#corelation matrix.
cor_mat= df.corr()
mask = np.array(cor_mat)
mask[np.tril_indices_from(mask)] = False
fig=plt.gcf()
fig.set_size_inches(30,12)
sns.heatmap(data=cor_mat,mask=mask,square=True,annot=True,cbar=True)

"""###### BREAKING IT DOWN
Firstly calling .corr() method on a pandas data frame returns a corelation data frame containing the corelation values b/w the various attributes.
now we obtain a numpy array from the corelation data frame using the np.array method.
nextly using the np.tril_indices.from() method we set the values of the lower half of the mask numpy array to False. this is bcoz on passing the mask to heatmap function of the seaborn it plots only those squares whose mask is False. therefore if we don't do this then as the mask is by default True then no square will appear. Hence in a nutshell we obtain a numpy array from the corelation data frame and set the lower values to False so that we can visualise the corelation. In order for a full square just use the [:] operator in mask in place of tril_ind... function.
in next step we get the refernce to the current figure using the gcf() function of the matplotlib library and set the figure size.
in last step we finally pass the necessary parameters to the heatmap function.

DATA=the corelation data frame containing the 'CORELATION' values.

MASK= explained earlier.

vmin,vmax= range of values on side bar

SQUARE= to show each individual unit as a square.

ANNOT- whether to dispaly values on top of square or not. In order to dispaly pass it either True or the cor_mat.

CBAR= whether to view the side bar or not.

###### SOME INFERENCES FROM THE ABOVE HEATMAP

1. Self relation ie of a feature to itself is equal to 1 as expected.

2. JobLevel is highly related to Age as expected as aged employees will generally tend to occupy higher positions in the company.

3. MonthlyIncome is very strongly related to joblevel as expected as senior employees will definately earn more.

4. PerformanceRating is highly related to PercentSalaryHike which is quite obvious.

5. Also note that TotalWorkingYears is highly related to JobLevel which is expected as senior employees must have worked for a larger span of time.

6. YearsWithCurrManager is highly related to YearsAtCompany.

7. YearsAtCompany is related to YearsInCurrentRole.

Note that we can drop some highly corelated features as they add redundancy to the model but since the corelation is very less in genral let us keep all the features for now. In case of highly corelated features we can use something like Principal Component Analysis(PCA) to reduce our feature space.
"""

df.columns

"""## 3 ) Feature Selection

## 3.1 ) Plotting the Features against the 'Target' variable.

####  3.1.1 ) Age

Note that Age is a continuous quantity and therefore we can plot it against the Attrition using a boxplot.
"""

sns.factorplot(data=df,y='Age',x='Attrition',size=5,aspect=1,kind='box')

"""Note that the median as well the maximum age of the peole with 'No' attrition is higher than that of the 'Yes' category. This shows that peole with higher age have lesser tendency to leave the organisation which makes sense as they may have settled in the organisation.

#### 3.1.2 ) Department

Note that both Attrition(Target) as well as the Deaprtment are categorical. In such cases a cross-tabulation is the most reasonable way to analyze the trends; which shows clearly the number of observaftions for each class which makes it easier to analyze the results.
"""

df.Department.value_counts()

sns.factorplot(data=df,kind='count',x='Attrition',col='Department')

pd.crosstab(columns=[df.Attrition],index=[df.Department],margins=True,normalize='index') # set normalize=index to view rowwise %.

"""Note that most of the observations corresspond to 'No' as we saw previously also. About 81 % of the people in HR dont want to leave the organisation and only 19 % want to leave. Similar conclusions can be drawn for other departments too from the above cross-tabulation.

#### 3.1.3 ) Gender
"""

pd.crosstab(columns=[df.Attrition],index=[df.Gender],margins=True,normalize='index') # set normalize=index to view rowwise %.

"""About 85 % of females want to stay in the organisation while only 15 % want to leave the organisation. All in all 83 % of employees want to be in the organisation with only being 16% wanting to leave the organisation or the company.

#### 3.1.4 ) Job Level
"""

pd.crosstab(columns=[df.Attrition],index=[df.JobLevel],margins=True,normalize='index') # set normalize=index to view rowwise %.

"""People in Joblevel 4 have a very high percent for a 'No' and a low percent for a 'Yes'. Similar inferences can be made for other job levels.

#### 3.1.5 ) Monthly Income
"""

sns.factorplot(data=df,kind='bar',x='Attrition',y='MonthlyIncome')

"""Note that the average income for 'No' class is quite higher and it is obvious as those earning well will certainly not be willing to exit the organisation. Similarly those employees who are probably not earning well will certainly want to change the company.

#### 3.1.6 ) Job Satisfaction
"""

sns.factorplot(data=df,kind='count',x='Attrition',col='JobSatisfaction')

pd.crosstab(columns=[df.Attrition],index=[df.JobSatisfaction],margins=True,normalize='index') # set normalize=index to view rowwise %.

"""Note this shows an interesting trend. Note that for higher values of job satisfaction( ie more a person is satisfied with his job) lesser percent of them say a 'Yes' which is quite obvious as highly contented workers will obvioulsy not like to leave the organisation.

#### 3.1.7 ) Environment Satisfaction
"""

pd.crosstab(columns=[df.Attrition],index=[df.EnvironmentSatisfaction],margins=True,normalize='index') # set normalize=index to view rowwise %.

"""Again we can notice that the relative percent of 'No' in people with higher grade of environment satisfacftion.

#### 3.1.8 ) Job Involvement
"""

pd.crosstab(columns=[df.Attrition],index=[df.JobInvolvement],margins=True,normalize='index') # set normalize=index to view rowwise %.

"""#### 3.1.9 ) Work Life Balance"""

pd.crosstab(columns=[df.Attrition],index=[df.WorkLifeBalance],margins=True,normalize='index') # set normalize=index to view rowwise %.

"""Again we notice a similar trend as people with better work life balance dont want to leave the organisation.

#### 3.1.10 ) RelationshipSatisfaction
"""

pd.crosstab(columns=[df.Attrition],index=[df.RelationshipSatisfaction],margins=True,normalize='index') # set normalize=index to view rowwise %.

"""###### Notice that I have plotted just some of the important features against out 'Target' variable i.e. Attrition in our case. Similarly we can plot other features against the 'Target' variable and analye the trends i.e. how the feature effects the 'Target' variable.

## 3.2 ) Feature Selection
"""

df.drop(['BusinessTravel','DailyRate','EmployeeCount','EmployeeNumber','HourlyRate','MonthlyRate'
          ,'NumCompaniesWorked','Over18','StandardHours', 'StockOptionLevel','TrainingTimesLastYear'],axis=1,inplace=True)

"""##  4 ) Preparing Dataset

## 4.1 ) Feature Encoding

I have used the Label Encoder from the scikit library to encode all the categorical features.
"""

def transform(feature):
    le=LabelEncoder()
    df[feature]=le.fit_transform(df[feature])
    print(le.classes_)

cat_df=df.select_dtypes(include='object')
cat_df.columns

for col in cat_df.columns:
    transform(col)

df.head() # just to verify.

"""## 4.2 ) Feature Scaling.

The scikit library provides various types of scalers including MinMax Scaler and the StandardScaler. Below I have used the StandardScaler to scale the data.
"""

scaler=StandardScaler()
scaled_df=scaler.fit_transform(df.drop('Attrition',axis=1))
X=scaled_df
Y=df['Attrition'].to_numpy()

"""## 4.3 ) Splitting the data into training and validation sets"""

x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.25,random_state=42)

"""## 5 ) Modelling

## 5.1 ) Handling the Imbalanced dataset

## 5.1.1 ) Oversampling the Minority or Undersampling the Majority Class
"""

oversampler=SMOTE(random_state=42)
x_train_smote,  y_train_smote = oversampler.fit_sample(x_train,y_train)

"""## 5.1.2 ) Using the Right Evaluation Metric

## 5.2 ) Building A Model & Making Predictions
"""

def compare(model):
    clf=model
    clf.fit(x_train_smote,y_train_smote)
    pred=clf.predict(x_test)
    
    # Calculating various metrics
    
    acc.append(accuracy_score(pred,y_test))
    prec.append(precision_score(pred,y_test))
    rec.append(recall_score(pred,y_test))
    auroc.append(roc_auc_score(pred,y_test))

acc=[]
prec=[]
rec=[]
auroc=[]
models=[SVC(kernel='rbf'),RandomForestClassifier(),GradientBoostingClassifier()]
model_names=['rbfSVM','RandomForestClassifier','GradientBoostingClassifier']

for model in range(len(models)):
    compare(models[model])
    
d={'Modelling Algo':model_names,'Accuracy':acc,'Precision':prec,'Recall':rec,'Area Under ROC Curve':auroc}
met_df=pd.DataFrame(d)
met_df

"""## 5.3 ) Comparing Different Models"""

def comp_models(met_df,metric):
    sns.factorplot(data=met_df,x=metric,y='Modelling Algo',size=5,aspect=1.5,kind='bar')
    sns.factorplot(data=met_df,y=metric,x='Modelling Algo',size=7,aspect=2,kind='point')

comp_models(met_df,'Accuracy')

comp_models(met_df,'Precision')

comp_models(met_df,'Recall')

comp_models(met_df,'Area Under ROC Curve')