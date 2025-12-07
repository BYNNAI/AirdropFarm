# Web3.py v7 Changes - Detailed Reference

## Overview

This document provides a comprehensive reference for all changes made during the web3.py v7 migration.

## Table of Contents

1. [Method Name Changes](#method-name-changes)
2. [Gas Price Updates](#gas-price-updates)
3. [Transaction Structure](#transaction-structure)
4. [Provider Changes](#provider-changes)
5. [Error Handling](#error-handling)
6. [Performance Improvements](#performance-improvements)
7. [Deprecated Features](#deprecated-features)

## Method Name Changes

### Ethereum JSON-RPC Methods

All camelCase methods have been renamed to snake_case:

| Old (v6) | New (v7) | Notes |
|----------|----------|-------|
| `eth.getBlock()` | `eth.get_block()` | Get block by number/hash |
| `eth.getBalance()` | `eth.get_balance()` | Get account balance |
| `eth.getTransactionCount()` | `eth.get_transaction_count()` | Get nonce |
| `eth.getTransaction()` | `eth.get_transaction()` | Get tx by hash |
| `eth.getTransactionReceipt()` | `eth.get_transaction_receipt()` | Get tx receipt |
| `eth.sendRawTransaction()` | `eth.send_raw_transaction()` | Send signed tx |
| `eth.sendTransaction()` | `eth.send_transaction()` | Send tx (requires unlocked account) |
| `eth.waitForTransactionReceipt()` | `eth.wait_for_transaction_receipt()` | Wait for confirmation |
| `eth.getCode()` | `eth.get_code()` | Get contract code |
| `eth.call()` | `eth.call()` | No change |
| `eth.estimateGas()` | `eth.estimate_gas()` | Estimate gas |

### Web3 Utility Methods

| Old (v6) | New (v7) | Notes |
|----------|----------|-------|
| `web3.toWei()` | `Web3.to_wei()` | Now static method |
| `web3.fromWei()` | `Web3.from_wei()` | Now static method |
| `web3.toChecksumAddress()` | `Web3.to_checksum_address()` | Now static method |
| `web3.toHex()` | `Web3.to_hex()` | Now static method |
| `web3.toBytes()` | `Web3.to_bytes()` | Now static method |

## Gas Price Updates

### EIP-1559 Transactions (Preferred)

```python
# Modern transaction with EIP-1559
tx = {
    'from': wallet_address,
    'to': recipient,
    'value': amount,
    'nonce': nonce,
    'gas': gas_limit,
    'maxFeePerGas': max_fee_per_gas,
    'maxPriorityFeePerGas': priority_fee,
    'type': '0x2',  # EIP-1559 transaction type
}
```

### Calculating EIP-1559 Fees

```python
# Get latest block to determine base fee
latest_block = web3.eth.get_block('latest')
base_fee = latest_block.get('baseFeePerGas', 0)

if base_fee > 0:
    # Chain supports EIP-1559
    max_priority_fee = Web3.to_wei(2, 'gwei')  # Tip to miner
    max_fee = (base_fee * 2) + max_priority_fee  # Max willing to pay
    
    tx_params = {
        'maxFeePerGas': max_fee,
        'maxPriorityFeePerGas': max_priority_fee,
        'type': '0x2',
    }
else:
    # Fallback to legacy
    tx_params = {
        'gasPrice': web3.eth.gas_price,
        'type': '0x0',
    }
```

### Legacy Transactions (Fallback)

```python
# Legacy transaction for chains without EIP-1559
tx = {
    'from': wallet_address,
    'to': recipient,
    'value': amount,
    'nonce': nonce,
    'gas': gas_limit,
    'gasPrice': web3.eth.gas_price,
    'type': '0x0',  # Legacy transaction type
}
```

## Transaction Structure

### Building Transactions

```python
# Contract interaction
contract = web3.eth.contract(address=contract_address, abi=abi)

# Build transaction with proper parameters
tx = contract.functions.someMethod(arg1, arg2).build_transaction({
    'from': wallet_address,
    'nonce': web3.eth.get_transaction_count(wallet_address),
    'gas': 200000,
    'maxFeePerGas': max_fee,
    'maxPriorityFeePerGas': priority_fee,
})

# Sign transaction
signed_tx = web3.eth.account.sign_transaction(tx, private_key)

# Send transaction
tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

# Wait for receipt
receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
```

### Transaction Receipt Structure

```python
receipt = {
    'transactionHash': HexBytes('0x...'),
    'transactionIndex': 0,
    'blockHash': HexBytes('0x...'),
    'blockNumber': 12345,
    'from': '0x...',
    'to': '0x...',
    'gasUsed': 21000,
    'cumulativeGasUsed': 21000,
    'contractAddress': None,  # or address if contract creation
    'logs': [],
    'status': 1,  # 1 = success, 0 = failure
    'effectiveGasPrice': 1000000000,
}
```

## Provider Changes

### HTTP Provider

```python
from web3 import Web3
from web3.providers import HTTPProvider

# Basic provider
web3 = Web3(HTTPProvider('https://rpc.example.com'))

# Provider with custom timeout and headers
from web3.providers import HTTPProvider
from web3.providers.rpc import HTTPProviderConfig

provider = HTTPProvider(
    'https://rpc.example.com',
    request_kwargs={
        'timeout': 60,
        'headers': {'User-Agent': 'AirdropFarm/2.1'}
    }
)
web3 = Web3(provider)
```

### WebSocket Provider

```python
from web3 import Web3
from web3.providers.websocket import WebSocketProvider

web3 = Web3(WebSocketProvider('wss://rpc.example.com'))
```

### IPC Provider

```python
from web3 import Web3
from web3.providers.ipc import IPCProvider

web3 = Web3(IPCProvider('/path/to/geth.ipc'))
```

## Error Handling

### Common Exceptions

```python
from web3.exceptions import (
    TransactionNotFound,
    TimeExhausted,
    ContractLogicError,
    InvalidAddress,
    BadFunctionCallOutput,
)

try:
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    
except TimeExhausted:
    logger.error("Transaction confirmation timeout")
    # Transaction may still be pending
    
except TransactionNotFound:
    logger.error("Transaction not found")
    # Transaction was not broadcast successfully
    
except ContractLogicError as e:
    logger.error(f"Contract reverted: {e}")
    # Smart contract reverted
    
except InvalidAddress:
    logger.error("Invalid Ethereum address")
    # Address format is invalid
```

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def send_transaction_with_retry(web3, signed_tx):
    """Send transaction with automatic retry."""
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        return receipt
    except Exception as e:
        logger.warning(f"Transaction failed, retrying: {e}")
        raise
```

## Performance Improvements

### Connection Pooling

Web3.py v7 includes improved connection pooling:

```python
import requests
from web3 import Web3
from web3.providers import HTTPProvider

# Create session with connection pooling
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(
    pool_connections=10,
    pool_maxsize=20,
)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Use session with provider
provider = HTTPProvider(
    'https://rpc.example.com',
    session=session
)
web3 = Web3(provider)
```

### Batch Requests

```python
# Batch multiple requests for better performance
from web3.batch_requests import batch_request

with batch_request(web3) as batch:
    balance1 = batch.eth.get_balance(address1)
    balance2 = batch.eth.get_balance(address2)
    block = batch.eth.get_block('latest')

# Results available after context exit
print(f"Balance 1: {balance1.result()}")
print(f"Balance 2: {balance2.result()}")
print(f"Block: {block.result()}")
```

## Deprecated Features

### Removed in v7

- `web3.eth.getBlock()` - Use `web3.eth.get_block()`
- `web3.toWei()` - Use `Web3.to_wei()` (static method)
- `web3.personal` module - Use external signers instead
- `web3.miner` module - Use external mining software

### Middleware Changes

```python
# Old middleware style (v6)
web3.middleware_onion.inject(some_middleware, layer=0)

# New middleware style (v7) - same API, better performance
web3.middleware_onion.add(some_middleware, layer=0)
```

## Additional Resources

- [Official Web3.py v7 Documentation](https://web3py.readthedocs.io/en/stable/)
- [Web3.py v7 Release Notes](https://web3py.readthedocs.io/en/stable/releases.html)
- [Web3.py GitHub Repository](https://github.com/ethereum/web3.py)
- [Ethereum JSON-RPC Specification](https://ethereum.github.io/execution-apis/api-documentation/)

## Testing Your Migration

Run the migration test suite:

```bash
python scripts/test_migration.py
```

Test with your specific workflows:

```bash
# Test wallet generation
python main.py create-wallets --count 5

# Test balance checking
python main.py list-wallets

# Test faucet automation
python main.py fund-wallets --limit 1
```
