class Lock:
    def __init__(self, *codes):
        self.codes = codes
        self.position = None
        self.auto_destroys = False
        self.message_in_front = "You are standing in front of a code lock. \n" \
                                "It needs one or more codes to open. Call open_lock() with the code(s)."

        self.message_when_open = "Well done! The lock is open.\n" \
                                 "Please proceed."

        self.message_wrong_code = "The code you tried did not work. \n" \
                                  "Try another one."

    def open(self, *codes):
        return self.codes == codes


class Friend:
    def __init__(self, data, message):
        self.data = data
        self.message = message
        self.message_in_front = "You have met a friend. You can ask her something.\n" \
                                "Call the ask() function."

