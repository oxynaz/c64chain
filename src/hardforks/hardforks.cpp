// Copyright (c) 2014-2022, The Monero Project
// C64 CHAIN fork - all rights reserved under original BSD license
#include "hardforks.h"
#undef MONERO_DEFAULT_LOG_CATEGORY
#define MONERO_DEFAULT_LOG_CATEGORY "blockchain.hardforks"

// C64 CHAIN hard forks
// HF17: genesis (RandomWOW, dynamic unlock)
// HF18: fixed unlock time (288 blocks)
const hardfork_t mainnet_hard_forks[] = {
  { 17, 1, 0, 1700000000 },
  { 18, 1300, 0, 1700000000 },
};
const size_t num_mainnet_hard_forks = sizeof(mainnet_hard_forks) / sizeof(mainnet_hard_forks[0]);
const uint64_t mainnet_hard_fork_version_1_till = 0;

const hardfork_t testnet_hard_forks[] = {
  { 17, 1, 0, 1700000000 },
  { 18, 1300, 0, 1700000000 },
};
const size_t num_testnet_hard_forks = sizeof(testnet_hard_forks) / sizeof(testnet_hard_forks[0]);
const uint64_t testnet_hard_fork_version_1_till = 0;

const hardfork_t stagenet_hard_forks[] = {
  { 17, 1, 0, 1700000000 },
  { 18, 1300, 0, 1700000000 },
};
const size_t num_stagenet_hard_forks = sizeof(stagenet_hard_forks) / sizeof(stagenet_hard_forks[0]);
