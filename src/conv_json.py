# -*- coding: utf-8 -*-

import codecs
import json
import pandas as pd

csvlist = ['../data/game_450clustered.csv',
           '../data/game_150clustered.csv',
           '../data/game_50clustered.csv']

for csv in csvlist:
  gamelist = pd.read_csv(csv, encoding='utf-8', header=None)

  data = []
  prevclnumber = -1
  for index, game in gamelist.iterrows() :
    clustertop = (prevclnumber != game[14])
    record = {'boothNo':  game[2],
              'boothName':  game[3],
              'gameInfoUrl':  game[4],
              'gameTitle':    game[5],
              'designerName': game[6],
              'illustratorName':  game[7],
              'numberOfPlayers':  game[8],
              'playingTime':    game[9],
              'suggestedAges':  game[10],
              'price':      game[11],
              'published':  game[12],
              'index':      game[13],
              'clusterNo':  game[14],
              'clusterTop': clustertop}
    data.append(record)
    prevclnumber = game[14]

  filename = csv.replace('csv', 'json')
  f = codecs.open(filename, 'w', 'utf-8')
  dumped = json.dumps(data, ensure_ascii=False)
  dumped = dumped.replace('NaN', '""')
  f.write(dumped)
  f.close()
  print ' converted ', csv
