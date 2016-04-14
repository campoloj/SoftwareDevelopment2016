class Player_Proxy(object):

    def __init__(self, id, handler):
        self.id = id
        self.handler = handler

    def listen(self):
        while True:
            data = self.connection.recv(16)
            #print >>sys.stderr, 'received "%s"' % data
            if data:
                #print >>sys.stderr, 'sending data back to the client'
                #self.connection.sendall(data)
                return data
            else:
                #print >>sys.stderr, 'no more data from', client_address
                break

    def test(self):
        print self.id
