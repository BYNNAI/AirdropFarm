#!/usr/bin/env python3
"""
Migration test suite for web3.py v7 upgrade.

This script tests core functionality to ensure the migration was successful.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web3 import Web3
from eth_account import Account
import structlog

logger = structlog.get_logger()


class MigrationTests:
    """Test suite for web3.py v7 migration."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name):
        """Decorator for test functions."""
        def decorator(func):
            self.tests.append((name, func))
            return func
        return decorator
    
    def run(self):
        """Run all tests."""
        print("\n" + "="*60)
        print("Web3.py v7 Migration Test Suite")
        print("="*60 + "\n")
        
        for name, test_func in self.tests:
            try:
                print(f"Testing: {name}...", end=" ")
                test_func()
                print("\u2713 PASS")
                self.passed += 1
            except Exception as e:
                print(f"\u2717 FAIL")
                print(f"  Error: {str(e)}")
                self.failed += 1
        
        print("\n" + "="*60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("="*60 + "\n")
        
        return self.failed == 0


tests = MigrationTests()


@tests.test("Web3 module import")
def test_web3_import():
    """Test that web3 can be imported and version is correct."""
    import web3
    version = web3.__version__
    major_version = int(version.split('.')[0])
    assert major_version >= 7, f"Expected web3.py v7+, got v{version}"
    print(f"(v{version})", end=" ")


@tests.test("Web3 initialization")
def test_web3_init():
    """Test Web3 instance creation."""
    # Test with mock provider
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    assert w3 is not None
    assert hasattr(w3, 'eth')


@tests.test("Checksum address conversion")
def test_checksum_address():
    """Test Web3.to_checksum_address (v7 syntax)."""
    address = "0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed"
    checksummed = Web3.to_checksum_address(address.lower())
    assert checksummed == address


@tests.test("Wei conversion")
def test_wei_conversion():
    """Test Web3.to_wei and Web3.from_wei (v7 syntax)."""
    amount_eth = 1.5
    amount_wei = Web3.to_wei(amount_eth, 'ether')
    assert amount_wei == 1500000000000000000
    
    converted_back = float(Web3.from_wei(amount_wei, 'ether'))
    assert converted_back == amount_eth


@tests.test("Account creation")
def test_account_creation():
    """Test eth_account Account creation."""
    account = Account.create()
    assert account.address is not None
    assert account.key is not None
    assert len(account.address) == 42  # 0x + 40 hex chars


@tests.test("Transaction signing")
def test_transaction_signing():
    """Test transaction signing with eth_account."""
    account = Account.create()
    
    tx = {
        'to': '0x' + '00' * 20,
        'value': 1000000000000000000,
        'gas': 21000,
        'gasPrice': 1000000000,
        'nonce': 0,
        'chainId': 1
    }
    
    signed_tx = Account.sign_transaction(tx, account.key)
    assert signed_tx.raw_transaction is not None
    assert signed_tx.hash is not None


@tests.test("Method name changes")
def test_method_names():
    """Test that v7 method names are available."""
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    
    # Check that new snake_case methods exist
    assert hasattr(w3.eth, 'get_block')
    assert hasattr(w3.eth, 'get_balance')
    assert hasattr(w3.eth, 'get_transaction_count')
    assert hasattr(w3.eth, 'send_raw_transaction')
    assert hasattr(w3.eth, 'wait_for_transaction_receipt')


@tests.test("Solana library import")
def test_solana_import():
    """Test that solana libraries can be imported."""
    from solana.rpc.async_api import AsyncClient
    from solders.keypair import Keypair
    from solders.pubkey import Pubkey
    
    # Test keypair generation
    keypair = Keypair()
    assert keypair.pubkey() is not None


@tests.test("Cryptography library")
def test_cryptography():
    """Test cryptography library functionality."""
    from cryptography.fernet import Fernet
    
    # Test encryption/decryption
    key = Fernet.generate_key()
    f = Fernet(key)
    
    message = b"test message"
    encrypted = f.encrypt(message)
    decrypted = f.decrypt(encrypted)
    
    assert decrypted == message


@tests.test("Database libraries")
def test_database():
    """Test SQLAlchemy import."""
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    
    Base = declarative_base()
    
    class TestModel(Base):
        __tablename__ = 'test'
        id = Column(Integer, primary_key=True)
        name = Column(String)
    
    # Create in-memory database
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    
    assert True


@tests.test("HTTP libraries")
def test_http_libraries():
    """Test HTTP library imports."""
    import requests
    import aiohttp
    import httpx
    
    # Test that they can be instantiated
    session = requests.Session()
    assert session is not None


if __name__ == '__main__':
    success = tests.run()
    sys.exit(0 if success else 1)
