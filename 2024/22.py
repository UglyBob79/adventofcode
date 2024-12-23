#!/usr/bin/env python3

def iteration(secret):
    prune = 16777216 - 1

    # secret = ((secret * 64) ^ secret) ^ 16777216
    secret = ((secret << 6) ^ secret) & prune
    # secret = ((secret / 32) ^ secret) ^ 16777216
    secret = ((secret >> 5) ^ secret) & prune
    # secret = ((secret * 2048) ^ secret) ^ 16777216
    secret = ((secret << 11) ^ secret) & prune

    return secret

def map_prices(price_map, prices, diffs, index):
    n = 4

    for i in range(len(diffs) - n + 1):
        key = tuple(diffs[i:i + n])
        if key not in price_map:
            price_map[key] = {}
        # We only save the first match of each secret for each key
        if index not in price_map[key]:
            price_map[key][index] = prices[i + n]  # Add the next number to the dictionary

with open("22.input") as file:
    secrets = [int(line.strip()) for line in file]

    prices = []
    diffs = []
    price_map = {}

    for i in range(len(secrets)):
        prices.append([secrets[i] % 10])
        for n in range(2000):
            secrets[i] = iteration(secrets[i])
            prices[i].append(secrets[i] % 10)
        diffs.append([prices[i][j] - prices[i][j - 1] for j in range(1, len(prices[i]))])
        map_prices(price_map, prices[i], diffs[i], i)

    print(sum(secrets))

    best = 0
    for key, value in price_map.items():
        bananas = sum(value.values())
        if bananas > best:
            best = bananas

    print(best)