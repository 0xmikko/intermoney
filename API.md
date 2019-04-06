# API 

## /api/limit_sell
## /api/limit_buy

user_id - address

signature - HMAC

market - str (ex:EUR/USD)

size - decimal

price - float

Return:

error -  string or null if ok
result - string, order_id 



## /api/market_sell
## /api/market_buy

user_id - address

signature - HMAC

market - str (ex:EUR/USD)

size - decimal

Return:

error -  string or null if ok
result - string, order_id 

