# Quick Start Guide - Web3.py v7

## ⏱️ 5-Minute Setup

Get up and running with the upgraded AirdropFarm in 5 minutes.

## Prerequisites

- Python 3.9 or higher
- Git
- 5 minutes of your time

## Step 1: Clone & Setup (1 min)

```bash
# Clone repository
git clone https://github.com/BYNNAI/AirdropFarm.git
cd AirdropFarm

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 2: Configure (2 min)

```bash
# Copy environment template
cp .env.example .env

# Generate seed phrase
python main.py seed --generate

# Generate encryption key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Edit `.env` and add:**
```env
WALLET_SEED_MNEMONIC="your 24 word seed phrase here"
WALLET_ENCRYPTION_KEY="your_encryption_key_here"
TESTNET_MODE=true
```

## Step 3: Test (1 min)

```bash
# Run migration tests
python scripts/test_migration.py

# Create test wallets
python main.py create-wallets --count 5 --chains evm

# List wallets
python main.py list-wallets
```

## Step 4: Fund & Run (1 min)

```bash
# Fund wallets from faucets
python main.py fund-wallets --limit 5

# Check status
python main.py stats
```

## ✅ Done!

You're now running AirdropFarm with:
- ✅ Web3.py v7
- ✅ Latest security patches
- ✅ EIP-1559 support
- ✅ All protocol integrations updated

## Next Steps

### Scale Up

```bash
# Create more wallets
python main.py create-wallets --count 100

# Run eligibility actions
python main.py run-actions --action all

# Claim airdrops
python main.py claim-airdrops
```

### Monitor

```bash
# View stats
python main.py stats

# Check logs
tail -f logs/airdrop_farming.log

# List wallets with balances
python main.py list-wallets --limit 20
```

### Troubleshooting

If something goes wrong:

1. **Check Python version:**
   ```bash
   python --version  # Should be 3.9+
   ```

2. **Verify web3.py:**
   ```bash
   python -c "import web3; print(web3.__version__)"  # Should be 7.x
   ```

3. **Review logs:**
   ```bash
   tail -f logs/airdrop_farming.log
   ```

4. **Re-run tests:**
   ```bash
   python scripts/test_migration.py
   ```

## Common Issues

### "Module not found"

```bash
pip install -r requirements.txt --force-reinstall
```

### "No seed mnemonic configured"

```bash
# Generate new seed
python main.py seed --generate

# Add to .env
echo 'WALLET_SEED_MNEMONIC="your seed here"' >> .env
```

### "Transaction failed"

Check:
- Wallet has testnet ETH for gas
- RPC endpoint is working
- Chain is not congested

## Configuration Tips

### For Testing

```env
WALLET_COUNT=10
MAX_CONCURRENT_FAUCETS=3
MAX_CONCURRENT_ACTIONS=2
LOG_LEVEL=DEBUG
```

### For Production

```env
WALLET_COUNT=100
MAX_CONCURRENT_FAUCETS=10
MAX_CONCURRENT_ACTIONS=5
LOG_LEVEL=INFO

# Enable anti-detection
IP_SHARD_SIZE=10
FAUCET_SKIP_PROB=0.05
ACTION_SKIP_PROB=0.1
```

### For Maximum Safety

```env
TESTNET_MODE=true
WALLET_COUNT=50
OVER_COOLDOWN_JITTER_MAX=0.5
FAUCET_SKIP_PROB=0.15
OFF_DAYS=6
WEEKEND_ACTIVITY_REDUCTION=0.5
```

## Full Documentation

- `README.md` - Complete feature documentation
- `MIGRATION.md` - Web3.py v7 migration guide
- `UPGRADE_SUMMARY.md` - Summary of all changes
- `docs/WEB3_V7_CHANGES.md` - Detailed API reference

## Support

- Issues: https://github.com/BYNNAI/AirdropFarm/issues
- Documentation: https://github.com/BYNNAI/AirdropFarm
- Contact: [LinkTree](https://linktr.ee/oraclescript)

---

**Happy Farming! 🌱**
