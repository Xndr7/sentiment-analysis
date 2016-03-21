#import modules needed
import random
import pickle
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

#class to classify and determine the confidence of the system by counting the majority decision of the 3 algorithms
class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf                                                      #return confidence of the system


documents_f = open("pickled_algos/documents.pickle", "rb")
documents = pickle.load(documents_f)                                     #load pickle of all the doucments
documents_f.close()


word_features5k_f = open("pickled_algos/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)                           #load word featureset
word_features5k_f.close()


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

featuresets_f = open("pickled_algos/word_features5k.pickle", "rb")
featuresets = pickle.load(featuresets_f)                                 #load featuresets
featuresets_f.close()

random.shuffle(featuresets)
print(len(featuresets))

testing_set = featuresets[5000:]                                         #load testing set
training_set = featuresets[:5000]                                        #load training set

open_file = open("pickled_algos/originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(open_file)                                      #load pickle of naive bayes algorithm
open_file.close()


open_file = open("pickled_algos/MNB_classifier5k.pickle", "rb")
MNB_classifier = pickle.load(open_file)                                  #load pickle of MNB classifier
open_file.close()


open_file = open("pickled_algos/BernoulliNB_classifier5k.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)                          #load pickle of BernoulliNB classifier
open_file.close()


open_file = open("pickled_algos/SGDC_classifier5k.pickle", "rb")
SGDC_classifier = pickle.load(open_file)                                 #load SGDC classifier pickle
open_file.close()

voted_classifier = VoteClassifier(
                                  classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  SGDC_classifier)                       #load all classifiers into the Voteclassifier to determine sentiment


def sentiment(text):
    feats = find_features(text)

    return voted_classifier.classify(feats), voted_classifier.confidence(feats) #return sentiment and confidence value <=1


