from nltk.corpus import stopwords
from MessageDAO import MessageDAO
import nltk.classify
import pickle
import re
import itertools
from nltk.stem.snowball import SnowballStemmer
import sys
import enchant
import time
import random

# Set encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')


class Classifier:
    def __init__(self):
        self.training_features = []
        self.testing_features = []
        self.word_features = []
        nltk.download("stopwords")
        nltk.download("wordnet")
        self.classifier = self.get_classifier()

    def classify(self, message):
        # Return if classifier not initialized
        if not self.classifier:
            return

        features = self.__extract_features2(message.split())
        return self.classifier.classify(features)

    def get_classifier(self):
        f = None
        classifier = None
        try:
            f = open('classifier.pickle', 'rb')
            classifier = pickle.load(f)
            f.close()
        except IOError:
            classifier = self.__train()

        return classifier

    def test(self):
        print 'Acquiring testing messages...'

        message_dao = MessageDAO()
        testing_messages = message_dao.retrieve_testing_messages()

        # Pre-process testing messages
        testing_messages = self.__preprocess(testing_messages)[:100]

        print 'Generating test features'

        # Get testing features
        self.word_features = self.__generate_word_features(self.__get_all_words(testing_messages))
        self.testing_features = nltk.classify.apply_features(self.__extract_features, testing_messages)

        print 'Testing...'
        print 'Accuracy:', nltk.classify.util.accuracy(self.classifier, self.testing_features)

    def __train(self):
        start_train_time = time.time()
        start_message_time = time.time()

        print 'Acquiring training messages...'

        # Get training messages
        message_dao = MessageDAO()

        training_messages = message_dao.retrieve_training_messages()
        random.shuffle(training_messages)
        training_messages = training_messages[:5000]
        print len(training_messages), 'received -', time.time() - start_message_time

        start_process_time = time.time()
        print 'Processing messages...'

        # Pre-process training messages
        training_messages = self.__preprocess(training_messages)

        print 'Processing complete - ', time.time() - start_message_time
        print 'Generating training features...'

        # Get training features
        self.word_features = self.__generate_word_features(self.__get_all_words(training_messages))
        self.training_features = nltk.classify.apply_features(self.__extract_features, training_messages)

        print 'Training...'

        classifier = nltk.NaiveBayesClassifier.train(self.training_features)
        print 'Training complete -', time.time() - start_train_time

        classifier.show_most_informative_features(20)

        # Save classifier
        f = open('classifier.pickle', 'wb')
        pickle.dump(classifier, f)
        f.close()

        return classifier

    # Removes stop words from list of words inputed.
    # Utilizes corpus provided by NLTK
    def __remove_stop_words(self, words):
        # Create Set of stop words
        stop_words = set(stopwords.words('english'))

        # Remove stop words from word list
        stripped = [word for word in words if word not in stop_words]

        return stripped

    # Helper method that tokenizes input
    # Input: List of tuples(Tweet message, sentiment)
    def __tokenize_input(self, messages):
        tokenized_messages = []
        for message, sentiment in messages:
            # clean message before tokenizing
            message = self.__clean(message)

            # Transform list to tokenized list and lower case
            words = [word.lower() for word in message.split()]
            tokenized_messages.append((words, sentiment))
        return tokenized_messages

    # Preprocessing method
    def __preprocess(self, messages):
        # Tokenize messages
        processed_messages = self.__tokenize_input(messages)
        return processed_messages

    def __clean(self, message):
        words = []
        snowball_stemmer = SnowballStemmer("english")
        dictionary = enchant.Dict("en_US")

        for word in message.split():
            # Remove white space
            word = word.strip()

            # Remove usernames, urls, numbers and words shorter than 3
            if re.search(r'@\w', word) or re.search(r'http:', word) or re.search(r'\d', word):
                continue

            # Remove special characters
            word = re.sub(r'[/=:.?!\,()#-+$^%;-]*', '', word)

            # Remove repeating characters
            word = ''.join(ch for ch, _ in itertools.groupby(word))

            if len(word) < 3:
                continue

            # Throw out words not in english dictionary
            if not dictionary.check(word):
                continue

            try:
                # Use Snowball Stemmer to stem word
                word = snowball_stemmer.stem(word)
            except UnicodeDecodeError:
                continue

            words.append(word)

        return ' '.join(words)

    def __get_all_words(self, messages):
        all_words = []
        for (words, sentiment) in messages:
            all_words.extend(words)

        return self.__remove_stop_words(all_words)  # remove stop words

    def __generate_word_features(self, words):
        words = nltk.FreqDist(words)
        word_features = words.keys()
        return word_features

    def __extract_features(self, message):
        words = set(message)
        features = {}

        for word in self.word_features:
            features['%d %s' % (len(word), word)] = (word in words)

        return features

    def __extract_features2(self, message):
        words = set(message)
        features = {}

        for word in words:
            features[word] = True

        return features

    def test_list_classify(self, term):
        # Instantiate Classifier object
        classifier = Classifier()
        results = []

        # Instantiate DAO to retrieve messages
        message_dao = MessageDAO()
        messages = message_dao.retrieve_testing_messages(term)

        for message, sentiment in messages:
            results.append((message, classifier.classify(message)))

        return results


def main():
    classifier = Classifier()
    classifier.test()
    # print classifier.test_list_classify("all")
if __name__ == '__main__':
    main()
