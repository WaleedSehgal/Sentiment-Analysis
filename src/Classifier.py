from nltk.corpus import stopwords
from MessageDAO import MessageDAO
import nltk.classify


class Classifier:
    def __init__(self):
        self.training_features = None

    # Using a Bag of Words Model, extract features and return dictionary of features
    # Input: List of words
    def __generate_word_features(self, words):
        features = {}
        for word in words:
            features[word] = True
        return features

    def train(self):
        # Get training messages
        message_dao = MessageDAO()

        training_messages = message_dao.retrieve_training_messages()

        # Pre-process training messages
        training_messages = self.__preprocess(training_messages)

        # Get training features
        positive_words = [word for words, sentiment in training_messages for word in words if sentiment == '4']
        negative_words = [word for words, sentiment in training_messages for word in words if sentiment == '0']

        self.training_features = self.__generate_word_features(positive_words + negative_words)

        #training_set = nltk.classify.apply_features(__generate_word_features, training_messages)

        classifier = nltk.NaiveBayesClassifier.train(list(self.training_features))

        # Get Testing Messages
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
    classifier.train()

if __name__ == '__main__':
    main()
