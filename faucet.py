#!/usr/bin/env python3
#phentem facet

DEBUG = False 

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
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
# Start Global variables

faucetVersion = "Phantom Faucet beta 0.1.1"
faucetUsername = "phantom_faucet"
faucetMessage = "phantom32.tk faucet giving extra rewards!!"
faucetPassword = os.getenv("FAUCET_PASSWORD")
ducoserverAddress = "server.duinocoin.com"
ducosererPorts = [2811,2812,2813]
minimumFaucetBalance = 10

# End Global variables

# Start init flask routes

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
@limiter.limit("1 per hour")
def giveducos():
    return "currently faucet is temporarily disabled because some users are abusing the faucet(i am looking at you, darestz), i will rewrite the whole server backend to prevent it thanks for supporting the faucet :)",500
    randomducoamount = random.uniform(0.1,0.25)
    if DEBUG: randomducoamount = 0.00069 # debugging purposes

    soc = socket.socket()
    ducoUsername = request.args.get("username")
    faucetlog(f"{request.remote_addr} REQUEST {randomducoamount} by {ducoUsername}")
    if not ducoUsername: return "enter a username you dum dum",404


    serveraddress = (ducoserverAddress,random.choice(ducosererPorts))
    try:
        soc.connect(serveraddress)
        ducoserverVersion = print(soc.recv(8))
        soc.send(bytes(f"LOGI,{faucetUsername},{faucetPassword}",encoding="utf8"))
        print(soc.recv(80))
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
        receivedmessage = soc.recv(320).decode("utf8")
        if receivedmessage.startswith("OK"):
            faucetlog(f"{request.remote_addr} SUCCESS SENT {randomducoamount} to {ducoUsername}")
            return f"success {randomducoamount} sent to {ducoUsername}",200
        elif receivedmessage.startswith("NO"):
            print(f"fail: {receivedmessage}")
            return "couldnt send for some reason lmao contact me if this error occurs",500
    except:
        print("send fail xd")
        return "couldnt send for some reason lmao contact me if this error occurs electric boogalo 2",500

faucetlog(f"{__name__} Flask app starting debug: {DEBUG}")
if not __name__ == "__main__":
    print("imported as python module, exiting")
    quit()

app.run(debug=DEBUG,host="0.0.0.0",port=80)
