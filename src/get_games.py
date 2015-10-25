# -*- coding: utf-8 -*-

from lxml import html
import requests

import os.path as path

import pandas as pd

boothlistcsv = '../data/boothlist.csv'
gamelistcsv  = '../data/gamelist.csv'
gamedatacsv  = '../data/gamedata.csv'

gamemarketsite = 'http://gamemarket.jp/boothlist/'
boothinfobase = 'http://gamemarket.jp/booth/gm'


# GET BOOTH LIST

if not path.exists(boothlistcsv) :
  print 'Get boothlist...'

  page = requests.get(gamemarketsite)
  contents = html.fromstring(page.text)
  trlist = contents.xpath('//div[@id="tabarea1"]//tr')

  boothlist = []
  for tr in trlist :
    tdlist = tr.xpath('td')
    if (len(tdlist) >= 2) :
      boothno = tdlist[0].text
      if tdlist[1].text is not None :
        boothname = tdlist[1].text.strip()
      else :
        boothname = None
    alist = tr.xpath('td/a')
    if (len(alist) >= 1) :
      if boothname is None :
        boothname = alist[0].text
      boothurl = alist[0].get('href')

    try :
      if boothurl.startswith(boothinfobase) :
        boothlist.append([boothno, boothname.encode('utf-8'), boothurl])
        boothurl = '' # clear

    except NameError:
      print

  df = pd.DataFrame(boothlist)
  df.to_csv(boothlistcsv, encoding='utf-8', header=None)
  print ' boothlist >', boothlistcsv


# GET GAME LIST

if (not path.exists(gamelistcsv)) & path.exists(boothlistcsv) :
  print 'Get gamelist...'

  gamelist = []
  boothlist = pd.read_csv(boothlistcsv, encoding='utf-8', header=None)
  for index, booth in boothlist.iterrows() :
    boothno = booth[1]
    boothname = booth[2]
    boothurl = booth[3]

    page = requests.get(boothurl)
    contents = html.fromstring(page.text)
    gametab = contents.xpath('//div[@id="tabarea2"]')

    if (len(gametab) >= 1) :
      alist = gametab[0].xpath('section/div/h3/a')
      if (len(alist) >= 1) :
        print ' Check', boothurl
        for a in alist :
          gamelist.append([boothno, boothname, a.get('href')])

  df = pd.DataFrame(gamelist)
  df.to_csv(gamelistcsv, encoding='utf-8', header=None)
  print ' gamelist >', gamelistcsv


print 'done'
