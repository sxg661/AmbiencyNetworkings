import queue

class SocketWrapper:

    def __init__(self, connection):
        self.connection = connection
        self.inputQueue = queue.Queue()
        self.leftover = ""

    def split_message(self, message):
        currentWord = ""
        words = []
        inNewLine = False
        for ch in message:
            if(ch == '\n' and not inNewLine):
                inNewLine = True
            elif (ch == '\n' and inNewLine):
                inNewLine = False
                words.append(self.leftover + currentWord)
                currentWord = ""
                self.leftover = ""
            elif(ch != '\n' and inNewLine):
                currentWord = currentWord + '\n' + ch
            else:
                currentWord = currentWord + ch

        if(currentWord != ""):
            self.leftover = currentWord
        return words

    def refillQueue(self):
        commands = self.connection.recv(2048).decode('utf-8')
        print("Recieved" + commands)
        commands = self.split_message(commands)
        for command in commands:
            self.inputQueue.put(command)

    
    def send(self, string):
        self.connection.send(bytes(string + "\n\n", 'utf-8'))

    def recv(self):
        while(self.inputQueue.empty()):
            self.refillQueue()
        return self.inputQueue.get()

        










        
        
        
