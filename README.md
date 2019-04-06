# INTERMONEY centralized liquidity exchange with trustless storage 

## Problematic
Fully decentralized exchanges (DEX) is a hot topic however there are many problems connected with decentrlized protocol. 
1) Matching operations are slow 
2) Each operations requires gas
3) Operation speed is limited to blockchain perfrormance
4) Frontrunning is possible 
5) Clients positions are visible

Centralized crypto currency exchanges have other set of problems leading to lack of trust from the clients:
1) Vulnerable to hackers attack leading to loose of the clients assets
2) Frontrunning and other fraudulent actions are possible 


## Task
Create the tokenized exchange facility missing all problem mentioned above and find some other advantages of combining decentralized assets storage technology and centralized matching engine

## The structure
Meantime in a crypto space we see combining all functions of classic market in one place - the cryptocurrency exchange, however such structure leads to most of the problems mentioned above. If we take into account, we are workign on insitutional grade facility working with tokenised assets, we see the following structure:

<b>Tokenization center</b>, the equivalent of clearign house for the stock market, central bank holding the register of accounts of other banks, in other words, this is real-world asstes storage delaing with tokenization and responsible for deposits and withdrawals of participants funds issuing tokens accoring to the value of asstes deposited to this faclity. The main difference is that this facility trust balances written in distrubited ledger records. 
Technically designed as a smart-contract that has permission to increase and decrease balances of traders. 


<b>Goverance center</b>, the equivalent of court in a real works that deals with disputes resolution. This is the part thac can deal with revertign transactions. 
Technically designed as a multisignature smart-contract that permission to add and remove funds from accounts.  


<b>Traders</b>, the equivalaent of banks on the interbank market or traders, delaing with any kind of financial assets.
Techically is a private key that signs orders and blockchain transactions. 

<b>Exchange</b>, the analogue of old fashioned exchange, dealing with the orders of traders and acting as a technical facility for fulfillment the trades within the system. 
Technically is a set of matching engine,  smart contract with the permission to increase or decrease balances only in case this transaction is confirmed by trader. 

<i>Please note, that broker, the entity that forwards orders to exchanges and provide clearing houses with the information about clients transactions to balances reconciliation is eliminated from this scheme. </i>

## Entities 
<b>Assets</b> - tokenised assets, such as currencies, stocks or other financial instruments. Technically - ERC20-standard token with extended functionality. 

<b>Market</b> - a pair of assets, where the exchange rate is detemined by suppply and demand. Technically is a centralised place where buyers and sellers orders match. Please note, that such scheme allow one significat shift in nowadays technology, for example, it is possible to create pairs of for stocks eliminating spread, when buyers and seller want to to switch positions mtutually by changing one stock to another. 

<b>Balances</b> - a balance of the trader written in smart contract. Based on the value Tokenization center can withdraw funds from the system. This could be an amount of currency sent to bank account or stock transferred on balance of a broker.  

<b>Order</b> - the will of a trader to change one asset to another. There are market and limit orders supported by the system. Limit order provides a liquidity to the market when market order removes the liquidity exactly as it works on variety of classic markets nowadays. Techically orders is transferred as a set of parameters such as order type, size, side and price signed by traders private key to Exchange backend. This is not a blockchain transaction so no funds are required  

<b>Transfer order</b> - sending an assets from one trader to another without a trade. Must be sent in a form of "transfer" function call in ERC20 smart contract by specifying amount and recipients address. Such transactions can be done for bluring large positions, however doesn't guarantee impossibility of tracing. 

<b>Trade</b> -  a record that containg the information about buyer and seller orders and size of trade. Technically is a call to "Execute" function on matching smart contract and contacing information about trade parameters and order parameters signed by traders private keys. 

<b>Match</b> - when matching smart contract receives the trade information from the exchange's backend it checks integrity of orders parameters by validating the traders signature , then it checks if match parameters don't go against the interest of the traders and trade is done according to initial orders parameters, then it checks if the trade is not a duplicate by comparing nonce with nonce values in a smart contract and if total trade value doesn't overflow initial order value.  

## Possibilities 
Those fetures are a subject for more accurate studying:
<b>Additional privacy</b> - unlike DEX, centralised matching exchange gives great potential for improving the privacy. For example, matching transafers can be sent to addresses according to signed order parameters by matching engine smart contract masking the connection of multiple receipients to previous funds owner. Such balances can be accessed by private keys or masked by security codes those can be used for collecting funds on parent address when necessary.  

## Funds security
Total loss of funds is the main concern for institutional players that's why this is extrmely important to achieve better security of traders within the system. Since all traders are identified by private keys, key loose or compromentation should not lead to total loose of assets. 

<b>Risk of private key loose.</b> If there are no KYC or funds are stored on temporarty anonymous addresses and private key owner cannot confirm the ownership for such key we suggest to set backup private key by specifying an address agains current address for emergency funds withdrawal.   

<b>Risk of fraudulent actions.</b> In case the criminal activities lead to fraudulent transaction such addresses chould be blocked by goverance center for future investigation and reverting balances to initial state. Even in this case parties take exchange rate risk while the situation is in resolution phase it should be considered as a better options instead of total loss.  

<b>Risk error</b>. In case of the wrong action, such as specifying misproper receipient address, price or anything alse leading to funds get nowhere and cannot be accessed, the goverance center could take proper actions to eliminate the consequences. 

## Conclusion 
We should make maximum efforts to work out to understand fully all the potential profits and discover disadvantages and risks, however even on such a preliminary phase we see great potential for combining technology to achieve maixumum security, privacy and sustainability for traders. 

