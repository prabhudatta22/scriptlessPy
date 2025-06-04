from pandas import read_excel
import nltk
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
home = str(os.getcwd())
print('***********************************')
print(home)
print('***********************************')
seed = 211

# ingesting data and removing extra lines
data = read_excel("./inputdata/sentences_final.xlsx", encoding = "cp1252")
data = data.replace('\n', '', regex=True)
data = data.replace('\r', '', regex=True)

# changing all sentences to lowercase
data['Test Step Description'] = data['Test Step Description'].str.lower()

# Methods are camel-cased
data['NLP Method'] = data['NLP Method'].str[0].str.lower() + data['NLP Method'].str[1:]

# changing all categories to lowercase
data['NLP Categories'] = data['NLP Categories'].str.lower()

# removing Test Step Descriptions that correspond to more than one method (impossible to classify)
imp_counts = data[['NLP Method', 'Test Step Description']].groupby('Test Step Description').nunique()
imp_counts = imp_counts[imp_counts['NLP Method'] > 1]
imp_descs = imp_counts['Test Step Description'].index.values

for i in range(len(data)):
    if data['Test Step Description'][i] in imp_descs:
        data = data.drop(i)
        
# Removing 'out' from stop-words list
stopwords_list = stopwords.words('english')
stopwords_list.remove('out')

# tokenizing sentences
data['tokenized_sents'] = data.apply(lambda row: re.sub('[^A-Za-z0-9 :.]+', '', row['Test Step Description']), axis = 1)
data['tokenized_sents'] = data.apply(lambda row: nltk.word_tokenize(row['tokenized_sents']), axis = 1)
data['tokenized_sents'] = data.apply(lambda row: [word for word in row['tokenized_sents'] if not word in stopwords_list], axis = 1)
data['tokenized_sents'] = data.apply(lambda row: nltk.pos_tag(row['tokenized_sents']), axis = 1)
data['tokenized_sents'] = data.apply(lambda row: [word for word, tag in row['tokenized_sents'] if('NN' in tag or 'VB' in tag or 'RB' in tag or 'RP' in tag)], axis = 1)
data['tokenized_sents'] = data.apply(lambda row: row['tokenized_sents'][0:5], axis = 1)
data.apply(lambda row: row['tokenized_sents'].extend([''] * (5-len(row['tokenized_sents']))), axis = 1)

# giving each key word its own column and stemming the words
porter = PorterStemmer()

data['tok1'] = data.apply(lambda row: porter.stem(row['tokenized_sents'][0]), axis = 1)
data['tok2'] = data.apply(lambda row: porter.stem(row['tokenized_sents'][1]), axis = 1)
data['tok3'] = data.apply(lambda row: porter.stem(row['tokenized_sents'][2]), axis = 1)
data['tok4'] = data.apply(lambda row: porter.stem(row['tokenized_sents'][3]), axis = 1)
data['tok5'] = data.apply(lambda row: porter.stem(row['tokenized_sents'][4]), axis = 1)

# Save a copy for later
data_test = data.copy(deep=True)

# keeping only relevant columns and dropping rows with null values
data = data[['tok1', 'tok2', 'tok3', 'tok4', 'tok5', 'NLP Method', 'NLP Categories']]
data = data.dropna()

# training a model to predict NLP Categories with 'tok1', 'tok2', 'tok3', 'tok4' and 'tok5'

document1 = data[['tok1', 'tok2', 'tok3', 'tok4', 'tok5']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
tfidfconverter1 = TfidfVectorizer(analyzer='word', stop_words=stopwords_list, ngram_range=(1,3))
X1 = tfidfconverter1.fit_transform(document1).toarray()
y1 = data[['NLP Categories']]

pickle.dump(tfidfconverter1, open(home+'/Categories_Tfidf_Vectorizer.pkl', 'wb'))

CM_classifier1 = LinearSVC()
CM_classifier1.fit(X1, y1)

# Saving the trained model in a pickle file
pickle.dump(CM_classifier1, open(home+'/Categories_Model.pkl', 'wb'))

# training a model to predict NLP Method with 'tok1', 'tok2', 'tok3', 'tok4', 'tok5' and 'NLP Categories'

document2 = data[['tok1', 'tok2', 'tok3', 'tok4', 'tok5', 'NLP Categories']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
tfidfconverter2 = TfidfVectorizer(analyzer='word', stop_words=stopwords_list, ngram_range=(1,3))
X2 = tfidfconverter2.fit_transform(document2).toarray()
y2 = data[['NLP Method']]

pickle.dump(tfidfconverter2, open(home+'/Methods_Tfidf_Vectorizer.pkl', 'wb'))

CM_classifier2 = LinearSVC()
CM_classifier2.fit(X2, y2)

# Saving the trained model in a pickle file
pickle.dump(CM_classifier2, open(home+'/Methods_Model.pkl', 'wb'))