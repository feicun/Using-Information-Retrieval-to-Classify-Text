import cPickle as pickle
import string
import os
import re
from nltk.corpus import stopwords
import math
import heapq
from fractions import Fraction

class article:
    ### category string
    ###raw string
    ###TFDcit dict
    def __init__(self, category, raw, TFDict) :
        self.category = category
        self.raw = raw
        self.TFDict = TFDict

    def computeTFIDF(self) :
        TF = {}
        IDF = {}
        IDF, TF = computeDocumentFrequency(self.category)

        newRaw = re.findall('\w+', self.raw)
        for word in newRaw :
            newWord = word
            newWord = newWord.strip(string.punctuation)
            newWord = newWord.lower()

            if newWord not in stopwords.words('english'):
                TFIDFValue = TF.get(newWord) * IDF.get(newWord)
                self.TFDict.update({newWord: TFIDFValue})

        return self.TFDict



def computeDocumentFrequency(path) :
    TF = {} ### How frequency of a word occured in a query
    DF = {} ### How many files contains the word

    listing = os.listdir(path)
    Corpus = len(listing) ## D
    if not Corpus:
            return 0.0
    ### infile is an article file in the newsgroup category
    for infile in listing:
        f = open(path + '/' + infile)
        while 1:
            lines = f.readlines(100000)
            if not lines:
                break
            for line in lines:
                line = re.findall('\w+', line)
                
                ## Check whether the word occured in the file
                ## If yes, don not update DF
                tempDict = {} 

                for word in line:
                    newWord = word
                    newWord = newWord.strip(string.punctuation)
                    newWord = newWord.lower()

                    if newWord not in stopwords.words('english'):
                        if newWord in TF.viewkeys():
                            TF.update({newWord: TF.get(newWord) + 1})
                        else :
                            TF.update({newWord: 1})
                        ##update DF
                        if newWord not in tempDict.viewkeys() :
                            if newWord in DF.viewkeys() :
                                DF.update({newWord: DF.get(newWord) + 1})
                            else :
                                DF.update({newWord: 1})

                            tempDict.update({newWord: True})

    ### update DF value to IDF
    for element in DF.viewkeys() :
        value = DF.get(element)
        newValue = math.log(Fraction(Corpus) / (Fraction(value)+1))
        DF.update({element: newValue})

    ### DF now is the IDF dict
    ### TF is the TF dict
    return DF, TF



def computeTFIDFCategory(directory) :
    TF = {}
    IDF = {}
    TFIDF = {}
    TopKeys = {}
    IDF, TF = computeDocumentFrequency(directory)

    for word in IDF.viewkeys() :
        TFIDFValue = TF.get(word) * IDF.get(word)
        TFIDF.update({word: TFIDFValue})

    thousand_keys_sorted_by_values = heapq.nlargest(1000, TFIDF, key=TFIDF.get)

    for key in thousand_keys_sorted_by_values :
        TopKeys.update({key: TFIDF.get(key)})
    
    category = directory.split('/')[-1]
    pickle.dump(TopKeys, open(category, 'wb'))
    return TopKeys



def cosineSimilarity(dict1, dict2) :
    vec1 = []
    vec2 = []
    allWords = set(dict1.viewkeys()) & set(dict2.viewkeys())
    for word in allWords:
        if dict1.get(word) is None :
            vec1.append(0)
        else :
            vec1.append(dict1.get(word))
        if dict2.get(word) is None :
            vec2.append(0)
        else :
            vec2.append(dict2.get(word))

    numerator = 0
    for index in range(len(vec1)) :
        numerator = numerator + vec1[index] * vec2[index]

    sum1 = 0
    sum2 = 0
    for index in range(len(vec1)) :
        sum1 = sum1 + vec1[index] * vec1[index]
        sum2 = sum2 + vec2[index] * vec2[index]
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
       return 0.0
    else:
       return float(numerator) / denominator


### This function will write the category TFIDF dict to pickle file
### All the pickle files MUST put in a directory named "TFIDFCategoryFiles"
def generateTFIDFCategoryFiles() :
    path = 'C:/Users/feicun/hw5/20_newsgroups'
    newsgroups = os.listdir(path)

    for Dir in newsgroups :
        newsgroup_path = path + '/' + Dir
        computeTFIDFCategory(newsgroup_path)



def classify(Article) :
    biggest_cosine = 0
    newsgroup_path = ''
    most_similiar_newsgroup = ''

    path = 'C:/Users/feicun/hw5/TFIDFCategoryFiles'
    TFIDFCategoryFiles = os.listdir(path)
    TFDict = Article.computeTFIDF()
    for File in TFIDFCategoryFiles :
        consine = cosineSimilarity(TFDict, pickle.load(open(path + '/' + str(File),'rb')))
        print 'Cosine Similarity with ' + str(File) + 'is: ' + str(consine)
        if consine >= biggest_cosine :
            biggest_cosine = consine
            most_similiar_newsgroup = File

    print 'The most similiar newsgroup is: ' + str(most_similiar_newsgroup)
    print 'The biggest cosine is: ' + str(biggest_cosine)
    print '------------------------------------'



def hCluster() :
    S = {}
    path = 'C:/Users/feicun/hw5/TFIDFCategoryFiles'
    TFIDFCategoryFiles = os.listdir(path)
    for File in TFIDFCategoryFiles :
        TFIDFCategoryDict = pickle.load(open(path + '/' + str(File),'rb'))
        S.update({str(File): TFIDFCategoryDict})

    nextLevelDict = {}
    while (len(S) > 1):

        while (len(S) > 1) :
            currentKey = list(S.viewkeys())[0]
            currentCosine = 0
            pairKey = ''

            for key, value in S.iteritems():
                if key is not currentKey :
                    newCosine = cosineSimilarity(S.get(currentKey), value)
                    if newCosine > currentCosine :
                        currentCosine = newCosine
                        pairKey = key

            mergedKey = "{" + str(currentKey) + "U" + str(pairKey) + "}"
            nextLevelDict.update( { mergedKey : dictMerge(S.get(currentKey), S.get(pairKey) ) } )
            del S[currentKey]
            del S[pairKey]

        S = nextLevelDict

    print list(S.viewkeys())[0]



from collections import defaultdict
def dictMerge(dict1, dict2):
    newDict = defaultdict(int, dict1)
    for m, n in dict2.items():
        newDict[m] += n

    return dict(newDict)




if __name__ == '__main__' :

    ### Call hCluster() function
    #hCluster()


    ### Call generateTFIDFCategoryFiles() function
    generateTFIDFCategoryFiles()