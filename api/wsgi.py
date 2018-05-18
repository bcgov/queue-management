import eventlet

#Monkey patch to allow for async actions (aka multiple workers)
eventlet.monkey_patch()

print("Hello!")

from qsystem import application, socketio

if __name__ == "__main__":
	print("Starting socketio app with debug=" + application.config['REDIS_DEBUG'])
	socketio.run(application, debug=True)
