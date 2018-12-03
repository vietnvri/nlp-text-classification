import numpy as np 
import ast

data = ['test', 'val', 'train']

for type_set in data:
    with open('./data/after_lda_{}.csv'.format(type_set), 'r') as f:
        lines = f.readlines()
        X = []
        Y = []
        for line in lines:
            x = ast.literal_eval(line[1:-4])
            y = line[-2]
            X.append(x)
            Y.append(y)
        X = np.array(X).astype(np.float64)
        Y = np.array(Y).reshape(-1,1).astype(np.float64)
        np.save('./data/{}_{}.npy'.format(type_set, X.shape[1]), np.hstack([X, Y]))
