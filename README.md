# 🏨 Sistema de Gerenciamento de Hotel

Este projeto é um **Sistema de Gerenciamento Hoteleiro**, desenvolvido em Python, que visa organizar o fluxo de trabalho em estabelecimentos de hospedagem.  
A aplicação segue uma **arquitetura modular (MVC)**, separando as responsabilidades em **Controladores**, **Entidades** e **Telas**, e oferece tanto funcionalidades de **gestão operacional** quanto **relatórios automáticos**.

---

## 🚀 Funcionalidades Principais

O sistema foi projetado para cobrir todos os processos essenciais de um hotel:

### 👥 Hóspedes
- Cadastro, edição, listagem e exclusão de hóspedes.  
- Associação de **pets** aos hóspedes.  
- Consulta individual ou geral de hóspedes.

### 🛏️ Quartos
- Cadastro de **quartos Simples, Duplos e Suítes** com valores e disponibilidade.  
- Edição e exclusão de quartos.  
- Controle de ocupação automática conforme as reservas.

### 📅 Reservas
- Criação e cancelamento de reservas com múltiplos hóspedes e quartos.  
- Adição de **serviços de quarto** e **pets** à reserva.  
- Cálculo automático do valor total da estadia.  
- Geração de relatórios de reservas por hóspede ou por tipo de serviço.

### 💰 Pagamentos
- Registro e confirmação de pagamentos por reserva.  
- Alteração de método de pagamento.  
- Emissão de comprovantes.

### 🧑‍💼 Funcionários e Recursos Humanos
- Cadastro e gerenciamento de **cargos** e **funcionários**.  
- Associação automática entre funcionário e cargo.  
- Controle interno de equipe.

### 🧾 Relatórios
- **Relatório de Quartos Mais Reservados**: mostra estatísticas de uso e porcentagem de ocupação.  
- **Relatório por Hóspede**: lista reservas associadas a cada cliente.  
- **Relatório por Tipo de Serviço**: identifica serviços mais requisitados.

---

## 🧠 Arquitetura do Projeto

O sistema segue o padrão **MVC (Model-View-Controller)**:
- **Entidades (`entidades/`)**: representam os dados e regras de negócio (Hotel, Hospede, Quarto, Reserva, etc).
- **Telas (`telas/`)**: simulam a interface de interação (CLI/GUI).
- **Controladores (`controlers/`)**: contêm a lógica de controle e fluxo do sistema.

Principais arquivos:
