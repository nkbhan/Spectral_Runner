import threading

theVar = 1

class MyThread(threading.Thread):

    def run(self):

        global theVar
        print('This is thread ' + str(theVar) + ' speaking.')
        print('Hello and good bye.')
        theVar = theVar + 1

for x in range(20):
    MyThread().start()
