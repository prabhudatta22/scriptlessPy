import nltk
import pandas as pd
import os
import pickle
import re
from openpyxl import load_workbook
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
home = str(os.getcwd())
print(home)
sheet = pd.read_excel('C:/Users/Prabhudatta.C/Desktop/newToolSite/src/test/resources/TestCases.xlsx', 'TestCaseSheet')

sentence = pd.Series.copy(sheet['StepName'])

# ingesting data and removing extra lines
sentence = pd.DataFrame(sentence)
sentence.columns = ['Test Step Description']
sentence = sentence.replace('\n', '', regex=True)
sentence = sentence.replace('\r', '', regex=True)

# changing all sentences to lowercase
sentence['Test Step Description'] = sentence['Test Step Description'].str.lower()

# Removing 'out' from stop-words list
stopwords_list = stopwords.words('english')
stopwords_list.remove('out')

# filtering descriptions to a maximum of 3 key words
sentence['tokenized_sents'] = sentence.apply(lambda row: re.sub('[^A-Za-z0-9 :.]+', '', row['Test Step Description']), axis = 1)
sentence['tokenized_sents'] = sentence.apply(lambda row: nltk.word_tokenize(row['tokenized_sents']), axis = 1)
sentence['tokenized_sents'] = sentence.apply(lambda row: [word for word in row['tokenized_sents'] if not word in stopwords_list], axis = 1)
sentence['tokenized_sents'] = sentence.apply(lambda row: nltk.pos_tag(row['tokenized_sents']), axis = 1)
sentence['tokenized_sents'] = sentence.apply(lambda row: [word for word, tag in row['tokenized_sents'] if('NN' in tag or 'VB' in tag or 'RB' in tag or 'RP' in tag)], axis = 1)
sentence['tokenized_sents'] = sentence.apply(lambda row: row['tokenized_sents'][0:5], axis = 1)
sentence.apply(lambda row: row['tokenized_sents'].extend([''] * (5-len(row['tokenized_sents']))), axis = 1)

# giving each key word its own column
porter = PorterStemmer()

sentence['tok1'] = sentence.apply(lambda row: porter.stem(row['tokenized_sents'][0]), axis = 1)
sentence['tok2'] = sentence.apply(lambda row: porter.stem(row['tokenized_sents'][1]), axis = 1)
sentence['tok3'] = sentence.apply(lambda row: porter.stem(row['tokenized_sents'][2]), axis = 1)
sentence['tok4'] = sentence.apply(lambda row: porter.stem(row['tokenized_sents'][3]), axis = 1)
sentence['tok5'] = sentence.apply(lambda row: porter.stem(row['tokenized_sents'][4]), axis = 1)

# keeping only relevant columns
sentence = sentence[['tok1', 'tok2', 'tok3', 'tok4', 'tok5']]

# predicting "NLP Categories"
document1 = sentence[['tok1', 'tok2', 'tok3', 'tok4', 'tok5']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# Import TfIdfVectorizer for Categories
tfidfconverter1 = pickle.load(open(home+'/Categories_Tfidf_Vectorizer.pkl', 'rb'))

# Transform document1 using the TfIdfVectorizer for Categories
X_category = tfidfconverter1.transform(document1).toarray()

# Load Trained Model for Categories
categories_model = pickle.load(open(home+'/Categories_Model.pkl', 'rb'))

# Predict Category
predicted_category = categories_model.predict(X_category)

# predicting "NLP Method"
sentence['NLP_Categories_pred'] = predicted_category
document2 = sentence[['tok1', 'tok2', 'tok3', 'tok4', 'tok5', 'NLP_Categories_pred']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# Import TfIdfVectorizer for Methods
tfidfconverter2 = pickle.load(open(home+'/Methods_Tfidf_Vectorizer.pkl', 'rb'))

# Transform document2 using the TfIdfVectorizer for Methods
X_method = tfidfconverter2.transform(document2).toarray()

# Load Trained Model for Methods
methods_model = pickle.load(open(home+'/Methods_Model.pkl', 'rb'))

# Predict Method
predicted_method = methods_model.predict(X_method)    

# Print the Predicted Method and Category
sheet['ActionType'] = predicted_method

excelBook = load_workbook('C:/Users/Prabhudatta.C/Desktop/newToolSite/src/test/resources/TestCases.xlsx')
with pd.ExcelWriter('C:/Users/Prabhudatta.C/Desktop/newToolSite/src/test/resources/TestCases.xlsx', engine='openpyxl') as writer:
    # Save your file workbook as base
    writer.book = excelBook
    writer.sheets = dict((ws.title, ws) for ws in excelBook.worksheets)

    # Now here add your new sheets
    sheet.to_excel(writer, sheet_name='TestCaseSheet', index=False)

    # Save the file
    writer.save()
    writer.close()