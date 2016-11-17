from nltk.corpus import stopwords
from MessageDAO import MessageDAO
import nltk.classify


class Classifier:
    def __init__(self):
        self.training_features = None

    # Feature Extraction
    def extract_features(self, message, training_features):
            features = {}
            words = set(message)
            for word in training_features:
                features[word] = (word in words)
            return features

    def train(self):
        # Get training messages
        message_dao = MessageDAO()

        training_messages = message_dao.retrieve_training_messages()

        # Preprocess training messages
        training_messages = self.__preprocess(training_messages)

        # Get training features
        self.training_features = self.__generate_word_features(training_messages)

        training_set = nltk.classify.apply_features(self.extract_features, training_messages)

        classifier = nltk.NaiveBayesClassifier.train(training_set)

        # Get Tesing Messages
        testing_messages = message_dao.retrieve_testing_messages()

        print 'Accuracy:', nltk.classify.accuracy(classifier, testing_messages)

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
    def __generate_word_features(self, messages):
        temp = []

        for (messages, sentiment) in messages:
            temp.extend(messages)

        return list(set(temp))

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


    # Feature Extraction
    def extract_features(self, message):
        features = {}
        words = set(message)
        for word in self.training_features:
            features['contains(%s)' % word] = (word in words)
        return features


def main():
    classifier = Classifier()
    classifier.train()

if __name__ == '__main__':
    main()
