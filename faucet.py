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

class timers:
    usersnamelist = {}
    usersiplist = {}
    ipsfaucethtml = {}
    ipsfavicon = {}

# End Global variables

# Start init flask routes

def faucettimerreset(): # reset the faucet timers at the start of every hour
    while(1):
        if(round(time.time()) % 3600):
            faucetlog("RESET FAUCET TIMER POG")
            timers.usersnamelist = {}
            timers.usersiplist = {}
            timers.ipsfaucethtml = {}
            timers.ipsfavicon = {}
        time.sleep(0.99)

def faucetlog(log): # logger
    print(f"[{time.strftime('%X %x %Z')}] {log}")
    os.system(f"echo [{time.strftime('%X %x %Z')}] {log} >> logfaucet.txt")

@app.route("/", methods=["GET"])
def indexpage():
    return render_template("index.html", faucetversion=faucetVersion)

@app.route("/faucet", methods=["GET"])
def faucetpage():
    return render_template("faucet.html")

@app.route("/faucetchungus", methods=["POST"])
@limiter.limit("1 per minute")
def giveducos():
    if DISABLED: return disabledMessage,500
    randomducoamount = random.uniform(minimumDUCOfromFaucet,maximumDUCOfromFaucet)
    if DEBUG: randomducoamount = 0.00069 # debugging purposes
    socketbuffer = ""
    soc = socket.socket()
    ducoUsername = request.args.get("username")
    faucetlog(f"{request.remote_addr} REQUEST {randomducoamount} by {ducoUsername}")
    if not ducoUsername: return "enter a username you dum dum",404


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
            faucetlog(f"{request.remote_addr} SUCCESS SENT {randomducoamount} to {ducoUsername}")
            return f"success {randomducoamount} sent to {ducoUsername}",200
        elif socketbuffer.startswith("NO"):
            print(f"fail: {socketbuffer}")
            return f"couldnt send, reason {socketbuffer}",500
    except:
        print("send fail xd")
        return "couldnt send for some reason lmao this error shouldnt exist at all XDdfofjdsklafjdslajfsdl",500

faucetlog(f"{__name__} Flask app starting debug: {DEBUG}")

app.run(debug=DEBUG,host="0.0.0.0",port=PORT)
