from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = input('Digite uma frase minuscula:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print ('Resposta do servidor:', modifiedSentence.decode());
clientSocket.close()

boolean connection = true;
event = threading.Event()
while connection
    temperature = client.getTemperature();
    timestemp = client.getTimestam();
    sentence = temperature + " " + timestemp;
    clientSocket.send(sentence.encode())
    event.wait(600)