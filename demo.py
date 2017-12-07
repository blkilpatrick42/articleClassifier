import nltk
from nltk.classify import SklearnClassifier
import pickle


class SKLearnWrapper(SklearnClassifier):
    
    def print_informative_features(self, length=10):
        feature_names = self._vectorizer.get_feature_names()
        top_list = []
        print(''.join([ "{:<20}".format(label) for label in self.labels()]))
        for i, label in enumerate(self.labels()):
            top = np.argsort(self._clf.coef_[i])[-length:]
            top = [feature_names[j] for j in top]
            top_list.append(top)
            #print("%s: %s" % (label, " ".join(feature_names[j] for j in top)))
        for i in range(1, length+1):
            print(''.join(["{:<20}".format(top[-i]) for top in top_list]))

def classify_doc(document):
	word_features = pickle.load(open("Featuresets/word_features.pickle", "rb"))
	classifier = pickle.load(open("Classifiers/sgd_classifier.pickle", "rb"))
	words = nltk.word_tokenize(document)
	features = {}
	for w in word_features:
		features[w] = (w in words)
	print(classifier.classify(features))


filename = input("Enter Filename:")
doc = ""
with open("DemoPages/"+filename, "r") as f:
	for line in f:
		doc += line

classify_doc(doc)
