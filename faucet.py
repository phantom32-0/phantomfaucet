#!/usr/bin/env python3
#phentem facet

DEBUG = False
PORT = 5000

DISABLED = False
disabledMessage = "faucet is disabled"

minimumDUCOfromFaucet = 0.1
maximumDUCOfromFaucet = 0.15

# Start import modules

import random,math,socket,threading,asyncio,sys,time,os,requests,json
from dotenv import load_dotenv
from flask import Flask, request, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from requests.sessions import Request

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

faucetVersion = "Phantom Faucet beta 0.3"
faucetUsername = "phantom_faucet"
faucetMessage = "phantom32.tk wooohooooooooooooo epic faucet"
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

def getip(request): # gets ip of the client
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr

#def discordwebhook(message):
#    data = {"embeds": [{"description": message }]}
#    requests.post(os.getenv("DISCORD_WEBHOOK_URL"), json = data)

def faucettimerreset(): # reset the faucet timers at the start of every hour
    while(1):
        if((round(time.time()) % 3600) == 0):
            faucetlog(f"RESET FAUCET TIMER POG users this hour: {timers.usersnamelist}")
            timers.usersnamelist = []
            timers.usersiplist = []
            timers.ipsfaucethtml = []
        time.sleep(0.99)

def faucetlog(log): # logger
    print(f"[{time.strftime('%X %x %Z')}] {log}")
    os.system(f"echo [{time.strftime('%X %x %Z')}] {log} >> logfaucet.txt")
    data = {"embeds": [{"description": f"[{time.strftime('%X %x %Z')}] {log}" }]}
    lolololol = requests.post(os.getenv("DISCORD_WEBHOOK_URL"), json = data)

@app.route("/", methods=["GET"])
def indexpage():

    return render_template("index.html", faucetversion=faucetVersion)

@app.route("/faucet", methods=["GET"])
def faucetpage():
    if getip(request) not in timers.ipsfaucethtml:
        timers.ipsfaucethtml.append(getip(request))
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
    faucetlog(f"REQUEST {randomducoamount} by {ducoUsername}")
    if not ducoUsername: return "enter a username you dum dum",404

    if ducoUsername in bannedlist:
        faucetlog(f"lmao {ducoUsername} tried to use the faucet but he/she is banned")
        return "uh oh looks like you are banned from using the faucet if you want to get unbanned dm me on duinocoin discord phantom32#5148",400

    if getip(request) not in timers.ipsfaucethtml :
        faucetlog(f"{ducoUsername} doesnt look like he is in all ip lists XD nomoney for yuo")
        return "uh oh, your actions looks sussy, if you are not a bot contact me on duinocoin discord phantom32#5148",401
        
    if ducoUsername in timers.usersnamelist or getip(request) in timers.usersiplist:
        faucetlog(f"{ducoUsername} tried to use the faucet but they used it in the last hour")
        return f"uh oh, looks like you used the faucet this hour, try again at the start of next hour, debug: {getip(request)}",400
    try:
        r = requests.get(f"https://{ducoserverAddress}/transaction?username={faucetUsername}&password={faucetPassword}&recipient={ducoUsername}&amount={randomducoamount}&memo={faucetMessage}")
        r.raise_for_status()
    except Exception as e:
        faucetlog(f"{ducoUsername} couldnt request transaction oops {e}")
        return "couldnt connect to the master server oops try again later",500
    if DEBUG: print(r.text)
    serverresponse = json.loads(r.text)

    serverresponse = serverresponse["result"]

    serverresponse.split(",")
    if not serverresponse.startswith('OK'):
        faucetlog(f"{ducoUsername} fail sending {serverresponse}")
        return f"uh oh, couldnt send the ducos to {ducoUsername}, reason {serverresponse}",500
    timers.usersnamelist.append(ducoUsername)
    timers.usersiplist.append(getip(request))
    faucetlog(f"SUCCESS SENT {randomducoamount} to {ducoUsername}")
    return f"yayyyyyyyyyyy sent {randomducoamount} to {ducoUsername} yay you can use the faucet again at the start of the next hour"


@app.route("/banhammer",methods=["POST"])
def banhammer():
    message = request.args.get("message")
    message.split(",")
    if message[0] != faucetPassword:
        return "",404
    if message[1] not in bannedlist:
        faucetlog(f"{getip(request)} THE BAN HAMMER HAS SPOKEN: banned user {message[1]}")
        bannedlist.append(message[1])
        file = open("blacklist.txt","w")
        file.write(bannedlist)
        file.close()
        return f"success banned {message[1]}, new ban list is {bannedlist}",200
    else:
        faucetlog(f"{getip(request)} THE BAN HAMMER HAS SPOKEN: couldnt ban user becase its albeady banned lmao {message[1]}")
        return f"the user {message[1]} is already bannedl ol the ban list is {bannedlist}"

faucetlog(f"{__name__} Flask app starting debug: {DEBUG}")
file = open("blacklist.txt", "r")
bannedlist = file.read()
faucetlog(f"Loaded ban list: {bannedlist}")

faucetlog("faucet timer thread starting")
timerthread = threading.Thread(target=faucettimerreset, args=(), daemon=True)
timerthread.start()

if __name__ == "__main__":
    app.run(debug=DEBUG,host="0.0.0.0",port=PORT)
