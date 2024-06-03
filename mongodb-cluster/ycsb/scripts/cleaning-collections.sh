#!/bin/bash

sleep 5

# Limpeza da Coleção Antes de Executar os Benchmarks para RUN
echo "Criar Banco de Dados e Coleção"

docker exec -it mongos1 mongosh --eval "use ycsb"
docker exec -it mongos1 mongosh --eval "db.usertable.drop()"
docker exec -it mongos1 mongosh --eval "db.createCollection('usertable')"
docker exec -it mongos1 mongosh --eval "db.usertable.createIndex({ _id: 'hashed' })"
docker exec -it mongos1 mongosh --eval "sh.enableSharding('ycsb')"
docker exec -it mongos1 mongosh --eval "sh.shardCollection('ycsb.usertable', { _id: 'hashed' })"

sleep 2

echo "Verificar a lista de bancos de dados:"

docker exec -it mongos1 mongosh --eval "show dbs"