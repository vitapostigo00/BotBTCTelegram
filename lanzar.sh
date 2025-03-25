source ./variables.sh
#Primero se lanzará la testnet ya que es más ligera y posteriormente la mainnet con un retraso ya que el acceso a disco es lento para cargar la mainnet, el tiempo está optimizado para un hdd externo de 5400rpm en una RPI5.
#PARTE TESTNET:
docker run --network testnet --name bitcoin_testnet -d -v /home/vita/discoGrande:/home/bitcoin/.bitcoin --rm -p 18332:18332 bitcoin/bitcoin -testnet=1 -txindex=1 -rpcbind=0.0.0.0 -rpcallowip=0.0.0.0/0 -zmqpubhashblock=tcp://0.0.0.0:8433 -rpcauth='testnet:70626c77b484d414f945fa9a24a42bf3$7882d3e04dd32609b99abef95e97f7ac201799c9880249ca7d68b15670319a5c';
sleep 50;
#Conexiones a fulcrum testnet en puerto 50002
docker run  --network testnet --name fulcrum_testnet -d -v /home/vita/discoSSD/Fullcrum/testnet:/data --rm -p 50002:50001 cculianu/fulcrum Fulcrum -u testnet -p $TESTNET_PASS -b bitcoin_testnet:18332;

#PARTE MAINNET
docker run --network mainnet --name bitcoin_mainnet -d -v /home/vita/discoGrande/mainnet:/home/bitcoin/.bitcoin --rm -p 8332:8332 bitcoin/bitcoin -txindex=1 -rpcbind=0.0.0.0 -rpcallowip=0.0.0.0/0 -zmqpubhashblock=tcp://0.0.0.0:8433 -rpcauth='mainnet:7093e4071b32228d44db26132978368b$16257d20a01a71e5ea19d2f5174524d28be1c08959fb100c86f92f7eacd768f5';
#La mainnet tarda más en cargar, es recomendable darle una pausa mayor.
sleep 120;
#Conexiones a fulcrum mainnet en puerto 50001 (por defecto, sin forwarding)
docker run --network mainnet --name fulcrum_mainnet -d -v /home/vita/discoSSD/Fullcrum/mainnet:/data --rm -p 50001:50001 cculianu/fulcrum Fulcrum -u mainnet -p $MAINNET_PASS -b bitcoin_mainnet:8332;

#Base de datos
docker run --name mongo_db  --rm  -d -v /home/vita/discoSSD/mongoDb:/data/db --network host mongo;