import pandas as pd

def datawash(pathtocsv):
    df = pd.read_csv(pathtocsv)
    word = ['[动画表情]','图片']
    words = '|'.join(word)
    df = df[df["Message"].str.contains(words) == False]
    return df


