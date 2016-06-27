#Python 2.7 irc Octo-bot 
import socket
import time
import json
import threading

#My stuff
import asteroid
import areyoubeingwatched

with open('commands.json', 'r') as f:
    
    commands = json.load(f)
    f.close()
    
with open('config.json', 'r') as f:
    
    config = json.load(f)
    f.close()
    
with open('perms.json', 'r') as f:
    
    perms = json.load(f)
    f.close()
    
_version_ = config['general']['version']
_author_ = config['general']['author']

botnick = config['info']['botnick']
realname = 'Octo[bot] {0} Author: {1}'.format(_version_, _author_)
ident =  config['info']['ident']
passwd = config['info']['pass']
network = config['network']['network']
port = config['network']['port']
channels  = config['channels']
debug = config['general']['debug']
commandchar = config['general']['commandchar']

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((network, port))

    
def connectandidentify():
        
    send('PASS {0}'.format(passwd))
    send('NICK {0}'.format(botnick))
    send('USER {0} {1} blah :{2}'.format(ident, network, realname))
    
    
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
        data = data.replace(':', '')
        data = data.split()
        if debug: print data
        
        if data[0] == 'PING':
            send('PONG :{0}'.format(data[1]))
            if debug: print 'Pong sent to {0}'.format(data[1])
        
        if data[1] == 'INVITE':
            
            send('JOIN {0}'.format(data[3]))
            
            if data[3] not in channels:
                config['channels'].append(data[3])
                
                with open('config.json', 'w') as f:
                    
                    json.dump(config, f, indent=4)
                    
                
        
        
        if len(data) > 3:
         
                
            if commandchar in data[3]:
                
                   
                    
                channel = data[2]
            
            
                if debug: print 'Channel is: ' + channel 
                
                
                data[3] = data[3].replace(commandchar, '')
                sendercloak = data[0].split('@')[1]
                
                if debug: print 'Command is: ' + data[3]
                
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
                        
                        sendtochan('Channels that I am in: ' + ', '.join(channels), channel)
                        
                    else:
                        
                        sendtochan("You can only use 'channels' or 'commands'", channel)
                
                elif data[3] == 'ping': 
                    
                    sendtochan('OCTOPONG', channel)
                    if debug: print 'Sending to, ' + channel
                    
                elif data[3] == 'moo':
                    
                    sendtochan('moo!', channel)
                    
                elif data[3] == 'leave':
                    
                    if sendercloak == perms['master']:
                        if len(data) < 5:
                            
                            sendtochan('You need another argument. {0}'.format(commands['leave']['syntax']), channel)
                            
                        elif data[4] in channels:
                            
                            send('PART {0}'.format(data[4]))
                            channels.remove(data[4])
                            
                        else:
                            
                            sendtochan('I am not in {0})'.format(data[4]), channel)
                            
                    else:
                        
                        sendtochan('You do not have permission to do that!', channel)
                        
                elif data[3] == 'are-we-safe?':
                    
                    
                    sendtochan(asteroid.checkifsafe(), channel)
                    
                elif data[3] == 'am-I-being-watched?':
                    
                    if len(data) < 6:
                        
                        sendtochan('You need another argument. {0}'.format(commands['am-I-being-watched?']['syntax']), channel)
                    else:
                        
                        sendtochan(areyoubeingwatched.check(data[4], data[5]), channel)
                else:
                    
                    sendtochan('{0} is not a valid command! Do _8list commands for a list of commands.'.format(data[3]), channel)
                    
        

