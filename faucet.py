#!/usr/bin/env python3
#phentem facet

DEBUG = True
PORT = 5000

DISABLED = False
disabledMessage = "faucet is disabled"

minimumDUCOfromFaucet = 0.1
maximumDUCOfromFaucet = 0.2

# Start import modules

import random,math,socket,threading,asyncio,sys,time,os
from dotenv import load_dotenv
from flask import Flask, request, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()
random.seed()
randomducoamount = 0

# End import modules

# init Flask application
app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address
)
# Start Global variables

faucetVersion = "Phantom Faucet beta 0.2"
faucetUsername = "phantom_faucet"
faucetMessage = "phantom32.tk duinocion fauet come bakc sooon"
faucetPassword = os.getenv("FAUCET_PASSWORD")
ducoserverAddress = "server.duinocoin.com"
ducosererPorts = [2811,2812,2813]
minimumFaucetBalance = 10

bannedlist = {}

class timers:
    usersnamelist = []
    usersiplist = []
    ipsfaucethtml = []
    ipsfavicon = []
    ipsindexhtml = []

# End Global variables

# Start init flask routes

def faucettimerreset(): # reset the faucet timers at the start of every hour
    while(1):
        if((round(time.time()) % 3600) == 0):
            faucetlog(f"RESET FAUCET TIMER POG users this hour: {timers.usersnamelist}")
            timers.usersnamelist = []
            timers.usersiplist = []
            timers.ipsfaucethtml = []
            timers.ipsfavicon = []
        time.sleep(0.99)

def faucetlog(log): # logger
    print(f"[{time.strftime('%X %x %Z')}] {log}")
    os.system(f"echo [{time.strftime('%X %x %Z')}] {log} >> logfaucet.txt")

@app.route("/favicon.ico", methods=["GET"])
def faviconpage():
    if request.remote_addr not in timers.ipsfavicon:
        timers.ipsfavicon.append(request.remote_addr) # nobody is going to notice a thing
    return "",404

@app.route("/", methods=["GET"])
def indexpage():
    if request.remote_addr not in timers.ipsindexhtml:
        timers.ipsindexhtml.append(request.remote_addr)
    return render_template("index.html", faucetversion=faucetVersion)

@app.route("/faucet", methods=["GET"])
def faucetpage():
    if request.remote_addr not in timers.ipsfaucethtml:
        timers.ipsfaucethtml.append(request.remote_addr)
    return render_template("faucet.html")

@app.route("/faucetchungus", methods=["POST"])
@limiter.limit("1 per 10 second")
def giveducos():
    if DISABLED: return disabledMessage,500
    randomducoamount = random.uniform(minimumDUCOfromFaucet,maximumDUCOfromFaucet)
    if DEBUG: randomducoamount = 0.00069 # debugging purposes
    socketbuffer = ""
    soc = socket.socket()
    ducoUsername = request.args.get("username")
    faucetlog(f"{request.remote_addr} REQUEST {randomducoamount} by {ducoUsername}")
    if not ducoUsername: return "enter a username you dum dum",404

    if ducoUsername in bannedlist:
        faucetlog(f"{request.remote_addr} lmao {ducoUsername} tried to use the faucet but he/she is banned")
        return "uh oh looks like you are banned from using the faucet if you want to get unbanned dm me on duinocoin discord phantom32#5148",400

    if request.remote_addr not in timers.ipsfavicon or request.remote_addr not in timers.ipsfaucethtml or request.remote_addr not in timers.ipsindexhtml:
        faucetlog(f"{request.remote_addr} {ducoUsername} doesnt look like he is in all ip lists XD nomoney for yuo")
        if ducoUsername not in timers.usersnamelist: timers.usersnamelist.append(ducoUsername)
        return "uh oh, your actions looks like a bot, if you are not a bot contact me on duinocoin discord phantom32#5148",401
        
    if ducoUsername in timers.usersnamelist or request.remote_addr in timers.usersiplist:
        return "uh oh, looks like you used the faucet this hour, try again at the start of next hour",400

    serveraddress = (ducoserverAddress,random.choice(ducosererPorts))
    try:
        soc.connect(serveraddress)
        ducoserverVersion = print(soc.recv(8))
        soc.send(bytes(f"LOGI,{faucetUsername},{faucetPassword}",encoding="utf8"))
        socketbuffer = soc.recv(80)
        if DEBUG: print(socketbuffer)
    except:
        faucetlog(f"{request.remote_addr} {ducoUsername} couldnt log in to faucet account")
        return "server sided error: couldnt login to faucet account",500
    try:
        soc.send(bytes(f"BALA,{faucetUsername}",encoding="utf8"))
        faucetBalance = soc.recv(320).decode("utf8")
        print(faucetBalance)
    except:
        faucetlog(f"{request.remote_addr} {ducoUsername} couldnt retrieve balance")
        return "server sided error: cannot retrieve faucet balance",500
    try:
        if float(faucetBalance) < randomducoamount:
            return "faucet empty :(",500
    except:
        faucetlog(f"{request.remote_addr} {ducoUsername} server closed connection")
        return "server sided error: server closed connection",500
    try:
        soc.send(bytes(f"SEND,{faucetMessage},{ducoUsername},{randomducoamount}",encoding="utf8"))
        socketbuffer = soc.recv(320).decode("utf8")
        if socketbuffer.startswith("OK"):
            timers.usersnamelist.append(ducoUsername)
            timers.usersiplist.append(request.remote_addr)
            faucetlog(f"{request.remote_addr} SUCCESS SENT {randomducoamount} to {ducoUsername}")
            
            return f"success {randomducoamount} ducos sent to {ducoUsername} yayyyyyyy",200
        elif socketbuffer.startswith("NO"):
            socketbuffer.split(",")
            return f"couldnt send, reason {socketbuffer[1]}",500
    except:
        print("send fail xd")
        return "couldnt send for some reason lmao this error shouldnt exist at all XDdfofjdsklafjdslajfsdl",500

@app.route("/banhammer",methods=["POST"])
def banhammer():
    message = request.args.get("message")
    message.split(",")
    if message[0] != faucetPassword:
        return "",404
    if message[1] not in bannedlist:
        faucetlog(f"{request.remote_addr} THE BAN HAMMER HAS SPOKEN: banned user {message[1]}")
        bannedlist.append(message[1])
        file = open("blacklist.txt","w")
        file.write(bannedlist)
        file.close()
        return f"success banned {message[1]}, new ban list is {bannedlist}",200
    else:
        faucetlog(f"{request.remote_addr} THE BAN HAMMER HAS SPOKEN: couldnt ban user becase its albeady banned lmao {message[1]}")
        return f"the user {message[1]} is already bannedl ol the ban list is {bannedlist}"

faucetlog(f"{__name__} Flask app starting debug: {DEBUG}")
file = open("blacklist.txt", "r")
bannedlist = file.read()
faucetlog(f"Loaded ban list: {bannedlist}")

faucetlog("faucet timer thread starting")
timerthread = threading.Thread(target=faucettimerreset, args=(), daemon=True)
timerthread.start()

app.run(debug=DEBUG,host="0.0.0.0",port=PORT)
