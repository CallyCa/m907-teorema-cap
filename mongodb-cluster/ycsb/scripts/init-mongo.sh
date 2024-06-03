#!/bin/bash

echo "Aguardando MongoDB iniciar..."

sleep 5

echo "Inicializando Replica Set do Config Server..."
docker exec -it configsvr1 mongosh --eval "rs.initiate({
  _id: 'rs-config',
  configsvr: true,
  members: [
    { _id: 0, host: 'configsvr1:27017' },
    { _id: 1, host: 'configsvr2:27017' },
    { _id: 2, host: 'configsvr3:27017' }
  ]
})"

sleep 5

echo "Inicializando Replica Set do Shard 1..."
docker exec -it mongo-shard1-1 mongosh --eval "rs.initiate({
  _id: 'shard1-rs',
  members: [
    { _id: 0, host: 'mongo-shard1-1:27017' },
    { _id: 1, host: 'mongo-shard1-2:27017' },
    { _id: 2, host: 'mongo-shard1-3:27017' }
  ]
})"

sleep 5

echo "Inicializando Replica Set do Shard 2..."
docker exec -it mongo-shard2-1 mongosh --eval "rs.initiate({
  _id: 'shard2-rs',
  members: [
    { _id: 0, host: 'mongo-shard2-1:27017' },
    { _id: 1, host: 'mongo-shard2-2:27017' },
    { _id: 2, host: 'mongo-shard2-3:27017' }
  ]
})"

sleep 5

echo "Adicionando Shards ao mongos..."
docker exec -it mongos1 mongosh --eval "sh.addShard('shard1-rs/mongo-shard1-1:27017,mongo-shard1-2:27017,mongo-shard1-3:27017')"
docker exec -it mongos1 mongosh --eval "sh.addShard('shard2-rs/mongo-shard2-1:27017,mongo-shard2-2:27017,mongo-shard2-3:27017')"

echo "Configuração de sharding concluída!"

sleep 5
echo "Criar Banco de Dados e Coleção"

docker exec -it mongos1 mongosh --eval "use ycsb"
docker exec -it mongos1 mongosh --eval "db.createCollection('usertable')"
docker exec -it mongos1 mongosh --eval "db.usertable.createIndex({ _id: 'hashed' })"
docker exec -it mongos1 mongosh --eval "sh.enableSharding('ycsb')"
docker exec -it mongos1 mongosh --eval "sh.shardCollection('ycsb.usertable', { _id: 'hashed' })"

sleep 5

echo "Verificar a lista de bancos de dados:"

docker exec -it mongos1 mongosh --eval "show dbs"

# sleep 5

# Limpeza da Coleção Antes de Executar os Benchmarks
# echo "Limpando a coleção 'usertable' antes de iniciar o benchmark..."
# docker exec -it mongos1 mongosh --eval "use ycsb; db.usertable.remove({})"

# sleep 10

# echo "Verificar a lista de coleções no banco de dados:"

# docker exec -it mongos1 mongosh --eval "use ycsb; show collections"

# sleep 10

# echo "Verificar se o sharding está habilitado para o banco de dados:"

# docker exec -it mongos1 mongosh --eval "sh.status()"