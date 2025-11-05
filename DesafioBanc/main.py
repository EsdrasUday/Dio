import abc
from datetime import date

class Transacao(abc.ABC):
    """
    Interface para as transações.
    Define o método 'registrar' que todas as transações concretas
    (Saque, Deposito) devem implementar.
    """
    
    # O UML não especifica um 'valor' nesta interface,
    # mas ambas as implementações (Saque, Deposito) o possuem.
    # Vamos adicioná-lo no construtor das classes filhas.

    @abc.abstractmethod
    def registrar(self, conta):
        """Registra a transação na conta."""
        pass

class Deposito(Transacao):
    """Representa uma transação de depósito."""
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta):
        """
        Registra o depósito na conta.
        Atualiza o saldo e adiciona ao histórico.
        """
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)
        
    def __str__(self):
        # Helper para facilitar a leitura no extrato
        return f"[+] Depósito: R$ {self.valor:.2f}"

class Saque(Transacao):
    """Representa uma transação de saque."""
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta):
        """
        Registra o saque na conta.
        Atualiza o saldo e adiciona ao histórico.
        A validação (se o saque é possível) é feita
        pela própria classe 'Conta' antes de chamar este método.
        """
        conta.saldo -= self.valor
        conta.historico.adicionar_transacao(self)
        
    def __str__(self):
        return f"[-] Saque:    R$ {self.valor:.2f}"


class Historico:
    """Armazena e gerencia a lista de transações de uma conta."""
    
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        """Propriedade para acessar a lista de transações."""
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        """Adiciona uma nova transação ao histórico."""
        self._transacoes.append(transacao)

    def gerar_relatorio(self):
        """Gera um extrato de texto das transações."""
        if not self._transacoes:
            return "Nenhuma transação realizada."
        
        relatorio = "--- Extrato de Transações ---\n"
        for transacao in self._transacoes:
            relatorio += f"{str(transacao)}\n"
        return relatorio

class Conta:
    """
    Classe base para contas bancárias.
    Armazena dados da conta e gerencia operações de saque e depósito.
    """
    
    def __init__(self, numero: int, cliente, agencia: str = "0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico() # Composição: Conta "possui" um Histórico

    @classmethod
    def nova_conta(cls, cliente, numero: int):
        """Método de fábrica para criar uma nova conta."""
        return cls(numero, cliente)

    def depositar(self, valor: float) -> bool:
        """
        Realiza um depósito na conta.
        Cria a transação e a registra.
        """
        if valor <= 0:
            print("Erro: O valor do depósito deve ser positivo.")
            return False
        

        deposito = Deposito(valor)
        deposito.registrar(self)
        print("Depósito realizado com sucesso.")
        return True

    def sacar(self, valor: float) -> bool:
        """
        Realiza um saque na conta.
        Este método será sobrescrito por classes filhas (ContaCorrente).
        """
        if valor <= 0:
            print("Erro: O valor do saque deve ser positivo.")
            return False

        if valor > self.saldo:
            print("Erro: Saldo insuficiente.")
            return False
            
 
        saque = Saque(valor)
        saque.registrar(self)
        print("Saque realizado com sucesso.")
        return True
        
    def __str__(self):
        nome_cliente = getattr(self.cliente, 'nome', 'Cliente') # Pega o nome se existir
        return f"Agência: {self.agencia} | Conta: {self.numero} | Titular: {nome_cliente}"

class ContaCorrente(Conta):
    """Implementação específica de Conta para 'Conta Corrente'."""
    
    def __init__(self, numero: int, cliente, limite: float = 500.0, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self._numero_saques_realizados = 0

    def sacar(self, valor: float) -> bool:
        """Sobrescreve o método 'sacar' para incluir regras da conta corrente."""
        
        if valor <= 0:
            print("Erro: O valor do saque deve ser positivo.")
            return False
            
        if self._numero_saques_realizados >= self.limite_saques:
            print(f"Erro: Limite de {self.limite_saques} saques diários atingido.")
            return False
        
        saldo_total_disponivel = self.saldo + self.limite
        if valor > saldo_total_disponivel:
            print(f"Erro: Valor do saque excede o limite disponível (Saldo + Cheque Especial).")
            print(f"Disponível: R$ {saldo_total_disponivel:.2f}")
            return False
            
      
        saque = Saque(valor)
        saque.registrar(self) 
        
        self._numero_saques_realizados += 1
        print("Saque realizado com sucesso.")
        return True

class Cliente:
    """Classe base para clientes do banco."""
    
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = [] 

    def adicionar_conta(self, conta: Conta):
        """Adiciona uma conta à lista de contas do cliente."""
        self.contas.append(conta)

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        """
        Realiza uma transação em uma conta específica do cliente.
        
        Nota de Design: No diagrama UML, este método existe.
        No entanto, um fluxo mais robusto (usado nesta implementação)
        é chamar 'conta.sacar()' ou 'conta.depositar()', que
        internamente criam e registram a transação.
        
        Mantemos o método aqui para seguir o UML, mas ele não é
        o ponto de entrada principal para saques/depósitos no nosso menu.
        """
        
        # Validação simples para garantir que o cliente "possa" usar a conta
        if conta not in self.contas:
            print("Erro: O cliente não possui esta conta.")
            return

        # Delega o registro para a própria transação
        transacao.registrar(conta)


class PessoaFisica(Cliente):
    """Implementação específica de Cliente para 'Pessoa Física'."""
    
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        
    def __str__(self):
        return f"Cliente: {self.nome} (CPF: {self.cpf})"
    


def menu():
    """Exibe o menu de opções."""
    print("\n--- Sistema Bancário v2 (POO) ---")
    print("1. Criar Novo Cliente")
    print("2. Criar Nova Conta Corrente")
    print("3. Listar Contas de um Cliente")
    print("4. Depositar")
    print("5. Sacar")
    print("6. Ver Extrato")
    print("0. Sair")
    return input("Escolha uma opção: ")

def filtrar_cliente_por_cpf(cpf, clientes):
    """Busca um cliente na lista pelo CPF."""
    clientes_encontrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_encontrados[0] if clientes_encontrados else None

def get_conta_cliente(cliente: PessoaFisica):
    """Permite ao usuário selecionar uma das contas do cliente."""
    if not cliente.contas:
        print("Erro: Este cliente não possui contas.")
        return None
    
    if len(cliente.contas) == 1:
        return cliente.contas[0]
        
    print("Selecione a conta:")
    for i, conta in enumerate(cliente.contas):
        print(f"{i+1}. {conta}")
        
    try:
        idx = int(input("Número da conta: ")) - 1
        if 0 <= idx < len(cliente.contas):
            return cliente.contas[idx]
        else:
            print("Seleção inválida.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None


def main():
    """Função principal que executa o menu interativo."""
    clientes = []
    contas = [] 
    while True:
        opcao = menu()

        if opcao == "1": 
            print("--- Novo Cliente (Pessoa Física) ---")
            cpf = input("CPF (só números): ")
            cliente_existente = filtrar_cliente_por_cpf(cpf, clientes)
            
            if cliente_existente:
                print("Erro: Já existe um cliente com este CPF.")
                continue
                
            nome = input("Nome completo: ")
          
            dt_nasc_str = input("Data de Nascimento (DD-MM-AAAA): ")
            try:
                dia, mes, ano = map(int, dt_nasc_str.split('-'))
                data_nascimento = date(ano, mes, dia)
            except ValueError:
                print("Formato de data inválido. Usando data padrão.")
                data_nascimento = date(2000, 1, 1)
                
            endereco = input("Endereço (Rua, N - Bairro, Cidade/Sigla): ")
            
            novo_cliente = PessoaFisica(
                cpf=cpf,
                nome=nome,
                data_nascimento=data_nascimento,
                endereco=endereco
            )
            clientes.append(novo_cliente)
            print(f"Cliente '{nome}' criado com sucesso!")

        elif opcao == "2": 
            print("--- Nova Conta Corrente ---")
            cpf_cliente = input("CPF do titular: ")
            cliente = filtrar_cliente_por_cpf(cpf_cliente, clientes)
            
            if not cliente:
                print("Erro: Cliente não encontrado. Crie o cliente primeiro.")
                continue
                
            
            numero_conta = len(contas) + 1
            
            
            nova_conta = ContaCorrente.nova_conta(
                cliente=cliente,
                numero=numero_conta
            )
            
            contas.append(nova_conta)
            cliente.adicionar_conta(nova_conta) 
            
            print(f"Conta Corrente {nova_conta.numero} criada para {cliente.nome}.")

        elif opcao == "3": 
            cpf_cliente = input("CPF do titular: ")
            cliente = filtrar_cliente_por_cpf(cpf_cliente, clientes)
            
            if not cliente:
                print("Erro: Cliente não encontrado.")
                continue
                
            if not cliente.contas:
                print(f"Cliente {cliente.nome} não possui contas cadastradas.")
                continue
                
            print(f"--- Contas de {cliente.nome} ---")
            for conta in cliente.contas:
                print(f"  > {conta}")
                
        elif opcao == "4": 
            cpf_cliente = input("CPF do titular: ")
            cliente = filtrar_cliente_por_cpf(cpf_cliente, clientes)
            
            if not cliente:
                print("Erro: Cliente não encontrado.")
                continue
                
            conta = get_conta_cliente(cliente)
            if not conta:
                continue
                
            try:
                valor = float(input("Valor do depósito: R$ "))
                conta.depositar(valor)
            except ValueError:
                print("Erro: Valor inválido.")

        elif opcao == "5": 
            cpf_cliente = input("CPF do titular: ")
            cliente = filtrar_cliente_por_cpf(cpf_cliente, clientes)
            
            if not cliente:
                print("Erro: Cliente não encontrado.")
                continue
                
            conta = get_conta_cliente(cliente)
            if not conta:
                continue
                
            try:
                valor = float(input("Valor do saque: R$ "))
                conta.sacar(valor)
            except ValueError:
                print("Erro: Valor inválido.")

        elif opcao == "6": 
            cpf_cliente = input("CPF do titular: ")
            cliente = filtrar_cliente_por_cpf(cpf_cliente, clientes)
            
            if not cliente:
                print("Erro: Cliente não encontrado.")
                continue
                
            conta = get_conta_cliente(cliente)
            if not conta:
                continue
                
            print(f"\n--- Extrato da Conta {conta.numero} ---")
            print(f"Titular: {cliente.nome}")
            print(conta.historico.gerar_relatorio())
            print("---------------------------------")
            print(f"Saldo Atual:     R$ {conta.saldo:.2f}")
            if isinstance(conta, ContaCorrente):
                 print(f"Cheque Especial: R$ {conta.limite:.2f}")
                 print(f"Disponível total: R$ {conta.saldo + conta.limite:.2f}")

        elif opcao == "0":
            print("Obrigado por usar o sistema!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()