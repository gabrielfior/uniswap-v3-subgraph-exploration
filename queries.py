QUERY_READ_POOLS_QUERY = """
    query ($assetId: ID!) {
  data_token0: pools(where: {token0_: {id: $assetId}}) {
    ...PoolFragment
  }
  data_token1: pools(where: {token1_: {id: $assetId}}) {
    ...PoolFragment
  }
}

fragment TokenFragment on Token {
  id
  symbol
}

fragment PoolFragment on Pool {
    id
    token0 {
      ...TokenFragment
    }
    token1 {
      ...TokenFragment
    }
}
"""

QUERY_READ_SWAPS_FOR_ASSET_ID_TIMESTAMP_BETWEEN = """
    query ($assetId: ID!, $start: BigInt!, $end: BigInt!) {
  data_token0: swaps(where: {token0_: {
    id: $assetId}, 
      timestamp_gte: $start
      timestamp_lte: $end
  }) {
    ...SwapFragment
  }
 data_token1: swaps(where: {token1_: {
    id: $assetId}, 
      timestamp_gte: $start
      timestamp_lte: $end
  }) {
    ...SwapFragment
  }
}

fragment TokenFragment on Token {
  id
  symbol
}

fragment SwapFragment on Swap {
    amountUSD
    token0 {
      ...TokenFragment
    }
    token1 {
      ...TokenFragment
    }
}
"""

QUERY_READ_SWAPS_FOR_BLOCK = """
query ($blockNumber: BigInt!) {
  swaps(where: {
    transaction_: {blockNumber: $blockNumber}}) {
    ...SwapFragment
  }
}

fragment TokenFragment on Token {
  id
  symbol
}
fragment SwapFragment on Swap {
    amountUSD
    token0 {
      ...TokenFragment
    }
    token1 {
      ...TokenFragment
    }
}
"""