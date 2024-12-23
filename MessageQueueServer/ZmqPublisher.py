import zmq


class ZmqPublisher:
    def __init__(self, store, emailHandler):

        self.storeContext = store
        self.emailHandler = emailHandler
        self.publisherContext = zmq.Context()
        self.publisherSocket = self.publisherContext.socket(zmq.PUB)
        self.publisherSocket.bind("tcp://127.0.0.1:5000")
        print("Publisher started on port 5000")

    def triggerSubscribe(self, subject):
        userEmailList = self.storeContext.getEmailStore(subject)
        updateContent = self.storeContext.getContentBySubject(subject)
        for email in userEmailList:
            self.emailHandler.send_email(email, subject, updateContent)

        self.publisherSocket.send_string(f"{subject} {updateContent}")
