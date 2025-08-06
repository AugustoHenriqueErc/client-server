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

        # Cria o socket do servidor utilizando TCP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Associa o socket ao endereço e porta
        self.server_socket.bind((self.host, self.port))

        # Coloca o servidor em modo de escuta para conexões
        self.server_socket.listen(1)
        print(
            f"Servidor escutando em {self.server_socket.getsockname()[0]}:{self.port}"
        )

    def start(self):
        """
        Inicia o servidor para aceitar conexões de clientes de forma contínua

        Este método entra em um loop infinito aguardando conexões
        Para cada cliente conectado, chama o método handleConnection
        """

        # Loop que aguarda conexões de clientes
        while True:
            print("Aguardando conexão de cliente...")

            # Aceita uma nova conexão de cliente
            conn, addr = self.server_socket.accept()
            print(f"Conexão recebida de {addr[0]}:{addr[1]}")

            # Cria e inicia uma thread para lidar com cada cliente
            # handleConnection manipula a conexão recebida
            thread = threading.Thread(target=self.handleConnection, args=(conn, addr))
            thread.daemon = True
            thread.start()

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
                print(f"Dados recebidos de {addr[0]}:{addr[1]}: {data}")

                # Chama método para processar os dados do sensor
                response = self.handleSensor(data)

                # Envia a resposta de volta ao cliente
                conn.sendall(response.encode())
                print(f"Resposta enviada para {addr[0]}:{addr[1]}: {response}")
        except Exception as e:
            print(f"Erro ao manipular conexão com {addr[0]}:{addr[1]}: {e}")
        finally:
            # Fecha a conexão com o cliente
            conn.close()
            print(f"Conexão encerrada com {addr[0]}:{addr[1]}")

    def shutdown(self):
        """
        Encerra o servidor e fecha o socket
        """
        print("\nEncerrando o servidor...")

        try:
            # Fecha o socket do servidor
            self.server_socket.close()
            print("Servidor encerrado pelo usuário.")
        except Exception as e:
            print(f"Erro ao fechar o socket: {e}")

    def handleSensor(self, sensorData):
        """
        Método para processar os dados recebidos de um sensor de temperatura

        Args:
            sensorData (str): Dados do sensor recebidos
        """
        print("Processando dados do sensor...")

        # TODO: Implementar lógica de processamento dos dados do sensor
        # TODO: Retornar uma resposta adequada ao cliente

        # FIXME: Remover exemplo de resposta e retornar resposta real
        # Exemplo de resposta
        response = f"Informações do sensor: '{sensorData}'"
        return response


if __name__ == "__main__":
    server = MonitoringCenter()
    try:
        server.start()
    except KeyboardInterrupt:
        server.shutdown()
