__author__ = 'thorwhalen'


# input: message, and possibly args (to be placed in the message string, sprintf-style
# output: Displays the time (HH:MM:SS), and the message
# use: To be able to track processes (and the time they take)
def printProgress(message='',args=[]):
    from datetime import datetime
    if isinstance(args,str): args = [args]
    print str(datetime.now().time()) + ' ' + message.format(*args)

    #def printProgress(message,args):
    #    print "".format([message,str(datetime.now().time())]+args)

