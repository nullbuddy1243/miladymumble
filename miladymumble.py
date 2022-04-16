import tweepy
import pickledb
import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import pymongo

from censor import *

from web3.auto import w3
from web3 import Web3
from eth_account.messages import defunct_hash_message

load_dotenv()
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def setLastTweet(tokenId):
    store = pickledb.load('store.db', auto_dump=True)
    store.set(tokenId, time.time())

def getlastTweet(tokenId):
    store = pickledb.load('store.db', auto_dump=True)
    last = store.get(tokenId)
    return last

def verifyLastTweet(tweet):
    last = getlastTweet(tweet['tokenId'])
    if(last and last + 86400 > time.time()):
        return False
    return True

def verifySignature(tweet):
    message_hash = defunct_hash_message(text=tweet['message'])
    address = w3.eth.account.recoverHash(
        message_hash,
        signature=tweet['signature'])
    if(address != tweet['address']): 
        return False
    else:
        return True

def verifyBalance(tweet):
    address = '0x5Af0D9827E0c53E4799BB226655A1de152A425a5'
    abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"MAX_MILADYS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MILADY_PROVENANCE","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"array","type":"address[]"}],"name":"editWhitelistOne","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"array","type":"address[]"}],"name":"editWhitelistTwo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"flipSaleState","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxMiladyPurchase","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"numberOfTokens","type":"uint256"}],"name":"mintMiladys","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"reserveMintMiladys","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"saleIsActive","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"baseURI","type":"string"}],"name":"setBaseURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"provenanceHash","type":"string"}],"name":"setProvenanceHash","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"standardMiladyCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"whitelistOneMint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"whitelistTwoMint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    infurakey = os.getenv("INFURA_TOKEN")
    infura = f"https://mainnet.infura.io/v3/{infurakey}"
    activeW3 = Web3(Web3.HTTPProvider(infura))
    contract_instance = activeW3.eth.contract(address=address, abi=abi)
    owner = contract_instance.functions.ownerOf(int(tweet['tokenId'])).call()
    return owner == tweet['address']

@app.get("/times")
async def postTweet():
    store = pickledb.load('store.db', auto_dump=False)
    return store.db

@app.post("/tweet")
async def postTweet(request: Request):
    tweet = await request.json()
    if(not verifyLastTweet(tweet)):
        return {"Error": "tweeting too soon"}
    if(not verifySignature(tweet)): 
        return {"Error": "Invalid Signature"}
    if(not verifyBalance(tweet)): 
        return {"Error": "Invalid Balance"}
    setLastTweet(tweet['tokenId'])

    sendTweet(tweet['message'], tweet)
    return {"Success": "Hello Milady"}
    
def sendTweet(tweet, full):
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    client = tweepy.Client(consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token=access_token,
                        access_token_secret=access_token_secret)
    
    herWords = full['message']
    twitterResponse = ''
    if isDirty(herWords):
        speakNoEvil = cleanHerWords(herWords)
        print(f"speak no evil: {speakNoEvil}")
        twitterResponse = client.create_tweet(text=speakNoEvil)
        mongopw = os.getenv("mongopw")
        mongostring = f"mongodb://mongo:{mongopw}@containers-us-west-37.railway.app:8073"
        conn = pymongo.MongoClient(mongostring)
        db = conn['miladymumble']
        sheSaid = db['shesaid']
        insertSheSaid = {
            "tweet": tweet,
            "jsyk": "tweet key contains info about milady that sent that.",
            "created": time.time(),
            "twitterResponse": twitterResponse
        }
        saved = sheSaid.insert_one(insertSheSaid)
        return JSONResponse(content= jsonable_encoder({"milady": "mumbled", "saved": saved}))
    else: 
        twitterResponse = client.create_tweet(text=herWords)
        mongopw = os.getenv("mongopw")
        mongostring = f"mongodb://mongo:{mongopw}@containers-us-west-37.railway.app:8073"
        conn = pymongo.MongoClient(mongostring)        
        db = conn['miladymumble']
        sheSaid = db['shesaid']
        insertSheSaid = {
            "tweet": tweet,
            "jsyk": "tweet key contains info about milady that sent that.",
            "created": time.time(),
            "twitterResponse": twitterResponse
        }
        saved = sheSaid.insert_one(insertSheSaid)
        return JSONResponse(content= jsonable_encoder({"milady": "mumbled", "saved": saved}))

@app.get("/hello")
async def hello(request: Request):
    return "hello milady"

@app.get("/")
async def land(request: Request):
    return "hello milady"

class SheSaid(BaseModel):
    words: str

@app.post("/censoooor")
async def censoooor(request: Request, sheSaid: SheSaid):
    print(sheSaid.words)
    sheDirty = isDirty(sheSaid.words)
    print(f"is milady being rude? {isDirty(sheSaid.words)}")
    if sheDirty:
        speakNoEvil = cleanHerWords(sheSaid.words)
        print(f"speak no evil: {speakNoEvil}")
        return speakNoEvil
    else:
        return sheSaid

class CanShe(BaseModel):
    tokenIds: list

@app.post("/canshespeak")
async def canSheSpeak(request: Request, canShe: CanShe):
    print(canShe.tokenIds)
    store = pickledb.load('store.db', auto_dump=True)
    miladysCanTalks = []
    for tokenId in canShe.tokenIds:
        herLastWords = store.get(tokenId)
        secondsInADay = 86400
        if time.time() > herLastWords + secondsInADay: # a day in seconds
            miladysCanTalks.append(tokenId)
    output = jsonable_encoder({
        "tokenIds": miladysCanTalks
    })
    return JSONResponse(content=output)


@app.get("/censoooor", response_class=HTMLResponse)
async def censoooor(request: Request):
    words = request.query_params['words']
    print(words)
    sheDirty = isDirty(words)
    print(f"is milady being rude? {isDirty(words)}")
    
    if sheDirty:
        speakNoEvil = cleanHerWords(words)
        print(f"speak no evil: {speakNoEvil}")
        render =  f"""
            <html>
                <head>
                    <title>miladymumble</title>
                </head>
                <body>
                    <p>she said: {speakNoEvil}</p>
                </body>
            </html>
        """
        return render
    else:
        return words

@app.get("/censoooor/politepictures")
async def land(request: Request):
    out = ""
    for it in politePictures():
        out += it
    return out
