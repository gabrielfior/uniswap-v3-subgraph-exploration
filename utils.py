from queries import QUERY_READ_SWAPS_FOR_BLOCK
from gql import gql, Client

def get_swaps(client: Client, block_number: int):
    query = gql(QUERY_READ_SWAPS_FOR_BLOCK)
    params = {"blockNumber": block_number}
    swaps_query_result = client.execute(query, variable_values=params)
    return swaps_query_result