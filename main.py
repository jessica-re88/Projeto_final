import mysql.connector

try:
    # Conexão ao banco de dados
    ligacao = mysql.connector.connect(
        host="localhost",
        user="Jéssica",
        password="Jéssica2011",
        database="python4"
    )

    print('Ligação estabelecida com sucesso!')

    cursor = ligacao.cursor()

    # Criação das tabelas
    comando_sql = """
    CREATE TABLE IF NOT EXISTS clientes_ginasio (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255),
        idade INT,
        telefone VARCHAR(15),
        peso FLOAT,
        altura FLOAT,
        plano VARCHAR(100)
    )"""
    cursor.execute(comando_sql)

    comando_sql = """
    CREATE TABLE IF NOT EXISTS assiduidade (
        id INT AUTO_INCREMENT PRIMARY KEY,
        cliente_id INT,
        data_visita DATE,
        FOREIGN KEY (cliente_id) REFERENCES clientes_ginasio(id)
    )"""
    cursor.execute(comando_sql)

    # Inserção de dados iniciais
    comando_sql = 'INSERT INTO clientes_ginasio (nome, idade, telefone, peso, altura, plano) VALUES (%s, %s, %s, %s, %s, %s)'
    dados = [
        ('Maria', 24, '123456789', 82.0, 1.56, 'Mensal'),
        ('Guilherme', 35, '987654321', 100.0, 1.78, 'Trimestral'),
        ('Cleusa Maria', 55, '456789123', 70.0, 1.69, 'Anual'),
        ('Rafael', 23, '789123456', 90.0, 1.85, 'Mensal'),
        ('José', 70, '321654987', 77.0, 1.75, 'Mensal')
    ]
    cursor.executemany(comando_sql, dados)
    ligacao.commit()
    print('\nDados adicionados com sucesso!')

    # Funções para funcionalidades adicionais

    # Consultar clientes por nome ou ID
    def consultar_cliente():
        parametro = input("Digite o nome ou ID do cliente para consulta: ")
        cursor.execute("SELECT * FROM clientes_ginasio WHERE nome LIKE %s OR id = %s", (f"%{parametro}%", parametro))
        resultados = cursor.fetchall()
        for cliente in resultados:
            imc = cliente[4] / (cliente[5] ** 2)  # Cálculo do IMC
            print(f"ID: {cliente[0]}, Nome: {cliente[1]}, IMC: {imc:.2f}")

    # Atualizar dados do cliente
    def atualizar_cliente():
        cliente_id = int(input("Digite o ID do cliente que deseja atualizar: "))
        campo = input("Digite o campo que deseja atualizar (nome, idade, telefone, peso, altura, plano): ")
        novo_valor = input("Digite o novo valor: ")
        cursor.execute(f"UPDATE clientes_ginasio SET {campo} = %s WHERE id = %s", (novo_valor, cliente_id))
        ligacao.commit()
        print(f"Dados do cliente {cliente_id} atualizados com sucesso!")

    # Excluir cliente
    def excluir_cliente():
        cliente_id = int(input("Digite o ID do cliente que deseja excluir: "))
        cursor.execute("DELETE FROM clientes_ginasio WHERE id = %s", (cliente_id,))
        ligacao.commit()
        print(f"Cliente {cliente_id} excluído com sucesso!")

    # Registrar assiduidade
    def registrar_assiduidade():
        cliente_id = int(input("Digite o ID do cliente: "))
        data_visita = input("Digite a data da visita (AAAA-MM-DD): ")
        cursor.execute("INSERT INTO assiduidade (cliente_id, data_visita) VALUES (%s, %s)", (cliente_id, data_visita))
        ligacao.commit()
        print(f"Assiduidade registrada para o cliente {cliente_id} na data {data_visita}.")

    # Menu de opções
    def menu():
        while True:
            print("\nMenu de Opções:")
            print("1. Consultar cliente")
            print("2. Atualizar dados do cliente")
            print("3. Excluir cliente")
            print("4. Registrar assiduidade")
            print("5. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                consultar_cliente()
            elif opcao == "2":
                atualizar_cliente()
            elif opcao == "3":
                excluir_cliente()
            elif opcao == "4":
                registrar_assiduidade()
            elif opcao == "5":
                print("Encerrando o sistema...")
                break
            else:
                print("Opção inválida. Tente novamente.")

    # Executar o menu
    menu()

    # Fechando conexões
    cursor.close()
    ligacao.close()

except mysql.connector.Error as erro:
    print(f"Erro ao estabelecer ligação à base de dados: {erro}")