# INTERMONEY centralized liquidity exchange with trustless storage 

## Problematic
Fully decentralized exchanges (DEX) is a hot topic however there are many problems connected with decentrlized protocol. 
1) Matching operations are slow 
2) Each operations requires gas
3) Operation speed is limited to blockchain perfrormance
4) Front-running is possible 
5) Clients positions are visible

Centralized crypto currency exchanges have other set of problems leading to lack of trust from the clients:
1) Vulnerable to hackers attack leading to loose of the clients assets
2) Front-running and other fraudulent actions are possible 


## Task
Create the tokenized exchange facility missing all problem mentioned above and find some other advantages of combining decentralized assets storage technology and centralized matching engine.

## The structure
Meantime in a crypto space we see combining all functions of classic market in one place - the cryptocurrency exchange, however such structure leads to most of the problems mentioned above. If we take into account, we are building the insitutional grade facility dealing with tokenised assets, we see the following structure:

<b>Tokenization center</b>, the equivalent of clearign house for the stock market, central bank holding the register of accounts of other banks, in other words, this is real-world asstes storage dealing with tokenization and responsible for deposits and withdrawals of participants funds issuing tokens accoring to the value of asstes deposited to this faclity. The main difference is that this facility trust balances written in distrubited ledger records. 
Technically designed as a smart-contract that has permission to increase and decrease balances of traders. 


<b>Goverance center</b>, the equivalent of court in a real world that deals with disputes resolution. This is the part thac can deal with revertign transactions. 
Technically designed as a multisignature smart-contract that has permission to manage balances.


<b>Traders</b>, the equivalent of banks on the interbank market or traders, delaing with any kind of financial assets.
Techically is a private key that signs orders and blockchain transactions. 

<b>Exchange</b>, the analogue of old fashioned exchange, dealing with the orders and operates as a technical facility for fulfillment the trades within the system. 
Technically is a combination of matching engine and smart contract with the permission to increase or decrease balances only in case this transaction is confirmed by trader. 

<i>Please note, that broker, the entity that forwards orders to exchanges and provide clearing houses with the information about clients transactions to balances reconciliation is eliminated from this scheme. </i>

## Idea
Create technical solution that allows to perform trading of tokenized assets on mutual untrust principle however was governed and transparent for regulatory and couterparties.

## Entities 
<b>Assets</b> - tokenised assets, such as currencies, stocks or other financial instruments. Technically - ERC20-standard token with extended functionality. 

<b>Market</b> - a pair of assets, where the exchange rate is detemined by suppply and demand. Technically is a centralised place where buyers and sellers orders match. Please note, that such scheme allow one significat shift in nowadays technology, for example, it is possible to create pairs of for stocks eliminating spread, when buyers and seller want to to switch positions mtutually by changing one stock to another. 

<b>Balances</b> - a balance of the trader written in smart contract. Based on the value Tokenization center can withdraw funds from the system. This could be an amount of currency sent to bank account or stock transferred on balance of a broker.  

<b>Order</b> - the will of a trader to change one asset to another. There are market and limit orders supported by the system. Limit order provides a liquidity to the market when market order removes the liquidity exactly as it works on variety of classic markets nowadays. Techically orders is transferred as a set of parameters such as order type, size, side and price signed by traders private key to Exchange backend. This is not a blockchain transaction so no funds are required  

<b>Transfer order</b> - sending an assets from one trader to another without a trade. Must be sent in a form of "transfer" function call in ERC20 smart contract by specifying amount and recipients address. Such transactions can be done for bluring large positions, however doesn't guarantee impossibility of tracing. 

<b>Trade</b> -  a record that containg the information about buyer and seller orders and size of trade. Technically is a call to "Execute" function on matching smart contract and contacing information about trade parameters and order parameters signed by traders private keys. 

<b>Match</b> - when matching smart contract receives the trade information from the exchange's backend it checks integrity of orders parameters by validating the traders signature , then it checks if match parameters don't go against the interest of the traders and trade is done according to initial orders parameters, then it checks if the trade is not a duplicate by comparing nonce with nonce values in a smart contract and if total trade value doesn't overflow initial order value.  

## Technical implementation
<b>Exchnage backend</b> 
Python / Django / SQLLite - provides JSON/RPC interface for public and private endpoints. Process received orders from Frontend or can be accessed by algorithms through REST API. 

<b>Smart-contract interaction backend</b>
NodeJS - provides JSON/RPC interface for interacting with smart-contract. Receives matching and order information from exchange backend signs it with exchanges smart contract owner  private key and sends it to Ethereum blockchain. 

<b>Frontend</b>
React/Redux, provides trader with simple interface to interact with backend over REST API.

Uses Metamask to sign orders with traders private key.

Provides Level2 market depth informarmation, shows recent trades, last trade price. 

For authorized traders shows balances, orders, allows to send market or limit orders. 

![Intermoney exchange frontend](/images/frontend.jpg?raw=true "Intermoney exchnage Frontend")


<b>Tokenized asset smart-contract</b>
A standard ERC-20 token contract with alowance function. Existing or new contarcts can be added to the system. 

<b>Asset Interaction contract</b>
Contract holding traders balances accesible for trading. Each traded asset requires deployment new contract. Goverance interacts with the system through this contract. Freeze function should be added to guarantee presence of funds any moment, otherwise backed lister to contract events and remove orders if trader transfers funds from the account and cannot guarantee the execution. 


<b>Trade execution smart contarct</b>
Processes trades informaion received from backend and writes informaion to blockchain, makes sure orders are properly signed by owners and trades doesn't violate orders parameters. Signature gaurantees the order belongs to account owner, nonce value guarantees there will be no duplicated trades, blockchain order storage guarantees required order value is not overfilled.
If match is validated Asset Interaction contract is called to perfrom transaction between buyers and sellers account. 



## Workflow 
Trader enters order parameters and signes it with its private key over Metamask Google Chrome plugin. This is not a blockchain transaction but a SECP256K1 ECDSA signature of Keccak-256 hash of ABI encoded parameters. 

Signed orders is sent to exchange backend. Exchange backend assigns and returns global order number and puts order to unprocessed orders queue, where orders are sorder and executes simultaneously sorted by order number. 

Limit orders are provide liquidity, but if the price specified can match currently active orders, matching entine performs matching.  If order is not fully filled its status set to "PARTIALLY FILLED" and unfilled size is added to liquidity. 

Market order takes the liquidity until order size os fully filled. If there's not enough liquidity, order status is set to "FILLED" anyway.

Cancelling the order can be done in two ways : using exchange backend or by calling smart-contract directly. This guarantees that traders remain the full control over their funds, no matter if backend works or not. 

Result of matched orders is sent to smart contract along with signed parameters of both orders. Smart contract validates orders parameters and checks that the trade suits them. 

If validation was successful, smart contract exchange matched value of base asset and matched value multiplied to price of quote asset by calling "transfer" function of Assets smart contract. 

## Goverance and Mutual mistrust principle 

The protocol guarantees respect for the interests of all parties. 
From one side this is well goverened regulatory compliant solution, protecting funds by goverance and from another side it provides appropriate level of privacy for traders, allows keeping full control over the funds while perfoming exchange operations based on mututal mistrust priciple. 
<i>This is looking like the perfect middle between fully decentralized DEX and fully centralized cryptocurrency exchanges.</i>  



## Funds security
Total loss of funds is the main concern for institutional players that's why this is extrmely important to achieve better security of traders within the system. Since all traders are identified by private keys, key loose or compromentation should not lead to total loose of assets. 

<b>Risk of private key loose.</b> If there are no KYC or funds are stored on temporarty anonymous addresses and private key owner cannot confirm the ownership for such key we suggest to set backup private key by specifying an address agains current address for emergency funds withdrawal.   

<b>Risk of fraudulent actions.</b> In case the criminal activities lead to fraudulent transaction such addresses chould be blocked by goverance center for future investigation and reverting balances to initial state. Even in this case parties take exchange rate risk while the situation is in resolution phase it should be considered as a better options instead of total loss.  

<b>Human fault risk</b>. In case of the wrong action, such as specifying misproper receipient address, price or anything alse leading to funds get nowhere and cannot be accessed, the goverance center could take proper actions to eliminate the consequences. 


## Advanced features
Following features are a subject for more accurate studying:
<b>Additional privacy</b> - unlike DEX, centralised matching exchange gives great potential for improving the privacy. For example, matching transafers can be sent to addresses according to signed order parameters by matching engine smart contract masking the connection of multiple receipients to previous funds owner. Such balances can be accessed by private keys or masked by security codes those can be used for collecting funds on parent address when necessary.  

<b>Transparency for regulators and counterparties</b>. Matching is not a random algorithm and its result cannot be threated as something variable. DLT provides the exchange with opportunity to achieve full transaprency and become provable fair. Each order received by matching engine is assigned with order id, meantime order data signed by trader should be signed with previous hash and reported to blockchain. The exchange confirms this way all the orders are processed by predefined matching rules and all trades and funds transfer can be historicaly simulated. This process guarantees the protection agains front-running that cen be easily identified by regulatory and guarantees traders their orders are executed according to exchange's matching rules.

## Conclusion 
We should make maximum efforts to work out to understand fully all the potential profits and discover disadvantages and risks, however even on such a preliminary phase we see great potential for combining technology to achieve maixumum security, privacy and sustainability for traders. 

## Links

https://github.com/kataloo/DSXTContracts - Smart Contracts repository

https://github.com/kataloo/dsxt-sc-caller - Smart Contract interaction server repository

https://github.com/masquel/intermoney-front - InterMoney Exchange FrontEnd repository

https://github.com/MikaelLazarev/intermoney - InterMOney Exchange BackEnd repository (this one)

https://rinkeby.etherscan.io/address/0x1b1db1206837661f51e9b96a58a61f9f67b1c670 - link to Rinkeby deployed contract on Etherscan

http://intermoney.herokuapp.com/docs/ - backend API documentation





