from pyvi import ViTokenizer, ViPosTagger
import _pickle as pk 

# print(ViTokenizer.tokenize(""))
with open('./data.pkl','rb') as f:
	data_l = pk.load(f)
	data = data_l["data"]
	label = data_l["label"]

data_tok = []
for batch in data:
	sub = []
	for item in batch:
		sub.append(ViTokenizer.tokenize(item))
	data_tok.append(sub)

with open("./data_tok.pkl", "wb") as f:
	pk.dump({"data": data_tok, "label": label}, f)
