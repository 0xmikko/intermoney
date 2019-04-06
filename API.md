# API 

## /api/limit_sell
## /api/limit_buy

user_id - address

signature - HMAC

market - str (ex:EUR/USD)

size - decimal

price - float

hash_signature - string

Return:

error -  string or null if ok
result - string, order_id 



## /api/market_sell
## /api/market_buy

user_id - address

signature - HMAC

market - str (ex:EUR/USD)

size - decimal

hash_signature - string

Return (JSON):

error -  string or null if ok
result - string, order_id 


## /api/order_list
user_id - address

signature - HMAC

Return (JSON)
error  - string or null of ok
result array JSON:
{
    id - uint

    market - string

    size - decimal
    
    price - decimal
    
    type - int (1 - limit, 2 - market)
    
    side - int (-1 - sell, 1 - buy)
status - int (0 - pendingnew, 1 - new, 2 -            rejected, 3 - cancelled, 4 - partially            filled, 5 - filled)

    filled - decimal 

    created_at - uint

    updated_at - uint 
}


## /api/get_trades

market - str (ex:EUR/USD)

from - from order id

Return (JSON):

error - string or null
result - trades array JSON
{
	market : string
	timestamp  :  int
	size   : deciaml
    price  : decimal
}