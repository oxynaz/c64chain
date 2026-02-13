# C64 Chain

![C64 Chain](https://img.shields.io/badge/C64_Chain-v0.5.1-blue)

**C64 Chain** is a privacy-focused, CPU-mineable cryptocurrency inspired by the legendary Commodore 64.
Forked from [Wownero](https://codeberg.org/wownero/wownero) (itself a fork of Monero).

## ⚠️ Current Status: TESTNET

> **C64 Chain is currently in TESTNET phase.** The mainnet has not launched yet.
> Coins mined on testnet will be transferred to mainnet at a reduced ratio (details TBD).
> Early testnet miners will be rewarded for helping test the network.

## The C64 Spirit 🕹️

C64 Chain is built as a love letter to the Commodore 64, the best-selling home computer of all time. Every detail pays homage:

- **Node TUI**: Full ncurses Commodore 64 boot screen — blue border, PETSCII font, `**** C64 CHAIN NODE V0.1 ****` / `64K RAM SYSTEM  38911 BASIC BYTES FREE` / `READY.`
- **Datasette loading**: The node startup simulates a Datasette tape loading animation with colored bars, just like loading a game in 1984
- **BASIC-style display**: Node status displayed as `LIST` output with numbered lines, like a BASIC program
- **Max supply**: **19,640,000 C64** — 1964 is the year the MOS 6502 CPU was designed, the processor that powered the C64
- **Algorithm name**: `rx/c64` — RandomX variant customized for C64 Chain
- **Miner TUI**: The C64 Miner features its own Commodore 64-themed terminal with `READY.` / `RUN C64MINER` prompt

## Tokenomics

| Parameter | Value |
|-----------|-------|
| **Max supply** | **19,640,000 C64** |
| **Algorithm** | rx/c64 (RandomX variant, CPU-only) |
| **Block time** | 5 minutes (300 seconds) |
| **Initial block reward** | ~149 C64 |
| **Emission speed factor** | 21 |
| **50% mined in** | ~10 months |
| **80% mined in** | ~2 years |
| **96% mined in** | ~4 years |
| **Dev fund** | 2% of each block reward |
| **Emission curve** | Smooth exponential decay (no halving cliffs) |

The emission follows Monero's smooth curve formula: `reward = (supply_cap - already_mined) >> ESF`. This means block rewards decrease gradually with every block, unlike Bitcoin's sudden halvings. Combined with the 19.64M cap, this creates a fair and predictable monetary policy.

### Vesting (Anti-Dump Protection)

Every block reward is split into **4 equal outputs** with staggered unlock times. This prevents miners from dumping all rewards immediately at listing:

| Portion | Unlock after | Blocks |
|---------|-------------|--------|
| 25% | ~24 hours | 288 |
| 25% | ~30 days | 8,640 |
| 25% | ~60 days | 17,280 |
| 25% | ~90 days | 25,920 |

The 2% dev fund unlocks after ~24 hours (288 blocks).

Each coinbase transaction has **5 outputs**: 4 vesting outputs for the miner + 1 dev fund output. This is enforced at consensus level — blocks without proper vesting are rejected by the network.

### Why Vesting Matters

Without vesting, early miners could accumulate large amounts of C64 and dump them as soon as the coin is listed on exchanges, crashing the price for everyone. The 90-day staggered unlock ensures that selling pressure is distributed over time, protecting the coin's value for all participants.

## Features

- 🖥️ Commodore 64-themed ncurses TUI built into the node
- 📼 Datasette loading animation on startup
- ⛏️ CPU-only mining (rx/c64 algorithm, RandomX variant)
- 💰 2% dev fund for project development
- ⏱️ 5 minute block time
- 🔒 Vesting on block rewards (4×25% staggered unlock over 90 days)
- 🕶️ Privacy by default (Monero/CryptoNote-based)
- 🚫 No premine, no ICO, no VC funding

## Quick Start

### Option A: Pre-compiled binaries (Ubuntu 24.04 x86_64)

Download from [Releases](https://github.com/oxynaz/c64chain/releases/tag/v0.5.1):
```bash
wget https://github.com/oxynaz/c64chain/releases/download/v0.5.1/c64chain-v0.5.1-ubuntu24-x86_64.tar.gz
tar xzf c64chain-v0.5.1-ubuntu24-x86_64.tar.gz
chmod +x c64chaind c64wallet c64chain-wallet-rpc
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

This produces binaries in `build/bin/`:
- `c64chaind` — the node daemon
- `c64wallet` — the wallet CLI
- `c64chain-wallet-rpc` — wallet RPC server (for exchange/pool integration)

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

It will ask for a password. **Save your wallet address** (starts with `9...`) and your **seed phrase** (25 words). You will need the address to configure the miner.

## Open an existing wallet
```bash
./c64wallet --testnet --daemon-address=127.0.0.1:29641 --wallet-file=$HOME/.c64chain/mywallet
```

Useful wallet commands:
- `balance` — check your balance (shows locked/unlocked due to vesting)
- `address` — show your address
- `transfer ADDRESS AMOUNT` — send C64 coins
- `seed` — display your recovery seed phrase
- `exit` — quit the wallet

## Mine C64

Download the miner from [C64 Miner Releases](https://github.com/oxynaz/c64miner/releases/tag/v0.2.1), or build from [source](https://github.com/oxynaz/c64miner).

Create a `config.json`:
```json
{
    "autosave": false,
    "donate-level": 0,
    "cpu": { "enabled": true },
    "opencl": false,
    "cuda": false,
    "pools": [{
        "url": "127.0.0.1:29641",
        "user": "YOUR_C64_WALLET_ADDRESS_HERE",
        "algo": "rx/c64",
        "coin": "c64chain",
        "daemon": true,
        "daemon-poll-interval": 1000
    }],
    "print-time": 5
}
```

> ⚠️ `"daemon": true` and `"coin": "c64chain"` are **required**.

Run the miner:
```bash
sudo ./c64miner -c config.json -t $(nproc)
```

Always run with `sudo` for best performance (huge pages). The miner features a Commodore 64-themed TUI showing hashrate, accepted blocks, and live mining logs.

## Network Configuration

| Parameter | Testnet | Mainnet |
|-----------|---------|---------|
| P2P Port | 29640 | 19640 |
| RPC Port | 29641 | 19641 |
| Algorithm | rx/c64 | rx/c64 |
| Block time | 5 minutes | 5 minutes |
| Max supply | 19,640,000 | 19,640,000 |
| Dev fund | 2% | 2% |

## Seed Nodes

4 seed nodes are hardcoded in the node binary. Your node will automatically discover and connect to them.

## Block Explorer

- **[c64chain.com](https://c64chain.com)** — search blocks, transactions, network stats

## Downloads

| Component | Binary | Source |
|-----------|--------|--------|
| Node + Wallet | [v0.5.1 Release](https://github.com/oxynaz/c64chain/releases/tag/v0.5.1) | [oxynaz/c64chain](https://github.com/oxynaz/c64chain) |
| Miner | [v0.2.1 Release](https://github.com/oxynaz/c64miner/releases/tag/v0.2.1) | [oxynaz/c64miner](https://github.com/oxynaz/c64miner) |

## Community

- Discord: [discord.gg/MTRgHT8r45](https://discord.gg/MTRgHT8r45)
- GitHub: [github.com/oxynaz](https://github.com/oxynaz)
- Block Explorer: [c64chain.com](https://c64chain.com)

## Credits & License

C64 Chain is a fork of [Wownero](https://codeberg.org/wownero/wownero), which is a fork of [Monero](https://github.com/monero-project/monero).

Licensed under the **GNU General Public License v3.0** — see [LICENSE](LICENSE).

All original Monero and Wownero copyrights remain intact.
