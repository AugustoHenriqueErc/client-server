# TP Cliente-Servidor

## 1. Cliente (sensor)

### Funcionalidades

- [x] Se conecta ao servidor e envia periodicamente:
  - [x] Identificação do sensor (ID ou nome)
  - [x] Temperatura atual
  - [x] Timestamp da leitura

- [x] Pode simular o envio com `random.uniform()` para gerar temperaturas variadas
- [x] Pode permitir o envio contínuo ou em ciclos (ex: a cada 1 minuto. Você escolhe como fazer)

## 2. Servidor (central de monitoramento)

### Funcionalidades

- [x] Recebe dados de múltiplos sensores
- [x] Armazena os dados em um log ou estrutura de dados (pode ser um arquivo CSV ou lista)
  - [x] Os dados de sensores e alertas emitidos
  - [x] Um resumo com a temperatura média de cada sensor

- [x] Verifica se a temperatura está fora de um intervalo aceitável (ex: <15°C ou >35°C)
  - [x] Se estiver, envia uma mensagem de alerta ao cliente (sensor)

- [x] Exibir no console:
  - [x] Exibe os dados de sensores e alertas emitidos
  - [x] Um resumo com a temperatura média de cada sensor

- [ ] Implementar um gráfico simples com matplotlib
