import docker
import time
import random

def network_manipulation(client, node_name, action, duration=0, delay=None, loss=None):
    """
    Manipula a rede de um container Docker.

    Args:
    client (docker.DockerClient): Cliente Docker.
    node_name (str): Nome do container do node Cassandra.
    action (str): 'disconnect', 'delay', ou 'loss'.
    duration (int): Duração da ação em segundos.
    delay (str): Atraso para introduzir na rede, formato '1000ms'.
    loss (str): Porcentagem de perda de pacote, formato '30%'.
    """
    network_name = "mongo_net"
    try:
        network = client.networks.get(network_name)
        container = client.containers.get(node_name)

        if action == 'disconnect':
            print(f"Disconnecting {node_name} for {duration} seconds")
            network.disconnect(container)
            time.sleep(duration)
            network.connect(container)
            print(f"Reconnected {node_name}")

        elif action == 'delay':
            print(f"Adding delay of {delay} to {node_name} for {duration} seconds")
            command = f"tc qdisc add dev eth0 root netem delay {delay}"
            container.exec_run(cmd=command, privileged=True)
            time.sleep(duration)
            container.exec_run(cmd="tc qdisc del dev eth0 root netem", privileged=True)

        elif action == 'loss':
            print(f"Introducing packet loss of {loss} to {node_name} for {duration} seconds")
            command = f"tc qdisc add dev eth0 root netem loss {loss}"
            container.exec_run(cmd=command, privileged=True)
            time.sleep(duration)
            container.exec_run(cmd="tc qdisc del dev eth0 root netem", privileged=True)
        
    except docker.errors.NotFound as e:
        print(f"Error: {str(e)} - Network or container not found.")
    except docker.errors.APIError as e:
        print(f"API Error: {str(e)} - Check Docker daemon and network configurations.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        
def main():
    client = docker.from_env()
    nodes = ['mongos1', 'mongos2']
    actions = ['disconnect', 'delay', 'loss']
    settings = {
        'delay': '500ms',
        'loss': '3%'
    }

    while True:
        node_to_manipulate = random.choice(nodes)
        action = random.choice(actions)
        duration = random.randint(3, 6)  # Random duration between 5 and 10 seconds

        if action in settings:
            network_manipulation(client, node_to_manipulate, action, duration, settings[action])
        else:
            network_manipulation(client, node_to_manipulate, action, duration)

        print(f"Action {action} performed on {node_to_manipulate} for {duration} seconds")
        time.sleep(140)  # Wait for 1 minute before next action

if __name__ == "__main__":
    main()
