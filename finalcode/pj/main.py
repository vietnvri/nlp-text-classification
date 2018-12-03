import numpy as np 
from sklearn.svm import SVC

train_set = np.load('data/train_50.npy')
val_set = np.load('data/val_50.npy')
# test_set = np.load('data/test_100.npy')

X_train = train_set[:, :-1]
Y_train = train_set[:, -1]
X_val = val_set[:, :-1]
Y_val = val_set[:, -1]

clf = SVC(kernel='rbf', degree=3, gamma='auto')
clf.fit(X_train, Y_train)
score = clf.score(X_val, Y_val)
print(score)