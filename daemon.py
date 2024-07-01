import time
import sys
import keys
import middleware_client

import stomp

class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('received an error "%s"' % message)
    def on_message(self, headers, message):
        print('received a message "%s"' % message)

myId = middleware_client.getMyId()
if(myId == -1):
	middleware_client.register()
	time.sleep(2)
	myId = middleware_client.getMyId()

conn = stomp.Connection([(keys.broker_url,keys.broker_port)])
conn.set_listener('', MyListener())
conn.start()
conn.connect('admin', 'admin', wait=True)

conn.subscribe(destination='instructions.'+myId, id=1, ack='auto')

input()
conn.disconnect()
