# C64 Chain — Node & Wallet

![C64 Chain](https://img.shields.io/badge/C64_Chain-v0.1-blue)

**C64 Chain** is a retro-themed CPU-mineable cryptocurrency, forked from [Wownero](https://github.com/wownero/wownero) (itself a fork of Monero).

It features a unique Commodore 64-inspired terminal interface with Datasette loading animations and classic C64 color schemes.

## Features

- 🖥️ **C64-themed ncurses TUI** built into the node binary — no external scripts needed
- ⛏️ **CPU-only mining** using RandomX (RandomWOW variant)
- 🔒 **Privacy by default** — CryptoNote protocol with ring signatures
- 💰 **2% dev fund** — automatically allocated from each block reward
- 🎮 **Datasette animation** on startup — press play on tape!
- ⏱️ **5-minute block time** (300 seconds)

## Quick Start

### Pre-compiled binaries (Ubuntu 24.04 x86_64)

Download from [Releases](../../releases):
- `c64chaind` — Node daemon with built-in TUI
- `c64wallet` — Wallet CLI with C64 interface

### Run the node
```bash
# Testnet
./c64chaind --testnet --data-dir=$HOME/.c64chain --rpc-bind-port=29641 --log-level=1

# Mainnet (when ready)
./c64chaind --data-dir=$HOME/.c64chain --rpc-bind-port=19641 --log-level=1
```

### Create a wallet
```bash
./c64wallet --testnet --daemon-address=127.0.0.1:29641 --generate-new-wallet=$HOME/.c64chain/mywallet
```

## Build from source

### Dependencies (Ubuntu 24.04)
```bash
sudo apt update
sudo apt install -y build-essential cmake pkg-config libboost-all-dev \
    libssl-dev libzmq3-dev libunbound-dev libsodium-dev libreadline-dev \
    libncurses5-dev libncursesw5-dev liblzma-dev libexpat1-dev \
    libpgm-dev qttools5-dev-tools libhidapi-dev libusb-1.0-0-dev \
    libprotobuf-dev protobuf-compiler libudev-dev
```

### Compile
```bash
git clone https://github.com/oxynaz/c64chain.git
cd c64chain
git submodule init && git submodule update
mkdir build && cd build
cmake ..
make -j$(nproc)
```

Binaries will be in `build/bin/`.

## Network

| Parameter | Value |
|-----------|-------|
| Algorithm | RandomX (RandomWOW) |
| Block time | 300 seconds (5 min) |
| Dev fund | 2% per block |
| P2P Port (mainnet) | 19640 |
| RPC Port (mainnet) | 19641 |
| P2P Port (testnet) | 29640 |
| RPC Port (testnet) | 29641 |

### Seed nodes

- `c64seed.ddns.net` (primary)
- `c64seed2.ddns.net` (secondary)

## Credits & License

C64 Chain is a fork of [Wownero](https://github.com/wownero/wownero), which is a fork of [Monero](https://github.com/monero-project/monero).

Licensed under the **GNU General Public License v3.0** — see [LICENSE](LICENSE).

The C64 Chain modifications include:
- Custom network IDs and genesis block
- Integrated ncurses TUI with C64 aesthetics
- 2% dev fund mechanism
- Rebranded binaries and messaging

All original Wownero and Monero copyrights remain intact.

## Donate

If you enjoy C64 Chain, consider mining with us! Every hash helps the network. 🕹️
