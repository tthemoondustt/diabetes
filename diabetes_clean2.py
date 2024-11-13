# -*- coding: utf-8 -*-
"""diabetes-clean2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fJF4xvjs5fpViD9HUrczU2OaiF0Riw2L

# A. Persiapan Data
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import graphviz
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, roc_auc_score

"""## 2. *Load* Dataset"""

from google.colab import drive
drive.mount('/content/drive')

dataset = pd.read_csv('./drive/MyDrive/dataset/pima - clean - eng.csv')

dataset

from google.colab import files
uploaded = files.upload()

import pandas as pd

# Mengakses file yang diunggah
dataset = pd.read_csv('/content/1-0-1-0 - acak.csv')
print(dataset.head())

"""## 3. Distribusi Dataset

### a. Deskriptif Statistik
"""

dataset.describe()

dataset.describe(include='object')

"""### b. Distribusi Kelas Dataset"""

fig, ax = plt.subplots()
Kelas = dataset.groupby('Kelas').size()

sns.set()
Kelas.plot(kind='pie', colors=['tomato','gold'], labeldistance=None,
               figsize=[5,5], textprops={'fontsize': 10},
              autopct=lambda p: '{:.2f}%({:.0f})'.format(p,(p/100)*Kelas.sum()))
ax.legend(dataset['Kelas'],  fontsize='large', loc='upper right',frameon=False)
# ax.legend(['Diabetes','Tidak Diabetes'],  fontsize='large', loc='upper right',frameon=False)

"""### c. Distribusi Atribut Numerik"""

sns.set_style('whitegrid')
fig, axs = plt.subplots(3, 3, figsize=(18, 16))

sns.histplot(data=dataset,x="Kehamilan", hue="Kelas", palette=["tomato",'gold'], ax=axs[0,0], kde=True)
sns.histplot(data=dataset,x="Glukosa", hue="Kelas", palette=["tomato",'gold'], ax=axs[0,1], kde=True, )
sns.histplot(data=dataset,x="Tekanan Darah", hue="Kelas", palette=["tomato",'gold'], ax=axs[0,2], kde=True)
sns.histplot(data=dataset,x="Ketebalan Kulit", hue="Kelas", palette=["tomato",'gold'], ax=axs[1,0], kde=True)
sns.histplot(data=dataset,x="Insulin", hue="Kelas", palette=["tomato",'gold'], ax=axs[1,1], kde=True)
sns.histplot(data=dataset,x="BMI", hue="Kelas", palette=["tomato",'gold'], ax=axs[1,2], kde=True)
sns.histplot(data=dataset,x="Umur", hue="Kelas", palette=["tomato",'gold'], ax=axs[2,1], kde=True)

"""### d. Distribusi Atribut Kategorik"""

feat = 'Kelas'
hue = 'Gender'
hue_type = dataset[hue].dtype.type

groups = dataset[feat].unique()
proportions = dataset.groupby(feat)[hue].value_counts(normalize=True)

ax = sns.countplot(x=feat, hue=hue, data=dataset, palette=["tomato",'gold'])

for c in ax.containers:
    labels = [f'{proportions.loc[g, hue_type(c.get_label())]:.1%}' for g in groups]
    ax.bar_label(c, labels)


plt.legend(loc='upper center')

feat = 'Kelas'
hue = 'Riwayat Keluarga'
hue_type = dataset[hue].dtype.type

groups = dataset[feat].unique()
proportions = dataset.groupby(feat)[hue].value_counts(normalize=True)

ax = sns.countplot(x=feat, hue=hue, data=dataset, palette=["tomato",'gold'])

for c in ax.containers:
    labels = [f'{proportions.loc[g, hue_type(c.get_label())]:.1%}' for g in groups]
    ax.bar_label(c, labels)

plt.legend(loc='center right')

"""### e. *Encoding*"""

from sklearn.preprocessing import OneHotEncoder

one_hot_encoder = OneHotEncoder(sparse_output=False)

dataset[['Laki-Laki','Perempuan']] = one_hot_encoder.fit_transform(dataset['Gender'].values.reshape(-1,1))
dataset[['Ada Riwayat','Tidak Ada Riwayat']] = one_hot_encoder.fit_transform(dataset['Riwayat Keluarga'].values.reshape(-1,1))
# dataset[['Tidak Ada Riwayat','Ada Riwayat']] = one_hot_encoder.fit_transform(dataset['Riwayat Keluarga'].values.reshape(-1,1))


dataset

"""### f. Pemisahan Atribut Input dan Output"""

# atr_dataset = dataset.drop(columns = ['Kelas','Gender','Riwayat Keluarga'])
# cls_dataset = dataset['Kelas']

atr_dataset = dataset.drop(columns = ['Kelas'])
cls_dataset = dataset['Kelas']

"""# B. *Modelling*

## 1. Pemisahan Data *Training* dan Data *Testing*
"""

xtrain, xtest, ytrain, ytest = train_test_split(atr_dataset, cls_dataset,
                                                train_size = 0.8, random_state=1)
tree_dataset = DecisionTreeClassifier(criterion='entropy',random_state=17)
tree_dataset.fit(xtrain, ytrain)
# print(ytrain.to_string())
xtrain

"""## 3. Menampilkan *Decision Tree*"""

# export_graphviz(tree_dataset, out_file = "Tree_Outcome.dot",
#                 feature_names=atr_dataset.columns, impurity=True, filled=True,class_names=cls_dataset, precision=5)

# with open("Tree_Outcome.dot") as fig:
#   dot_graph = fig.read()
#   graph = graphviz.Source(dot_graph)
# graph.view()
# graph

# pima
from sklearn.tree import export_graphviz
from io import StringIO
from IPython.display import Image
import pydotplus
dot_data = StringIO()
export_graphviz(tree_dataset, out_file=dot_data,
                filled=True, rounded=True,
                special_characters=True,feature_names = atr_dataset.columns,class_names=['Tidak Diabetes','Diabetes'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_png('diabetes.png')
Image(graph.create_png())

"""# C. Evaluasi Kinerja Model

## 1. Pembentukan *Confusion Matrix*
"""

fig, axs = plt.subplots(1, 2, figsize=(11, 3))

y_pred = tree_dataset.predict(xtest)

cm_test = confusion_matrix(ytest, y_pred,labels=tree_dataset.classes_)
cm_training = confusion_matrix(ytrain, tree_dataset.predict(xtrain), labels=tree_dataset.classes_)

disp_test = ConfusionMatrixDisplay(confusion_matrix=cm_test, display_labels=tree_dataset.classes_)
disp_training = ConfusionMatrixDisplay(confusion_matrix=cm_training, display_labels=tree_dataset.classes_)

disp_test.plot(ax=axs[0])
disp_training.plot(ax=axs[1])

ax=axs[0].set(title='Confusion Matrix Testing Data')
ax=axs[1].set(title='Confusion Matrix Training Data')

"""## 2. Menampilkan Nilai Akurasi, Presisi, *Recall*, dan f-1 score

### a. Data *Testing*
"""

test_accuracy = accuracy_score(ytest, y_pred)
print("Accuracy Data Testing : %d persen" % (test_accuracy*100))

test_precision = precision_score(ytest, y_pred)
print("Precision Data Testing : %d persen" % (test_precision*100))

test_recall = recall_score(ytest, y_pred)
print("Recall Data Testing: %d persen" % (test_recall*100))

test_f1 = f1_score(ytest, y_pred)
print("F-1 Score Data Testing : %d persen" % (test_f1*100))

"""### b. Data *Training*"""

train_accuracy = accuracy_score(ytrain, tree_dataset.predict(xtrain))
print("Accuracy Data Training: %d persen" % (train_accuracy*100))

train_precision = precision_score(ytrain, tree_dataset.predict(xtrain))
print("Precision Data Training: %d persen" % (train_precision*100))

train_recall = recall_score(ytrain, tree_dataset.predict(xtrain))
print("Recall Data Training: %d persen" % (train_recall*100))

train_f1 = f1_score(ytrain, tree_dataset.predict(xtrain))
print("F-1 Score Data Training: %d persen" % (train_f1*100))

"""## 3. Pembentukan Kurva ROC dan AUC"""

from sklearn.metrics import roc_curve, roc_auc_score

y_pred_proba_test = tree_dataset.predict_proba(xtest)[:,1]
y_pred_proba_train = tree_dataset.predict_proba(xtrain)[:,1]

fpr_test, tpr_test, _ = roc_curve(ytest, y_pred_proba_test)
fpr_train, tpr_train, _ =roc_curve(ytrain, y_pred_proba_train)

plt.plot(fpr_test,tpr_test, color="red", label="Kurva ROC Data Testing", marker='.', linestyle='--')
plt.plot(fpr_train,tpr_train, color="green", label="Kurva ROC Data Training", marker='.', linestyle='--')
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')

auc_test = roc_auc_score(ytest, y_pred_proba_test)
auc_train = roc_auc_score(ytrain, y_pred_proba_train)

y_zeros = [0 for _ in tpr_test]
plt.fill_between(fpr_test, y_zeros, tpr_test, alpha=0.3, label='AUC Data Testing : %.3f' % (auc_test), color="tomato")
plt.fill_between(fpr_train, y_zeros, tpr_train, alpha=0.3,label='AUC Data Training : %.3f' % (auc_train), color="green")

plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.legend(loc=4)
plt.show()

!apt-get install git

!git config --global user.name "tthemoondustt"
!git config --global user.email "dyahkinkinnn@gmail.com"

!git clone https://github.com/tthemoondustt/diabetes.git

!ls /content/
# !ls /content/diabetes

!cp /content/diabetes-clean2.ipynb /content/diabetes/

# Commented out IPython magic to ensure Python compatibility.
# Pindah ke folder repository
# %cd /content/repository

# Menambahkan file ke staging area
!git add my_script.py

# Melakukan commit
!git commit -m "Menambahkan file Python dari Google Colab"

# Melakukan push ke GitHub
!git push https://github.com/username/repository.git main
