#!/bin/bash

# Função para verificar a disponibilidade de todos os nós
function check_all_nodes_available {
    local nodes=("$@")
    local all_available=true
    
    # Iterar sobre todos os nós
    for node in "${nodes[@]}"; do
        # Verificar se o nó está disponível
        if ! mongo --host "$node" --eval "db.runCommand({ ping: 1 })" &> /dev/null; then
            all_available=false
            break
        fi
    done
    
    # Retorna verdadeiro se todos os nós estiverem disponíveis, falso caso contrário
    $all_available
}

# Função para esperar que o MongoDB esteja pronto em todos os nós
function wait_for_mongodb {
    echo "Esperando o MongoDB iniciar..."
    # Lista de nós MongoDB
    mongodb_nodes=("mongos1" "mongos2")
    
    # Esperar até que todos os nós respondam positivamente
    until check_all_nodes_available "${mongodb_nodes[@]}"; do
        echo "$(date) - MongoDB não está disponível - dormindo"
        sleep 20
    done
    
    echo "MongoDB está ativo - executando o comando"
}

# Função para iniciar a simulação de falhas de rede
function start_network_failure_simulation {
    echo "Iniciando simulação de falha de rede..."
    python3 /app/ycsb-0.18.0/scripts/network_failures.py
}

# Adicionar atraso de 60 segundos antes de iniciar o script
echo "Aguardando 60 segundos antes de iniciar..."
sleep 60

# Esperar que o MongoDB esteja pronto em todos os nós
wait_for_mongodb

# Função para converter a saída para JSON
function start_convert_logs_json {
    echo "Starting convert logs to JSON"
    sleep 10
    wait $RUN_PID
    python3 /app/ycsb-0.18.0/convert_to_json.py
}

# Comandos de carga e execução do YCSB
LOAD_COMMAND="/app/ycsb-0.18.0/bin/ycsb.sh load mongodb -P workloads/workloada -s -P db.properties -p hosts=${MONGO_HOSTS} -p port=${MONGO_PORTS} -P replica.properties"
RUN_COMMAND="/app/ycsb-0.18.0/bin/ycsb.sh run mongodb -P workloads/workloada -s -P db.properties -p hosts=${MONGO_HOSTS} -p port=${MONGO_PORTS} -P replica.properties"

# Timestamp para nomear arquivos de saída
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Executar comando de carga do YCSB e iniciar simulação de falhas de rede após 20 segundos
echo "Iniciando carga YCSB em $TIMESTAMP"
$LOAD_COMMAND > /app/ycsb-0.18.0/results/load_$HOSTNAME-$TIMESTAMP.txt &
LOAD_PID=$!
sleep 20
start_network_failure_simulation &
wait $LOAD_PID

Executar comando de execução do YCSB e iniciar simulação de falhas de rede após 20 segundos
echo "Iniciando execução YCSB em $TIMESTAMP"
$RUN_COMMAND > /app/ycsb-0.18.0/results/run_$HOSTNAME-$TIMESTAMP.txt &
RUN_PID=$!
sleep 20
start_network_failure_simulation &
wait $RUN_PID

# Convertendo a saída para JSON
start_convert_logs_json

exit