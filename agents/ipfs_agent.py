from fastapi import UploadFile, File, HTTPException
from torusdk.client import TorusClient
from torustrateinterface import Keypair
import requests

from core.base_agent import BaseAgent

class IPFSAgent(BaseAgent):
    def __init__(self, node_url: str, min_balance: int, pinata_api_key: str, pinata_secret_key: str):
        """
        IPFS Agent that uploads and pins files to Pinata, ensuring the user has sufficient balance or stake.
        """
        super().__init__(name="IPFS Agent", prefix="/ipfs")
        self.min_balance = min_balance
        self.pinata_headers = {
            "pinata_api_key": pinata_api_key,
            "pinata_secret_api_key": pinata_secret_key
        }
        self.torus_client = TorusClient(node_url)
        self._define_routes()
    
    def _define_routes(self):
        """Defines FastAPI routes."""
        @self.route("/upload_and_pin", methods=["POST"])
        async def upload_and_pin(address: str, mnemonic: str, stake: bool = False, file: UploadFile = File(...)):
            return await self._handle_upload_and_pin_request(address, file, mnemonic, stake)
    
    async def _handle_upload_and_pin_request(self, address: str, file: UploadFile, mnemonic: str, stake: bool):
        """Handles file upload and pinning based on balance or stake."""
        keypair = self._validate_keypair(mnemonic, address)
        balance = await self.get_balance(address, stake)
        if balance < self.min_balance:
            raise HTTPException(status_code=403, detail="Insufficient balance")
        return self._upload_and_pin_file(file, address)
    
    def _validate_keypair(self, mnemonic: str, key_addr: str):
        """Creates and validates the keypair."""
        try:
            keypair = Keypair.create_from_mnemonic(mnemonic)
            if keypair.ss58_address != key_addr:
                raise HTTPException(status_code=400, detail="Mnemonic does not match the provided address.")
            return keypair
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid mnemonic: {str(e)}")
    
    def _upload_and_pin_file(self, file: UploadFile, address: str):
        """Uploads and pins a file to Pinata."""
        try:
            files = {"file": (file.filename, file.file, file.content_type)}
            response = requests.post(
                "https://api.pinata.cloud/pinning/pinFileToIPFS",
                headers=self.pinata_headers,
                files=files
            )
            response.raise_for_status()
            pin_data = response.json()
            return {**pin_data, "pinned_by": address}
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_balance(self, address: str, stake: bool) -> int:
        return await self.get_staked_balance(address) if stake else await self.get_free_balance(address)

    async def get_staked_balance(self, address: str) -> int:
        res = self.torus_client.get_stakingto(address)
        return sum(res.values())
    
    async def get_free_balance(self, address: str) -> int:
        return self.torus_client.get_balance(address)
