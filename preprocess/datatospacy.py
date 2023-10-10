import spacy
import pandas as pd
from tqdm import tqdm
from spacy.tokens import DocBin


nlp = spacy.load('zh_core_web_sm')
df = pd.read_csv('/home/aurelian/codes/Github/Nijigen_saikou/datasets/simplifyweibo_4_moods.csv',encoding="utf8")
df = df.loc[:,['review','label']]
df['label']= df['label'].astype(str)

from sklearn.utils import shuffle
df = shuffle(df)
data = [tuple(df.iloc[i].values) for i in range(df.shape[0])]
flag = int(df.shape[0]*0.8)
train_data = data[:flag]
valid_data = data[flag:]


def make_docs(data):
    docs = []

    for doc, label in tqdm(nlp.pipe(data, as_tuples=True), total=len(data)):
        if label == '0':
            doc.cats["positive"] = 1
            doc.cats["anger"] = 0
            doc.cats["disgust"] = 0
            doc.cats["down"] = 0
        elif label == '1':
            doc.cats["positive"] = 0
            doc.cats["anger"] = 1
            doc.cats["disgust"] = 0
            doc.cats["down"] = 0
        elif label == '2':
            doc.cats["positive"] = 0
            doc.cats["anger"] = 0
            doc.cats["disgust"] = 1
            doc.cats["down"] = 0
        elif label == '3':
            doc.cats["positive"] = 0
            doc.cats["anger"] = 0
            doc.cats["disgust"] = 0
            doc.cats["down"] = 1

        docs.append(doc)
    return docs

train_docs = make_docs(train_data)
doc_bin = DocBin(docs=train_docs)
doc_bin.to_disk("train.spacy")

valid_docs = make_docs(valid_data)
doc_bin = DocBin(docs=valid_docs)
doc_bin.to_disk("valid.spacy")