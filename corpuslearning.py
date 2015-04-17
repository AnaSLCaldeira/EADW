__author__ = 'goncalograzina'

import nltk.data

import os, os.path
path = os.path.expanduser('~/nltk_data')

if not os.path.exists(path):
    os.mkdir(path)

os.path.exists(path)

#nltk.data.load('goncalograzina/PycharmProjects/Projecto/DBpediaEntities-PT-0.1/locations.txt', format='raw')
nltk.data.load('corpora/DBpediaEntities-PT-0.1/locations.txt', format='raw')