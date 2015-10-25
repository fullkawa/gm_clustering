# -*- coding: utf-8 -*-

from lxml import html
import requests

import os.path as path

import pandas as pd

boothlistcsv = '../data/boothlist.csv'

page = requests.get('http://gamemarket.jp/boothlist/')
boothinfobase = 'http://gamemarket.jp/booth/gm'


# GET BOOTH LIST

if not path.exists(boothlistcsv) :
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

    except NameError:
      print

  df = pd.DataFrame(boothlist)
  df.to_csv(boothlistcsv, encoding='utf-8', header=None)
  print 'boothlist >', boothlistcsv

print 'done'
