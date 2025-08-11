import logging
import socket
import threading


class MonitoringCenter:
    """
    Classe para criar e gerenciar um servidor TCP

    Attributes:
        host (str): Endereço do servidor
        port (int): Porta do servidor
        server_socket (socket.socket): Socket do servidor
    """

    def __init__(self, host="localhost", port=12000):
        """
        Inicializa o servidor com o endereço e a porta

        Args:
            host (str): Endereço do servidor
            port (int): Porta do servidor
        """

        self.host = host
        self.port = port
        self.logger = logging.getLogger()

        # Cria o socket do servidor utilizando TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Associa o socket ao endereço e porta
        self.server_socket.bind((self.host, self.port))

        # Coloca o servidor em modo de escuta para conexões
        self.server_socket.listen(1)

        message = (
            f"Servidor escutando em {self.server_socket.getsockname()[0]}:{self.port}"
        )

        # Log de inicialização do servidor
        logging.debug(message)
        print(message)

    def start(self):
        """
        Inicia o servidor para aceitar conexões de clientes de forma contínua

        Este método entra em um loop infinito aguardando conexões
        Para cada cliente conectado, chama o método handleConnection
        """

        print("Aguardando conexão de cliente...")

        # Loop que aguarda conexões de clientes
        while True:
            try:
                # Aceita uma nova conexão de cliente
                conn, addr = self.server_socket.accept()

                message = f"Conexão recebida de {addr[0]}:{addr[1]}"
                logging.debug(message)
                print(f"\033[32m{message}\033[0m")

                # Cria e inicia uma thread para lidar com cada cliente
                # handleConnection manipula a conexão recebida
                thread = threading.Thread(
                    target=self.handleConnection, args=(conn, addr)
                )
                thread.daemon = True
                thread.start()
            except KeyboardInterrupt:
                self.shutdown()
                break
            except Exception as e:
                message = f"Erro de conexão inesperado: {e}"
                logging.error(message)
                print(f"\033[31m{message}\033[0m")

    def handleConnection(self, conn, addr):
        """
        Manipula a conexão com o cliente conectado.

        Args:
            conn (socket.socket): Socket da conexão com o cliente
            addr (tuple): Endereço do cliente
        """

        try:
            while True:
                # Recebe dados do cliente até 1024 bytes
                data = conn.recv(1024)

                # Se não houver dados, encerra a conexão
                if not data:
                    break

                # Decodifica os dados recebidos
                data = data.decode()
                logging.debug(f"Dados recebidos de {addr[0]}:{addr[1]}: {data}")

                # Chama método para processar os dados do sensor
                response = self.handleSensor(data, addr)

                # Envia a resposta de volta ao cliente
                conn.sendall(response.encode())
                logging.debug(f"Resposta enviada para {addr[0]}:{addr[1]}: {response}")
                print(
                    f"Dado de temperatura do {addr[0]}:{addr[1]} recebidos, processado e respondido"
                )

        except Exception as e:
            message = f"Erro ao manipular conexão com {addr[0]}:{addr[1]}: {e}"
            logging.error(message)
            print(message)
        finally:
            # Fecha a conexão com o cliente
            conn.close()
            message = f"Conexão encerrada com {addr[0]}:{addr[1]}"
            logging.debug(message)
            print(f"\033[90m{message}\033[0m")

    def shutdown(self):
        """
        Encerra o servidor e fecha o socket
        """
        try:
            # Fecha o socket do servidor
            self.server_socket.close()
            message = "Servidor encerrado pelo usuário."
            logging.debug(message)
            print(f"\033[90m{message}\033[0m")

        except Exception as e:
            message = f"Erro ao fechar o socket: {e}"
            logging.error(message)
            print(f"\033[31m{message}\033[0m")

    def handleSensor(self, sensorData, addr):
        """
        Método para processar os dados recebidos de um sensor de temperatura

        Args:
            sensorData (str): Dados do sensor recebidos
            addr (tuple): Endereço do cliente
        """
        try:
            data = sensorData.split(",")
            sensorId = data[0]
            temperature = data[1]
            timestamp = data[2]

            # Verifica se a temperatura está fora do intervalo esperado
            if float(temperature) < 15:
                status = "Abaixo"
            elif float(temperature) > 35:
                status = "Acima"
            else:
                status = "Normal"

            logging.debug(f"Dados de {addr[0]}:{addr[1]} processados")

            return f"[{timestamp}] {sensorId} | {temperature}°C | {status}"
        except Exception as e:
            print(f"Erro ao processar dados do sensor: {e}")
            logging.error(f"Erro ao processar dados do sensor: {e}")
            return "Erro"


# Configuração do logging para gerar logs de depuração
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="./server/server_debug.log",
    filemode="w",
)

# Inicia o servidor se este arquivo for executado diretamente
if __name__ == "__main__":
    server = MonitoringCenter()
    server.start()
