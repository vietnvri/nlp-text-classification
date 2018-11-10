import glob
from pyvi import ViTokenizer, ViPosTagger
import _pickle as pkl 
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
		paths = glob.glob(folder+'/*')
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

	return({"data": data, "labels:": labels})

# format data {data: [[items]], labels: [label]}
data_l_train = preprocess("../data/*")
# data_test = preprocess("../test/*")

def clean_stop_words(path, data_l):
	stopwords = []
	with open(path) as f:
		stopwords.append(f.readline())

	for batch in data_l["data"]:
		for item in batch:
			for stop in stopwords:
				item.replace(stop, "")

clean_stop_words("./stopword/stopwords.txt", data_l=data_l_train)

# return matrix [[dim of each item] * item]
# def word_to_vec(data):
