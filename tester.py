import tfidf
import sys
import random
import os


if __name__ == '__main__':
    if sys.argv[1] is None :
        print "Please input the number of articles"
    else :
        number = int(sys.argv[1])
        newsgroup_path = ''
        path = 'C:/Users/feicun/hw5/20_newsgroups'
        newsgroups = os.listdir(path)
        ### Pick a random category
        for index in range(number) :
            randomNewsgroup = newsgroups[random.randrange(0, len(newsgroups)-1, 1)]
            newsgroup_path = path + '/' + randomNewsgroup

            ### Pick a random article
            articles = os.listdir(newsgroup_path)
            randomArticle = articles[random.randrange(0, len(articles)-1, 1)]

            with open (newsgroup_path + '/' + randomArticle, "r") as myfile:
                data = myfile.read()

            tempDict = {}
            newArticle = tfidf.article(newsgroup_path, data, tempDict)
            print 'The chosen article is: ' + newsgroup_path + '/' + randomArticle
            tfidf.classify(newArticle)