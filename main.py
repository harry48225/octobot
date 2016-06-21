#Python 2.7 irc Octo-bot 
import socket
import time
import json

import asteroid

_version_ = '0.01'
_author_ = 'harry48225'


usrname = 'ENTER HERE'
passwd = 'ENTER HERE'
botnick = 'Octo[bot]'
realname = 'Octo[bot] {0} Author: {1}'.format(_version_, _author_)
ident =  botnick
network = 'irc.freenode.net'
port = 6667
channels  = []

commandchar = '_8'

with open('commands.json', 'r') as f:
    
    commands = json.load(f)
    
with open('usrandpass', 'r') as f:
    
    usrname = f.readline()
    passwd = f.readline()

with open('channels', 'r') as f:
    
    channels = f.read().rstrip().split()

lastsender = ''

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((network, port))
    
def connectandidentify():

    send('NICK {0}'.format(botnick))
    send('USER {0} {1} blah :{2}'.format(ident, network, realname))
    i = 0
    while True:
        print i
        data = recieve() 
        print data
        i += 1
        if '<password>' in data:
            print '376 found'
            break
    
    
    send('MSG NickServ identify {0}'.format(passwd))
    print 'sent passwd'
    
    
def sendtochan(string, channel):
    
    irc.send('PRIVMSG {0} :{1}\r\n'.format(channel, string).encode('UTF-8'))

def send(string):
    
    irc.send('{0}\r\n'.format(string).encode('UTF-8'))
    
def recieve():
    
    data = irc.recv(4096)
    return data
    
if __name__ == '__main__':
        
    connectandidentify()
    for channel in channels:
        send('JOIN {0}'.format(channel))
    
    while True:
        data = recieve()
        print data
        data = data.replace(':', '')
        data = data.split()
        print data
        
        if data[0] == 'PING':
            irc.send('PONG\r\n'.encode('UTF-8'))
        
        if data[1] == 'INVITE':
            
            send('JOIN {0}'.format(data[3]))
            
            if data[3] not in channels:
                channels.append(data[3])
        
        
        if len(data) > 3:
            
                    
            channel = data[2]  
                
            if commandchar in data[3]:
                
                
                data[3] = data[3].replace(commandchar, '')
                print data[3]
                
                if data[3] == 'help':
                    
                    if len(data) < 5:
                        
                        sendtochan("{0}'s usage is: {1}, and it's syntax is: {2}".format('help', commands['help']['usage'], commands['help']['syntax']), channel)
                    
                    
                    elif len(data) == 5:
                        
                        try:
                            sendtochan("{0}'s usage is: {1}, and it's syntax is: {2}".format(data[4], commands[data[4]]['usage'], commands[data[4]]['syntax']), channel)
                            
                    
                        except:
                            
                            sendtochan('{0} is not a valid command!'.format(data[4]), channel)
                    
                    elif len(data) == 6:
                        
                        try:
                            sendtochan("{0}'s {1} is: {2}".format(data[4], data[5], commands[data[4]][data[5]]), channel)
                        
                        except:
                            
                            if data[4] not in commands:
                                
                                sendtochan('{0} is not a valid command!'.format(data[4]), channel)
                            
                            else:
                                
                                sendtochan("Please only use 'usage' or 'syntax'", channel)
                    
                
                elif data[3] == 'list':
                    
                    if len(data) < 5:
                        
                        sendtochan('You need another argument. {0}'.format(commands['list']['syntax']), channel)
                        
                    elif data[4] == 'commands':
                        
                        sendtochan('Command list: ' + ', '.join(commands.keys()), channel)
                        
                    elif data[4] == 'channels':
                        
                        sendtochan('Channels that I am connected to: ' + ', '.join(channels), channel)
                        
                    else:
                        
                        sendtochan("You can only use 'channels' or 'commands'", channel)
                
                elif data[3] == 'ping': 
                    sendtochan('OCTOPONG', channel)
                    print 'Sending to, ' + channel
                    
                elif data[3] == 'moo':
                    sendtochan('moo!', channel)
                    
                elif data[3] == 'leave':
                    
                    if len(data) < 5:
                        
                        sendtochan('You need another argument. {0}'.format(commands['leave']['syntax']), channel)
                        
                    elif data[4] in channels:
                        
                        send('PART {0}'.format(data[4]))
                        channels.remove(data[4])
                        
                    else:
                        
                        sendtochan('I am not connected to {0)'.format(data[4]), channel)
                        
                elif data[3] == 'are-we-safe?':
                    
                    sendtochan(asteroid.checkifsafe(), channel)
                    
                else:
                    
                    sendtochan('{0} is not a valid command! Do _8list commands for a list of commands.'.format(data[3]), channel)
                    
        

