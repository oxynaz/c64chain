# C64 Chain

![C64 Chain](https://img.shields.io/badge/C64_Chain-v0.3-blue)

**C64 Chain** is a privacy-focused, CPU-mineable cryptocurrency inspired by the Commodore 64.
Forked from [Wownero](https://codeberg.org/wownero/wownero) (itself a fork of Monero).

Features a unique Commodore 64-themed ncurses TUI with Datasette loading animation.

## ⚠️ Current Status: TESTNET

> **C64 Chain is currently in TESTNET phase.** The mainnet has not launched yet.
> All coins mined on testnet have no value and will be reset before mainnet launch.

## Features

- Commodore 64-themed ncurses TUI built into the node
- Datasette loading animation on startup
- CPU-only mining (RandomWOW algorithm)
- 2% dev fund for project development
- 5 minute block time
- Privacy by default (Monero-based)

## Quick Start

### 1. Install dependencies (Ubuntu 24.04 / Debian 12)
```bash
sudo apt update
sudo apt install -y build-essential cmake pkg-config libboost-all-dev libssl-dev \
    libzmq3-dev libsodium-dev libunwind-dev liblzma-dev libreadline-dev \
    libexpat1-dev libpgm-dev qttools5-dev-tools libhidapi-dev libusb-1.0-0-dev \
    libprotobuf-dev protobuf-compiler libudev-dev libncurses5-dev libncursesw5-dev libunbound-dev
```

### 2. Build the node and wallet
```bash
git clone https://github.com/oxynaz/c64chain.git
cd c64chain
mkdir build && cd build
cmake ..
make -j$(nproc)
```

This produces two binaries in `build/bin/`:
- `c64chaind` — the node daemon
- `c64wallet` — the wallet CLI

### 3. Run the node
```bash
cd ~/c64chain && screen -dmS node ./build/bin/c64chaind --testnet \
    --data-dir=$HOME/.c64chain --rpc-bind-port=29641 --log-level=1
```

View the TUI: `screen -r node` (detach with Ctrl+A then D)

The node will automatically connect to seed nodes and sync the blockchain.

### 4. Create a wallet
```bash
cd ~/c64chain && ./build/bin/c64wallet --testnet \
    --daemon-address=127.0.0.1:29641 \
    --generate-new-wallet=$HOME/.c64chain/mywallet
```

It will ask for a password. Save your wallet address (starts with 9...).

### 5. Open an existing wallet
```bash
cd ~/c64chain && ./build/bin/c64wallet --testnet \
    --daemon-address=127.0.0.1:29641 \
    --wallet-file=$HOME/.c64chain/mywallet
```

Useful wallet commands:
- `balance` — check your balance
- `address` — show your address
- `transfer ADDRESS AMOUNT` — send C64 coins
- `exit` — quit the wallet

### 6. Mine C64

See the [C64 Miner](https://github.com/oxynaz/c64miner) repository for mining instructions.

## Network Configuration

| Parameter | Testnet | Mainnet |
|-----------|---------|---------|
| P2P Port | 29640 | 19640 |
| RPC Port | 29641 | 19641 |
| Algorithm | RandomWOW | RandomWOW |
| Block time | 5 minutes | 5 minutes |
| Dev fund | 2% | 2% |

## Seed Nodes

- c64seed.ddns.net (163.172.215.129)
- c64seed2.ddns.net (51.158.152.121)

## Community

- Discord: [discord.gg/MTRgHT8r45](https://discord.gg/MTRgHT8r45)
- GitHub: [github.com/oxynaz](https://github.com/oxynaz)

## Credits & License

C64 Chain is a fork of [Wownero](https://codeberg.org/wownero/wownero), which is a fork of [Monero](https://github.com/monero-project/monero).

Licensed under the **GNU General Public License v3.0** — see [LICENSE](LICENSE).

All original Monero and Wownero copyrights remain intact.
