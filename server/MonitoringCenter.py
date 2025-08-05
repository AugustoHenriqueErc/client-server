import socket


class MonitoringCenter:
    """
    Classe para criar e gerenciar um servidor TCP

    Attributes:
        host (str): Endereço do servidor
        port (int): Porta do servidor
        server_socket (socket.socket): Socket do servidor
    """

    def __init__(self, host="127.0.0.1", port=12000):
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
        print(f"Servidor escutando em {self.host}:{self.port}")

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
            print(f"Conexão recebida de {addr}")

            # Manipula a conexão recebida
            self.handleConnection(conn, addr)

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
                print(f"Dados recebidos de {addr}: {data}")

                # TODO: Chamar o método para processar os dados recebidos

                # FIXME: Remover este exemplo
                # Exemplo de processamento: converte para maiúsculas
                response = data.upper()
                conn.sendall(response.encode())
        except Exception as e:
            print(f"Erro ao manipular conexão com {addr}: {e}")
        finally:
            # Fecha a conexão com o cliente
            conn.close()
            print(f"Conexão encerrada com {addr}")

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


if __name__ == "__main__":
    server = MonitoringCenter()
    try:
        server.start()
    except KeyboardInterrupt:
        server.shutdown()
