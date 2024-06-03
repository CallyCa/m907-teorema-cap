import os
import json

# Diretório de resultados absoluto
results_dir = '/app/ycsb-0.18.0/results'

# Certifique-se de que o diretório de resultados existe
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# Arquivos de log
load_logs = [os.path.join(results_dir, f) for f in os.listdir(results_dir) if f.startswith('load_') and f.endswith('.txt')]
run_logs = [os.path.join(results_dir, f) for f in os.listdir(results_dir) if f.startswith('run_') and f.endswith('.txt')]

# Caminhos dos arquivos JSON de saída
load_json_file_path = os.path.join(results_dir, 'load_logs.json')
run_json_file_path = os.path.join(results_dir, 'run_logs.json')

def parse_log_files(log_files, log_type):
    logs_data = {}
    
    for index, log_file_path in enumerate(log_files):
        if not os.path.isfile(log_file_path):
            print(f"Erro: O arquivo '{log_file_path}' não foi encontrado.")
            continue

        data = {
            "log_directory": None,
            "commands": [],
            "operations": [],
            "metrics": {}
        }

        with open(log_file_path, 'r') as file:
            lines = file.readlines()
            
            # Parse log directory creation
            if "Creating log directory..." in lines[0]:
                data["log_directory"] = lines[0].strip()
                lines = lines[1:]  # Remove a primeira linha

            # Parse commands
            if lines[0].startswith('/opt/java/openjdk/bin/java'):
                data["commands"].append(lines[0].strip())
                lines = lines[1:]  # Remove a linha de comando

            # Parse operations and metrics
            for line in lines:
                line = line.strip()
                if line.startswith('['):
                    metric_name = line.split('], ')[0][1:]
                    metric_values = line.split('], ')[1].split(', ')
                    if metric_name not in data["metrics"]:
                        data["metrics"][metric_name] = {}
                    data["metrics"][metric_name].update(dict(zip(metric_values[0::2], metric_values[1::2])))
                elif line and any(key in line for key in ["sec: ", "overall", "INSERT", "CLEANUP"]):
                    # Extraindo operações baseadas em "sec: "
                    if "sec: " in line:
                        parts = line.split(' sec: ')
                        timestamp = parts[0].strip()
                        remaining_parts = parts[1].split(';')
                        elapsed_time = remaining_parts[0].strip()
                        current_ops = remaining_parts[1].strip().split(' ')[0]
                        details = {}
                        if '[' in remaining_parts[-1]:
                            latency_info = remaining_parts[-1].split(' [')[1][:-1].split(' ')
                            if len(latency_info) % 2 == 0:  # Verifica se temos um número par de elementos
                                details.update({latency_info[i]: latency_info[i + 1] for i in range(0, len(latency_info), 2)})
                        details['current_ops'] = current_ops
                        data["operations"].append({
                            "timestamp": timestamp,
                            "elapsed_time": elapsed_time,
                            "details": details
                        })
                    # Extraindo operações e métricas finais
                    elif line.startswith('['):
                        metric_parts = line.split('], ')
                        metric_name = metric_parts[0][1:]
                        metric_values = metric_parts[1].split(', ')
                        if metric_name not in data["metrics"]:
                            data["metrics"][metric_name] = {}
                        data["metrics"][metric_name].update(dict(zip(metric_values[0::2], metric_values[1::2])))

        logs_data[f"{log_type}_RESULTADO_{index + 1}"] = {
            "log_file": log_file_path,
            "data": data
        }

    return logs_data

# Parse the load log files and convert to JSON
load_logs_data = parse_log_files(load_logs, 'LOAD')
with open(load_json_file_path, 'w') as json_file:
    json.dump(load_logs_data, json_file, indent=4)
print(f"Os arquivos de log de carga foram convertidos para {load_json_file_path}")

# Parse the run log files and convert to JSON
run_logs_data = parse_log_files(run_logs, 'RUN')
with open(run_json_file_path, 'w') as json_file:
    json.dump(run_logs_data, json_file, indent=4)
print(f"Os arquivos de log de execução foram convertidos para {run_json_file_path}")

print(f"Salvando arquivos JSON em: {results_dir}")
