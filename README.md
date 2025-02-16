# Torus IPFS Agent

This project is a Torus agent that allows pinning files to IPFS (InterPlanetary File System) using Pinata. It's written in Python and utilizes the Torus SDK and Pinata API.

## Overview

The Torus IPFS Agent is a FastAPI-based application that provides an API for uploading and pinning files to IPFS through Pinata. It integrates with the Torus network to verify user balances or stakes before allowing file uploads.

## Features

- Upload and pin files to IPFS via Pinata
- Balance and stake checking using Torus SDK
- FastAPI-based RESTful API
- Modular agent architecture

## Components

1. `main.py`: The entry point of the application, setting up the FastAPI app and initializing the IPFS agent.
2. `core/base_agent.py`: Defines the `BaseAgent` class, which provides a foundation for creating modular agents with their own API routes.
3. `agents/ipfs_agent.py`: Implements the `IPFSAgent` class, which handles file uploads, pinning to IPFS, and balance checking.

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - `PINATA_API_KEY`: Your Pinata API key
   - `PINATA_API_SECRET`: Your Pinata API secret

3. Run the application:
   ```
   python main.py
   ```

## Usage

The main endpoint for uploading and pinning files is:

```
POST /ipfs/upload_and_pin
```

Parameters:
- `address`: The Torus address of the user
- `mnemonic`: The mnemonic phrase for the user's keypair
- `stake` (optional): Boolean flag to check staked balance instead of free balance
- `file`: The file to be uploaded and pinned

The agent will check the user's balance (or stake) before proceeding with the upload. If the balance is sufficient, the file will be uploaded to IPFS via Pinata and pinned.

## Dependencies

- FastAPI
- Torus SDK
- Pinata API
- Python-dotenv
- Uvicorn (for running the server)

## Note

This project is a backend service and does not include a frontend interface. It's designed to be integrated into larger systems or called via API requests.
