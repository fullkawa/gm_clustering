# -*- coding: utf-8 -*-

import MeCab

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans

MAX_DF = 0.8
MAX_FEATURES = 6000
NUM_CLUSTERS = 20

gamedatacsv  = '../data/gamedata.csv'

gamelist = pd.read_csv(gamedatacsv, encoding='utf-8', header=None)
descs = gamelist[12]

def analyzer(text):
    ret = []
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(text.encode('utf-8'))
    while node:
        ret.append(node.feature.split(',')[-3].decode('utf-8'))
        node = node.next
    return ret

vectorizer = TfidfVectorizer(analyzer=analyzer,
                            max_df=MAX_DF,
                            max_features=MAX_FEATURES)
X = vectorizer.fit_transform(descs)
print 'Done: vectorizer.fit, transform'

km = MiniBatchKMeans(n_clusters=NUM_CLUSTERS,
                     init='k-means++',
                     batch_size=1000,
                     n_init=10,
                     max_no_improvement=10)
X = km.fit_predict(X)
print 'Done: km.fit, predict'

gamelist[13] = km.labels_
sortedlist = gamelist.sort(13)
sortedlist.to_csv('../data/game_clustered.csv', encoding='utf-8', header=None)
