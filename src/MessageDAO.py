# MessageDAO
# Author: Roshun Jones
# November 11, 2016
# Data Abstraction Object used to retrieve Twitter messages.

import csv


class MessageDAO:
    # No arg Constructor
    def __init__(self):
        self.messages = []  # Empty list
        self.train_data_file_name = "../resources/train_data.csv"
        self.test_data_file_name = "../resources/test_data.csv"

    # Retrieve messages from provided file
    def __retrieve_messages(self, file_name, keyword='all'):
        # Read file
        with open(file_name) as file:
            reader = csv.reader(file)
            for line in reader:
                sentiment = line[0]
                if sentiment == '4':
                    sentiment = 'Positive'
                elif sentiment == '0':
                    sentiment = 'Negative'
                message = line[5]
                if keyword == 'all' or (keyword != 'all' and (message.find(keyword) != -1)):
                    self.messages.append((message, sentiment))

        return self.messages

    # Retrieves training messages from the data source that contains the keyword. If no keyword is provided,
    # all messages in the data source are retrieved.
    def retrieve_training_messages(self, keyword='all'):
        return self.__retrieve_messages(self.train_data_file_name, keyword)

    # Retrieves testing messages from the data source that contains the keyword. If no keyword is provided,
    # all messages in the data source are retrieved.
    def retrieve_testing_messages(self, keyword='all'):
        return self.__retrieve_messages(self.test_data_file_name, keyword)


def main():
    # Used for testing
    messageDAO = MessageDAO()
    print messageDAO.retrieve_training_messages('cheering')
    print messageDAO.retrieve_testing_messages('cheering')

if __name__ == '__main__':
    main()