# -*- coding: utf-8 -*-
"""coursework_data_import.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/github/cbannard/lela60331_24-25/blob/main/coursework/coursework_data_import.ipynb
"""

!wget https://raw.githubusercontent.com/cbannard/lela60331_24-25/refs/heads/main/coursework/Compiled_Reviews.txt

reviews=[]
sentiment_ratings=[]
product_types=[]
helpfulness_ratings=[]

with open("Compiled_Reviews.txt") as f:
   for line in f.readlines()[1:]:
        fields = line.rstrip().split('\t')
        reviews.append(fields[0])
        sentiment_ratings.append(fields[1])
        product_types.append(fields[2])
        helpfulness_ratings.append(fields[3])

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import re

#split the reviews
token_def = re.compile("[^ ]+")
# Tokenise the text, turning a list of strings into a list of tokens.
tokenized_sents = [token_def.findall(txt) for txt in reviews]
# Collapse all tokens into a single list
tokens=[]
for s in tokenized_sents:
      tokens.extend(s)
# Count the tokens in the tokens list.
counts=Counter(tokens)
# Sort the tuples.
so=sorted(counts.items(), key=lambda item: item[1], reverse=True)
# Extract the list of tokens
so=list(zip(*so))[0]
# Select the firs 5000 words in the list
type_list=so[0:5000]

# Create a 36547 x 5000 matrix of zeros
M = np.zeros((len(reviews), len(type_list)))
#iterate over the reviews
for i, rev in enumerate(reviews):
    # Tokenise the current review:
    tokens = token_def.findall(rev)
    # iterate over the words in our type list (the set of 5000 words):
    for j,t in enumerate(type_list):
        # if the current word j occurs in the current review i then set the matrix element at i,j to be one. Otherwise leave as zero.
        if t in tokens:
              M[i,j] = 1

# Select 80% of the indices randomly for training set and the remaining 20% of the indices are used for the test set
train_ints=np.random.choice(len(reviews),int(len(reviews)*0.8),replace=False)
test_ints=list(set(range(0,len(reviews))) - set(train_ints))

# Create the training and test feature matrixes
M_train = M[train_ints,]
M_test = M[test_ints,]

#Create the training and test sentiment ratings sets
sentiment_ratings_train = [sentiment_ratings[i] for i in train_ints]
sentiment_ratings_test = [sentiment_ratings[i] for i in test_ints]

import math

# Number of features (5000 most frequent words)
num_features=5000

# Convert sentiment labels into binary values: 1 for "positive", 0 for others
y=[int(l == "positive") for l in sentiment_ratings_train]

# Initialize weights and bias randomly
weights = np.random.rand(num_features)
bias=np.random.rand(1)

# Set the number of iterations and the learning rate for gradient descent
n_iters = 1000
lr=0.4

# List to store the logistic loss values for each iteration
logistic_loss=[]

# Get the number of samples (reviews)
num_samples=len(y)

# training the logistic regression model
for i in range(n_iters):
  z = M_train.dot(weights)+bias
  q = 1/(1+np.exp(-z))
  eps=0.00001
  loss = -sum((y*np.log2(q+eps)+(np.ones(len(y))-y)*np.log2(np.ones(len(y))-q+eps)))
  logistic_loss.append(loss)
  y_pred=[int(ql > 0.5) for ql in q]

  dw = (q-y).dot(M_train)/num_samples
  db = sum((q-y))/num_samples
  weights = weights - lr*dw
  bias = bias - lr*db

# Plot the logistic loss over the number of iterations to visualize convergence
plt.plot(range(1,n_iters),logistic_loss[1:])
plt.xlabel("number of epochs")
plt.ylabel("loss")
#loss = sum(-(np.ones(len(y))*np.log2(q)+(np.ones(len(y))-y)*np.log2(np.ones(len(y))-q)))

z = M_test.dot(weights)+bias
q = 1/(1+np.exp(-z))
# set the decision boundary
y_test_pred=[int(ql > 0.5) for ql in q]

#calculate the accuracy
y_test=[int(l == "positive") for l in sentiment_ratings_test]
acc_test=[int(yp == y_test[s]) for s,yp in enumerate(y_test_pred)]
print(sum(acc_test)/len(acc_test))

labels_test_pred=["positive" if s == 1 else "negative" for s in y_test_pred]

#calculate the precision and recall

labels_test_pred=["positive" if s == 1 else "negative" for s in y_test_pred]

true_positives=sum([int(yp == "positive" and sentiment_ratings_test[s] == "positive") for s,yp in enumerate(labels_test_pred)])
false_positives=sum([int(yp == "positive" and sentiment_ratings_test[s] == "negative") for s,yp in enumerate(labels_test_pred)])
false_negatives=sum([int(yp == "negative" and sentiment_ratings_test[s] == "positive") for s,yp in enumerate(labels_test_pred)])
precision=true_positives/(true_positives+false_positives)
recall=true_positives/(true_positives+false_negatives)
print(precision)
print(recall)

# print the weights and corresponding features
feature_weights = list(zip(type_list, weights))
positive_features = [fw for fw in feature_weights if fw[1] > 0]
negative_features = [fw for fw in feature_weights if fw[1] < 0]


positive_features_sorted = sorted(positive_features, key=lambda x: abs(x[1]), reverse=True)
negative_features_sorted = sorted(negative_features, key=lambda x: abs(x[1]), reverse=True)

# Print the top 50 positive features and their weights
print("Top 50 Positive Features:")
for feature, weight in positive_features_sorted[:50]:
    print(f"{feature}: {weight}")

# Print the top 50 negative features and their weights
print("\nTop 50 Negative Features:")
for feature, weight in negative_features_sorted[:50]:
    print(f"{feature}: {weight}")