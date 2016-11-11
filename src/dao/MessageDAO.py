# MessageDAO
# Author: Roshun Jones
# November 11, 2016
# Data Abstraction Object used to retrieve Twitter messages.


class MessageDAO:
    # No arg Constructor
    def __init__(self):
        self.messages = []

    # Retrieves messages from the data source that contains the keyword. If no keyword is provided,
    # all messages in the data source are retrieved.
    def retrieve_messages(self, keyword='all'):
        return self.messages
