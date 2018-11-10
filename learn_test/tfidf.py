import _pickle as pk 
from sklearn.feature_extraction.text import TfidfVectorizer
tf = TfidfVectorizer(analyzer='word', min_df = 0)
with open('./data_tok.pkl','rb') as f:
	data_l = pk.load(f)
	data = data_l["data"]
	label = data_l["label"]

all_items = []
for batch in data:
	for item in batch[1:5]:
		all_items.append(item)

tfidf_matrix =  tf.fit_transform(all_items)
feature_names = tf.get_feature_names() 


dense = tfidf_matrix.todense()

episode = dense[0].tolist()[0]
phrase_scores = [pair for pair in zip(range(0, len(episode)), episode) if pair[1] > 0]

# print("%r" % tfidf_matrix)
# print(tfidf_matrix[0])

sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
for phrase, score in [(feature_names[word_id], score) for (word_id, score) in sorted_phrase_scores]:
   print('{0: <20} {1}'.format(phrase, score))