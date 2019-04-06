# API 

## /api/limit_sell
## /api/limit_buy

user_id - address

signature - HMAC

market - str (ex:EUR/USD)

size - uint

price - uint

hash_signature - string

Return JSON:
```
{

    error -  string or null if ok

    result - string, order_id 

}
```

## /api/market_sell
## /api/market_buy

user_id - address

signature - HMAC

market - str (ex:EUR/USD)

size - uint

hash_signature - string

Return (JSON):
```
{

    error -  string or null if ok

    result - string, order_id 
}
```

## /api/order_list
user_id - address

signature - HMAC

Return (JSON)

error  - string or null of ok

result array of JSON:
```
{
    
    id - uint

    market - string

    size - uint
    
    price - uint
    
    type - int (1 - limit, 2 - market)
    
    side - int (-1 - sell, 1 - buy)
    
    status - int (0 - pendingnew, 1 - new, 2 -            rejected, 3 - cancelled, 4 - partially            filled, 5 - filled)

    filled - uint

    created_at - uint

    updated_at - uint 
}
```


## /api/get_trades

market - str (ex:EUR/USD)

from - from order id

Return (JSON):

error - string or null

result - trades array of JSON
```
{

    market : string

    timestamp  :  int
	
    size   : uint
    
    price  : uint
}
```


## /api/get_markets


Return (JSON):

error - string or null

result - markest array of JSON
```
{
    market : string (ex:EUR/USD)

    basesymbol : string (ex: USD)

    quotesymbol : string (ex: EUR)

    precision : uint (ex : 4)
}
```


## /api/get_symbols


Return (JSON):

error - string or null

result - markest array of JSON
```
{
    symbol : string (ex: EUR )

    precision : uint (ex : 4)
}
```