
# Getting started

Backend deployed on Heroku -> https://lit-hollows-59862.herokuapp.com/docs/ (please don't mind the safety warning from the browser)


## Considerations

I based myself on the principle of "just give what is needed", hence added as little properties on the resulting queries for swaps and pools as needed. This is easily modified by adapting the fragments in the GraphQL queries (see [queries.py](./queries.py)).

## Suggestions for improvement with more work

- Python clean-up
    - Clean up app.py, remove business logic from endpoints
    - Move GraphQL endpoint to .env file
    - Allow more results to be fetched (by default GraphQL limits to 100)
  
- GraphQL: 
  - Use OR clause for cleaner code (query on pools for given assetId)
  - Automatically aggregate data in the GraphQL querying stage instead of application stage
  - Auto-generate client instead of writing GraphQL queries by hand
  - Refactor duplicated fragments.

- Endpoints:
  - For increased user-friendliness, would suggest using human-readable timestamps instead of epoch.
  - When listing all assets, it would be more interesting to list the swap pairs instead of a simple list informing all swaps (since you can derive the latter from the former).