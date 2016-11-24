from nltk.corpus import stopwords
from MessageDAO import MessageDAO
import nltk.classify
import pickle


class Classifier:
    def __init__(self):
        self.training_features = []
        self.testing_features = []

    def classify(self):
        print 'Classify'

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

    def test(self, classifier):
        print 'Acquiring testing messages...'

        message_dao = MessageDAO()
        testing_messages = message_dao.retrieve_testing_messages()

        # Pre-process testing messages
        testing_messages = self.__preprocess(testing_messages)[:100]

        print 'Generating test features'

        # Get testing features
        positive_words = [word for words, sentiment in testing_messages for word in words if sentiment == '4']
        negative_words = [word for words, sentiment in testing_messages for word in words if sentiment == '0']

        self.testing_features.append((self.__generate_word_features(positive_words), '4'))
        self.testing_features.append((self.__generate_word_features(negative_words), '0'))

        print 'Testing...'
        print 'Accuracy:', nltk.classify.util.accuracy(classifier, self.testing_features)

    # Using a Bag of Words Model, extract features and return dictionary of features
    # Input: List of words
    def __generate_word_features(self, words):
        features = {}
        for word in words:
            features[word] = True
        return features

    def __train(self):
        print 'Acquiring training messages...'

        # Get training messages
        message_dao = MessageDAO()

        training_messages = message_dao.retrieve_training_messages()

        # Pre-process training messages
        training_messages = self.__preprocess(training_messages)[:100]

        print 'Generating training features...'

        # Get training features
        positive_words = [word for words, sentiment in training_messages for word in words if sentiment == '4']
        negative_words = [word for words, sentiment in training_messages for word in words if sentiment == '0']

        self.training_features.append((self.__generate_word_features(positive_words),'4'))
        self.training_features.append((self.__generate_word_features(negative_words), '0'))

        print 'Training...'

        classifier = nltk.NaiveBayesClassifier.train(self.training_features)

        # Save classifier
        f = open('classifier.pickle', 'wb')
        pickle.dump(classifier, f)
        f.close()

        return classifier


    # Removes stop words from list of words inputed.
    # Utilizes corpus provided by NLTK
    # Input: List of tuples(List of words, sentiment)
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
            # Transform list to tokenized list and lower case
            words = [word.lower() for word in message.split()]
            tokenized_messages.append((words, sentiment))
        return tokenized_messages

    # Preprocessing method
    def __preprocess(self, messages):
        # Tokenize messages
        processed_messages = self.__tokenize_input(messages)

        return processed_messages


def main():
    classifier = Classifier()
    c = classifier.get_classifier()
    classifier.test(c)

if __name__ == '__main__':
    main()
