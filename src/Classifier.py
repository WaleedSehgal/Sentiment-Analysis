from nltk.corpus import stopwords


class Classifier:
    def __init__(self):
        print 'Init'

    def train(self):
        print 'Training'

    def classify(self):
        print 'Classify'

    # Removes stop words from list of words inputed.
    # Utilizes corpus provided by NLTK
    # Input: List of tuples(List of words, sentiment)
    def remove_stop_words(self, words):
        # Create Set of stop words
        stop_words = set(stopwords.words('english'))

        # Remove stop words from word list
        stripped = [word for word in words if word not in stop_words]

        return stripped

    # Helper method that generates word features based on input
    # Input: List of tuples(List of words, sentiment for these words)
    def __generate_word_features(self, input):
        print

    # Helper method that tokenizes input
    # Input: List of tuples(Tweet message, sentiment)
    def __tokennize_input(self, input):
        print

def main():
    A = ['we', 'must', 'win']
    classifier = Classifier()
    print classifier.remove_stop_words(A)

if __name__ == '__main__':
    main()
