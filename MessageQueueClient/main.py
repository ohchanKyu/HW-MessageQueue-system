import time
import zmq
import threading
import json
import re

isRunning = True
isSubscribe = False
subscribeSubject = ""
subscribeEmail = ""
requestContext = zmq.Context()
requestSocket = requestContext.socket(zmq.REQ)
requestSocket.connect("tcp://localhost:8080")
REGEX_EMAIL = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
stop_event = threading.Event()


def convertJsonToString(jsonData):
    return json.dumps(jsonData)


def printMenu():
    print("=== Command Menu ===")
    print("1: Display the Subject of Pub-Sub-System")
    print("2: Select a Subject And Register Email to Pub-Sub-System")
    print("3: Update Content for the topic you registered and trigger all other subscribers")
    print("4: Print the Menu again")
    print("q: Quit the program")
    print("====================")


def startSubscribe(subject, data):
    context = zmq.Context()
    subscriber_socket = context.socket(zmq.SUB)
    subscriber_socket.connect("tcp://localhost:5000")
    connectMessage = f"\nConnected to publisher on port 5000, subscribing to '{subject}'\n"
    connectMessage += f"[{subject} Content]\n"
    connectMessage += f"{data}\n"
    print(connectMessage)
    subscriber_socket.setsockopt_string(zmq.SUBSCRIBE, subject)

    while not stop_event.is_set():
        try:
            subsMessage = subscriber_socket.recv_string(flags=zmq.NOBLOCK)
            if subsMessage:
                printMessage = f"\n--- New Subscribe Message Received ---\n"
                printMessage += f"Topic - {subsMessage.split(' ')[0]}\n"
                printMessage += f"[Message] \n{' '.join(subsMessage.split(' ')[1:])}\n"
                printMessage += f"------------------------------\n"
                print(printMessage)
        except zmq.Again:
            pass


def startSubscribeThread(subject, data):
    subscribe_thread = threading.Thread(target=startSubscribe, args=(subject, data,))
    subscribe_thread.daemon = True
    subscribe_thread.start()


printMenu()
while isRunning:
    print("")
    userCommand = input("Input your command : ")
    match userCommand:
        case "1":
            request_data = { "type" : "1" }
            requestSocket.send_string(convertJsonToString(request_data))
            message = requestSocket.recv_string()
            print("Received from System - Subject List")
            print(message)
        case "2":
            userSubject = input("Select Subject : ")
            userEmail = input("Register Your Email : ")
            if not re.fullmatch(REGEX_EMAIL, userEmail):
                print("Email is not valid! try again.")
                continue
            request_data = { "type": "2", "email" : userEmail, "subject" : userSubject}
            requestSocket.send_string(convertJsonToString(request_data))

            message = requestSocket.recv_string()
            parsedData = json.loads(message)
            isValid = parsedData["isValid"]
            responseData = parsedData["data"]
            if isValid == "isSuccess":
                isSubscribe = True
                subscribeSubject = userSubject
                subscribeEmail = userEmail
                startSubscribeThread(userSubject,responseData)
                time.sleep(2)
            else:
                print(responseData)
        case "3":
            if not isSubscribe:
                print("You have not subscribed yet. Please subscribe first.")
            else:
                updateText = input("Input Update Text : ")
                if len(updateText) == 0:
                    print("Please enter the Message")
                else:
                    request_data = {"type": "3", "subject" : subscribeSubject , "updateMessage": updateText}
                    requestSocket.send_string(convertJsonToString(request_data))
                    message = requestSocket.recv_string()
                    if message == "isSuccess":
                        print("Successfully update content! and trigger all other subscribes")
        case "4":
            printMenu()
        case "q":
            isRunning = False
            if isSubscribe:
                request_data = {"type": "4", "subject" : subscribeSubject, "email" : subscribeEmail}
                requestSocket.send_string(convertJsonToString(request_data))
            print("Close Client. and cancel subscribe")
            stop_event.set()
        case _:
            print("Invalid command. Please try again.")
