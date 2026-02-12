# C64 Chain

![C64 Chain](https://img.shields.io/badge/C64_Chain-v0.4-blue)

**C64 Chain** is a privacy-focused, CPU-mineable cryptocurrency inspired by the Commodore 64.
Forked from [Wownero](https://codeberg.org/wownero/wownero) (itself a fork of Monero).

Features a unique Commodore 64-themed ncurses TUI with Datasette loading animation.

## ⚠️ Current Status: TESTNET

> **C64 Chain is currently in TESTNET phase.** The mainnet has not launched yet.
> Coins mined on testnet will be transferred to mainnet at a reduced ratio (details TBD).
> Early testnet miners will be rewarded for helping test the network.

## Features

- Commodore 64-themed ncurses TUI built into the node
- Datasette loading animation on startup
- CPU-only mining (rx/c64 algorithm)
- 2% dev fund for project development
- 5 minute block time
- Privacy by default (Monero-based)

## Quick Start

### Option A: Pre-compiled binaries (Ubuntu 24.04 x86_64)

Download from [Releases](https://github.com/oxynaz/c64chain/releases/tag/v0.4):
```bash
wget https://github.com/oxynaz/c64chain/releases/download/v0.4/c64chain-v0.4-ubuntu24-x86_64.tar.gz
tar xzf c64chain-v0.4-ubuntu24-x86_64.tar.gz
mkdir -p ~/c64chain/build/bin
mv c64chaind c64wallet ~/c64chain/build/bin/
```

### Option B: Build from source

#### 1. Install dependencies (Ubuntu 24.04 / Debian 12)
```bash
sudo apt update
sudo apt install -y build-essential cmake pkg-config libboost-all-dev libssl-dev \
    libzmq3-dev libsodium-dev libunwind-dev liblzma-dev libreadline-dev \
    libexpat1-dev libpgm-dev qttools5-dev-tools libhidapi-dev libusb-1.0-0-dev \
    libprotobuf-dev protobuf-compiler libudev-dev libncurses5-dev libncursesw5-dev \
    libunbound-dev liblmdb-dev libminiupnpc-dev
```

#### 2. Build the node and wallet
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

## Run the node
```bash
./c64chaind --testnet --data-dir=$HOME/.c64chain --rpc-bind-port=29641 --log-level=1
```

The node will automatically connect to seed nodes and sync the blockchain.

> **Tip:** Use `screen` to run in background: `screen -dmS node ./c64chaind --testnet --data-dir=$HOME/.c64chain --rpc-bind-port=29641 --log-level=1`
> View the TUI: `screen -r node` (detach with Ctrl+A then D)

## Create a wallet

> ⚠️ **You need a wallet address before you can mine.** Follow this step first.
```bash
./c64wallet --testnet --daemon-address=127.0.0.1:29641 --generate-new-wallet=$HOME/.c64chain/mywallet
```

It will ask for a password. **Save your wallet address** (starts with `9...`). You will need it to configure the miner.

## Open an existing wallet
```bash
./c64wallet --testnet --daemon-address=127.0.0.1:29641 --wallet-file=$HOME/.c64chain/mywallet
```

Useful wallet commands:
- `balance` — check your balance
- `address` — show your address
- `transfer ADDRESS AMOUNT` — send C64 coins
- `exit` — quit the wallet

## Mine C64

Download and build the miner from [C64 Miner](https://github.com/oxynaz/c64miner), or download the pre-compiled binary from [Miner Releases](https://github.com/oxynaz/c64miner/releases/tag/v0.2).

Create a `config.json` in `~/c64miner/`:
```json
{
    "autosave": false,
    "donate-level": 0,
    "cpu": {
        "enabled": true
    },
    "opencl": false,
    "cuda": false,
    "pools": [
        {
            "url": "127.0.0.1:29641",
            "user": "YOUR_C64_WALLET_ADDRESS_HERE",
            "algo": "rx/c64",
            "coin": "c64chain",
            "daemon": true,
            "daemon-poll-interval": 1000
        }
    ],
    "print-time": 5
}
```

> ⚠️ `"daemon": true` and `"coin": "c64chain"` are **required**. See the [C64 Miner README](https://github.com/oxynaz/c64miner) for full configuration details.

Run the miner:
```bash
sudo ./c64miner -c config.json -t 2
```

Replace `-t 2` with the number of CPU threads to use (leave 1-2 for system). Always run with `sudo` for best performance (huge pages).

## Network Configuration

| Parameter | Testnet | Mainnet |
|-----------|---------|---------|
| P2P Port | 29640 | 19640 |
| RPC Port | 29641 | 19641 |
| Algorithm | rx/c64 | rx/c64 |
| Block time | 5 minutes | 5 minutes |
| Dev fund | 2% | 2% |

## Seed Nodes

- c64seed.ddns.net (163.172.215.129)
- c64seed2.ddns.net (51.158.152.121)

## Block Explorer

- **[c64chain.com](https://c64chain.com)** — search blocks, transactions, network stats

## Downloads

| Component | Binary | Source |
|-----------|--------|--------|
| Node + Wallet | [v0.4 Release](https://github.com/oxynaz/c64chain/releases/tag/v0.4) | [oxynaz/c64chain](https://github.com/oxynaz/c64chain) |
| Miner | [v0.2 Release](https://github.com/oxynaz/c64miner/releases/tag/v0.2) | [oxynaz/c64miner](https://github.com/oxynaz/c64miner) |

## Community

- Discord: [discord.gg/MTRgHT8r45](https://discord.gg/MTRgHT8r45)
- GitHub: [github.com/oxynaz](https://github.com/oxynaz)
- Block Explorer: [c64chain.com](https://c64chain.com)

## Credits & License

C64 Chain is a fork of [Wownero](https://codeberg.org/wownero/wownero), which is a fork of [Monero](https://github.com/monero-project/monero).

Licensed under the **GNU General Public License v3.0** — see [LICENSE](LICENSE).

All original Monero and Wownero copyrights remain intact.
