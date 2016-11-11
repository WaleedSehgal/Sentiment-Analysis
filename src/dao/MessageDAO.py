# MessageDAO
# Author: Roshun Jones
# November 11, 2016
# Data Abstraction Object used to retrieve Twitter messages.

import csv


class MessageDAO:
    # No arg Constructor
    def __init__(self):
        self.messages = [] # Empty list
        self.data_source_file_name = "../../resources/test_data.csv"

    # Retrieves messages from the data source that contains the keyword. If no keyword is provided,
    # all messages in the data source are retrieved.
    def retrieve_messages(self, keyword='all'):
        # Read file
        with open(self.data_source_file_name) as file:
            reader = csv.reader(file)
            for line in reader:
                message = line[5]
                if keyword == 'all' or (keyword != 'all' and (message.find(keyword) != -1)):
                    self.messages.append(message)

        return self.messages


def main():
    # Used for testing
    messageDAO = MessageDAO()
    print messageDAO.retrieve_messages('cheering')

if __name__ == '__main__':
    main()