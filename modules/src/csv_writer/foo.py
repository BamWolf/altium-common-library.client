
print 'Plugin loaded!'

name = 'MySQLPlug'

class MySQLPlugin:

    def echo(self, message):
        return message[::-1]
    

