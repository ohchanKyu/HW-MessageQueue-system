from EmailHandler import EmailHandler
from StoreContext import StoreContext
from ZmqServer import ZmqServer
from ZmqPublisher import ZmqPublisher

globalStore = StoreContext()
emailHandler = EmailHandler()
ZmqPublisher = ZmqPublisher(globalStore, emailHandler)
serverInstance = ZmqServer(globalStore, ZmqPublisher)

serverInstance.startServer()