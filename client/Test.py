import socket

# FIXME: Remover este teste

def Test():
    host = "127.0.0.1"  # Endereço do servidor
    port = 12000  # Porta do servidor

    # Cria um socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Conecta ao servidor
            client_socket.connect((host, port))
            print(f"Conectado ao servidor em {host}:{port}")

            while True:
                # Lê uma mensagem do usuário
                mensagem = input("Digite uma mensagem (ou '\\sair' para encerrar): ")

                # Encerra se o usuário digitar '\\sair'
                if mensagem.lower() == "\\sair":
                    print("Encerrando o cliente.")
                    break

                # Envia a mensagem para o servidor
                client_socket.sendall(mensagem.encode())

                # Recebe a resposta do servidor
                resposta = client_socket.recv(1024).decode()
                print(f"Resposta do servidor: {resposta}")

        except Exception as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    try:
        Test()
    except KeyboardInterrupt:
        print("\nCliente encerrado pelo usuário.")
