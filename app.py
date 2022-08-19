import datetime
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from fastapi import FastAPI
from queries import *
from decimal import *
from utils import get_swaps
getcontext().prec = 18

app = FastAPI()
QUERY_ENDPOINT = 'https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v3-alt'
transport = AIOHTTPTransport(url=QUERY_ENDPOINT)
client = Client(transport=transport, fetch_schema_from_transport=True, execute_timeout=30)

@app.get("/")
def read_root():
    return {"curr_datetime": datetime.datetime.now()}

@app.get("/asset_id/{asset_id}/pools")
def read_pools_from_asset(asset_id: str):
    query = gql(QUERY_READ_POOLS_QUERY)
    params = {"assetId": asset_id.lower()}
    result = client.execute(query, variable_values=params)
    
    # merge two pools (token0 or token1 might equal assetId)
    all_pools = []
    for v in result.values():
        all_pools.extend(v)
    
    return {"pools": all_pools}

@app.get("/asset_id/{asset_id}/total_volume")
def read_total_volume_from_asset(asset_id: str, start: int, end: int):
    """ What is the total volume of that asset swapped in a given time range? """    
    query = gql(QUERY_READ_SWAPS_FOR_ASSET_ID_TIMESTAMP_BETWEEN)
    params = {"assetId": asset_id, "start": start, "end": end}
    swaps_query_result = client.execute(query, variable_values=params)

    # We use decimals in order to avoid floating point rounding problems.
    # We also set the precision to 18 digits (we take ETH as standard).
    total_volume = Decimal(0)
    for swap_list in swaps_query_result.values():
        for swap in swap_list:
            total_volume += Decimal(swap['amountUSD'])

    return {"total_volume_USD": total_volume}

@app.get("/block_number/{block_number}/swaps")
def read_swaps_by_block_number(block_number: int):
    """ What swaps occurred during that specific block? """
    # Note that int in Python is safe to use as it is automatically casted to long if needed.
    # (no need for BigInt).    
    swaps_query_result = get_swaps(client, block_number)
    return {"swaps": swaps_query_result['swaps']}

@app.get("/block_number/{block_number}/assets_swapped")
def read_swaps_by_block_number(block_number: int):
    """ List all assets swapped during that specific block """
    swaps_query_result = get_swaps(client, block_number)
    symbols = set()
    for swap in swaps_query_result['swaps']:
        token0, token1 = swap['token0']['symbol'], swap['token1']['symbol']
        symbols.update({token0, token1})
    
    return {"assets_swapped": symbols}
