import glob

import gensim
from gensim import corpora, models
from pyvi import ViTokenizer, ViPosTagger
import _pickle as pkl
import numpy as np


# print(ViPosTagger.postagging("Tôi tên là Nguyễn Văn Viết, sinh viên trường Đại học Bách Khoa Hà Nội"))

# with open('./data.pkl', 'wb') as f:
# 	pkl.dump({'data': data, 'label': labels}, f)

def preprocess(path):
    folders = glob.glob(path)
    labels = []
    data = []

    fError = open("./error.txt", 'a')

    for folder in folders:
        labels.append(folder.split('/')[-1])
        paths = glob.glob(folder + '/*')
        sub = []
        for path in paths:
            with open(path, 'r') as f:
                content = f.read()
                if "</" in content or "/>" in content:
                    fError.write(path + "\n")

                else:
                    sub.append(content)
        data.append(sub)
    fError.close()

    data_tok = []
    for batch in data:
        sub = []
        for item in batch:
            sub.append(ViTokenizer.tokenize(item))
        data_tok.append(sub)

    return {"data": data_tok, "labels:": labels}


# # format data {data: [[items]], labels: [label]}
# data_l_train = preprocess("../data/*")
#
#
# # data_test = preprocess("../test/*")
#
#
# def clean_stop_words(path, data_l):
#     stopwords = []
#     with open(path) as f:
#         stopwords.append(f.readline())
#
#     for batch in data_l["data"]:
#         for item in batch:
#             for stop in stopwords:
#                 item.replace(stop + " ", "")
#
#
# clean_stop_words("./stopword/stopwords.txt", data_l=data_l_train)
#
# with open("./tempdata.kpl", "wb") as f:
#     pkl.dump(data_l_train, f)

with open("./tempdata.kpl", "rb") as f:
    data_l_train = pkl.load(f)

all_item = []
for batch in data_l_train["data"]:
    for item in batch:
        all_item.append(item.split(" "))

all_item = np.array(all_item)

dictionary = gensim.corpora.Dictionary(all_item)
dictionary.filter_extremes(no_below=10, no_above=0.5, keep_n=100000)

bow_corpus = [dictionary.doc2bow(item) for item in all_item]
tfidf = models.TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]


lda_model = gensim.models.LdaMulticore(corpus_tfidf, num_topics=20, id2word=dictionary, passes=2, workers=8)

final_data = []

# for _, score in sorted(lda_model[tfidf])
