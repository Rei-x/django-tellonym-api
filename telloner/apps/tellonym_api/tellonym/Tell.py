from .Answer import Answer


class Tell:

    def __init__(self, input):
        self.id = input['id']
        self.text = input['tell']

    def is_anonymous_tell(self):

        if self.sender_status == 2:
            return False
        return True
        
    def answer(self, input):
        """
        Answers to the recieved tell

        Args:
            input (str): answer string

        returns:
            Answer class
        """
        data = self.client.answer_tell(self.id, input)
        answer = Answer(self.client, data['answer'])

        return answer

    def delete(self):
        """
        Deletes the received tell
        """
        print(self.client.delete_tell(self.id))
