# Desafio Python - v3 - Sistema de Banco com Programação Orientada a Objeto

Fomos contratados por um grande banco para desenvolver o seu novo sistema Esse banco deseja modernizar suas operações e para isso escolheu a linguagem Python Para a primeira versão do sistema devemos implementar apenas 3 operações depósito, saque e extrato.

## Depósito
Deve ser possível depositar valores positivos para a minha conta bancária A v 1 do projeto trabalha apenas com 1 usuário,
dessa forma não precisamos nos preocupar em identificar qual é o número da agência e conta bancária Todos os depósitos
devem ser armazenados em uma variável e exibidos na operação de extrato.

## Saque
O sistema deve permitir realizar 3 saques diários com limite máximo de R 500 00 por saque Caso o usuário não tenha
saldo em conta, o sistema deve exibir uma mensagem informando que não será possível sacar o dinheiro por falta de
saldo Todos os saques devem ser armazenados em uma variável e exibidos na operação de extrato.

## Extrato
Essa operação deve listar todos os depósitos e saques realizados na conta No fim da listagem deve ser exibido o
saldo atual da conta Se o extrato estiver em branco, exibir a mensagem Não foram realizadas movimentações
Os valores devem ser exibidos utilizando o formato R xxx xx, exemplo:

1500.45 = R$ 1500.45

## Cadastra Usuário
Cadastra um novo usuário com CPF, nome, data de nascimento e endereço

## Cadastra conta
Cria uma nova conta associada a um usuário com os atributos agência e número da conta.
O número da conta é gerado automaticamente de forma sequencial

## Lista usuários
Lista todos os usuários da base, mostrando: CPF e nome

## Lista contas
Lista todas as contas da base, mostrando: Número da conta, CPF e nome

## Funcionalidades como classe

Todas as funcionalidades devem ser implementadas como classe:

- Conta
- ContaCorrente
- Histórico
- Cliente
- PessoaFisica
- Transacao (Interface)
- Deposito
- Saque

