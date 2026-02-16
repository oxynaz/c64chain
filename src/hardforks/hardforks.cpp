// Copyright (c) 2014-2022, The Monero Project
// C64 CHAIN fork - all rights reserved under original BSD license
#include "hardforks.h"
#undef MONERO_DEFAULT_LOG_CATEGORY
#define MONERO_DEFAULT_LOG_CATEGORY "blockchain.hardforks"

// C64 CHAIN hard forks - all active from genesis
// HF17: RandomWOW
// HF18: fixed unlock time (288 blocks)
// HF19: tokenomics (19.64M supply, vesting 4x25%)
// HF20: LWMA-1 difficulty algorithm (block 2100)
const hardfork_t mainnet_hard_forks[] = {
  { 17, 0, 1, 1700000000 },
  { 18, 2, 1, 1700000001 },
  { 19, 3, 1, 1700000002 },
  { 20, 2100, 1, 1739739600 },
};
const size_t num_mainnet_hard_forks = sizeof(mainnet_hard_forks) / sizeof(mainnet_hard_forks[0]);
const uint64_t mainnet_hard_fork_version_1_till = 0;

const hardfork_t testnet_hard_forks[] = {
  { 17, 0, 1, 1700000000 },
  { 18, 2, 1, 1700000001 },
  { 19, 3, 1, 1700000002 },
  { 20, 2100, 1, 1739739600 },
};
const size_t num_testnet_hard_forks = sizeof(testnet_hard_forks) / sizeof(testnet_hard_forks[0]);
const uint64_t testnet_hard_fork_version_1_till = 0;

const hardfork_t stagenet_hard_forks[] = {
  { 17, 0, 1, 1700000000 },
  { 18, 2, 1, 1700000001 },
  { 19, 3, 1, 1700000002 },
  { 20, 2100, 1, 1739739600 },
};
const size_t num_stagenet_hard_forks = sizeof(stagenet_hard_forks) / sizeof(stagenet_hard_forks[0]);
