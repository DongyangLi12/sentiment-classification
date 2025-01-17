This project demonstrates how to perform sentiment classification on a collection of reviews using Logistic Regression and One-Hot Encoding. The goal is to classify product reviews as either positive or negative based on their content.

Introduction
Sentiment analysis is a critical task for understanding customer opinions and reviews on products. In this project, I focus on classifying Amazon product reviews as positive or negative using Logistic Regression. The reviews are preprocessed using One-Hot Encoding, where the most frequent words are selected as features.

Installation
To get started, you need to have Python 3.x and the required libraries installed.

Usage
Download this repository to your local machine.
Run the main Python script to train the Logistic Regression model
This will execute the processing, training and evaluation process, outputting the model's evaluation, loss curve over the iterations, and the top 50 positive and negative features and their corresponding weights.

Code Structure
Here’s an overview of the main components of the code:

Data Preprocessing:
Tokenization: Tokenize each review into individual words.
One-Hot Encoding: Transforms the reviews into binary vectors based on the 5000 most frequent words.
Train and test set spliting: Split the dataset into a training set (80%) and a test set (20%).

Logistic Regression Model training: 
The model is initialized with random weights and bias, and trained using stochastic gradient descent. 
The sigmoid function is used to calculate the probabilities of each class. 
The cross-entropy loss function is used to evaluate the model's predictions, with 1000 iterations and a learning rate of 0.4 

Model Evaluation:
The model is evaluated based on its accuracy, precision and recall on a test set.
The weights of the features are analyzed to interpret which words most influence the classification.

Results
After training the logistic regression model, the performance of the model is evaluated. The results show the accuracy, precision and recall of the model on the test set.
