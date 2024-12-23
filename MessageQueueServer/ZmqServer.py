import zmq
import json


class ZmqServer:
    def __init__(self, store, zmqPublisher):
        self.storeContext = store
        self.zmqPublisher = zmqPublisher
        self.serverContext = zmq.Context()
        self.serverSocket = self.serverContext.socket(zmq.REP)
        self.serverSocket.bind("tcp://127.0.0.1:8080")
        print("Listening Client request on port 8080")

    def startServer(self):
        while True:
            message = self.serverSocket.recv_string()
            print(f"Received request from Client : {message}")
            response = self.generateResponseMessage(message)
            self.serverSocket.send_string(response)

    def generateResponseMessage(self, request):
        parsedData = json.loads(request)
        requestType = parsedData["type"]
        match requestType:
            case "1":
                subjectList = self.storeContext.getAllSubjectList()
                formattedSubjects = " ".join([f"[{subject}]" for subject in subjectList])
                return formattedSubjects
            case "2":
                user_email = parsedData["email"]
                user_subject = parsedData["subject"]
                if self.storeContext.isExistSubject(user_subject):
                    response = self.storeContext.addEmailBySubject(user_subject, user_email)
                    responseData = {"data": response, "isValid": "isSuccess"}
                    print("Successfully register email and subscribe")
                    return json.dumps(responseData)
                else:
                    responseData = {"data": f"Not exist subject - {user_subject}. Try again!", "isValid": "Fail"}
                    return json.dumps(responseData)
            case "3":
                subject = parsedData["subject"]
                newContent = parsedData["updateMessage"]
                self.storeContext.addContentSubjectStore(subject, newContent)
                self.zmqPublisher.triggerSubscribe(subject)
                print("Successfully update content and send email")
                return "isSuccess"
            case "4":
                user_email = parsedData["email"]
                subject = parsedData["subject"]
                self.storeContext.deleteEmail(subject,user_email)
                print(f"Successfully delete email - {user_email}")
                return "isSuccess"
            case _:
                return "Invalid Request. Please try again."


