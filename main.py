from agents.balance_agent import BalanceAgent
from agents.ipfs_agent import IPFSAgent
from dotenv import load_dotenv
from fastapi import FastAPI
from torusdk.client import TorusClient
from torustrateinterface import Keypair
import os

app = FastAPI(title="Torus IPFS Agent API", description="")
load_dotenv()

NODE_URL = "wss://api.torus.network"
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_KEY = os.getenv("PINATA_API_SECRET")

MIN_BALANCE = 0

ipfs_agent = IPFSAgent(
    node_url=NODE_URL,
    min_balance=MIN_BALANCE,
    pinata_api_key=PINATA_API_KEY,
    pinata_secret_key=PINATA_SECRET_KEY
)

ipfs_agent.register_routes(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

