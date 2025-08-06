import socket
import time
import random
from datetime import datetime


class SensorClient:
    """
    Cliente que simula um sensor de temperatura

    A cada intervalo definido, gera um valor de temperatura aleatório
    (entre 10°C e 40°C por padrão), concatena com seu ID e timestamp,
    envia ao servidor e imprime a resposta recebida

    Attributes:
        sensorId (str): Identificador único deste sensor
        host (str): Endereço IP ou hostname do servidor
        port (int): Porta TCP do servidor
        interval (int): Tempo em segundos entre envios de leituras
    """

    def __init__(self, sensorId=None, host="localhost", port=12000, interval=15):
        """
        Inicializa o cliente sensor

        Args:
            sensorId (str): Identificador único do sensor
            host (str): Endereço do servidor
            port (int): Porta do servidor
            interval (int): Segundos entre leituras
        """

        self.sensorId = sensorId
        self.host = host
        self.port = port
        self.interval = interval

    def run(self):
        """
        Estabelece conexão TCP com o servidor e envia leituras em loop

        A cada iteração:
        1. Gera uma temperatura aleatória entre 10.00 e 40.00 °C
        2. Captura o timestamp atual
        3. Monta a mensagem "sensorId,temperatura,timestamp"
        4. Envia ao servidor e aguarda resposta
        5. Exibe no console:
            [DD/MM/AAAA HH:MM:SS] sensorId | temperatura °C | resposta do servidor
        6. Aguarda o intervalo definido antes de enviar a próxima leitura
        """

        # Cria o socket e garante fechamento automático ao sair do bloco
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Conecta ao servidor
            sock.connect((self.host, self.port))

            # Gera sensorId se não foi definido manualmente
            if self.sensorId is None:
                self.sensorId = f"sensor-{sock.getsockname()[1]}"
            try:
                while True:
                    # Gera temperatura simulada
                    temperature = round(random.uniform(10, 40), 2)

                    # Timestamp
                    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                    # Mensagem formatada
                    sensorData = f"{self.sensorId},{temperature},{timestamp}"

                    # Envia dados ao servidor
                    sock.sendall(sensorData.encode())

                    # Recebe resposta (até 1024 bytes)
                    response = sock.recv(1024).decode()

                    # Se não houver resposta, encerra conexão
                    if not response:
                        print(
                            f"\033[33m[{timestamp}] Conexão encerrada pelo servidor.\033[0m"
                        )
                        sock.close()
                        break

                    # Seta cor da mensagem baseado na resposta
                    if response.endswith("Abaixo"):
                        colorStatus = "\033[36m"  # Ciano
                    elif response.endswith("Acima"):
                        colorStatus = "\033[31m"  # Vermelho
                    else:
                        colorStatus = "\033[0m"  # padrão (sem cor)

                    # Exibe resposta no console
                    print(f"{colorStatus}{response}\033[0m")

                    # Aguarda próximo envio
                    time.sleep(self.interval)
            except KeyboardInterrupt:
                # Tratamento de encerramento pelo usuário
                print(
                    f"\n\033[33m[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {self.sensorId} encerrado pelo usuário.\033[0m"
                )


if __name__ == "__main__":
    # Inicialização automática:
    client = SensorClient()
    client.run()
