# Sistema de Gerenciamento de Estoque

Sistema web para consulta e gerenciamento de estoque, com autenticação de usuários e sincronização com API externa.

## 🚀 Funcionalidades

- Autenticação de usuários via arquivo CSV
- Consulta de produtos em estoque
- Sincronização automática com API externa
- Registro de acessos com localização por IP
- Interface web responsiva
- Edição de arquivos de configuração via interface web

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd site_estoque
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- Linux/Mac:
  ```bash
  source venv/bin/activate
  ```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

1. Crie a pasta `data` se ela não existir:
```bash
mkdir data
```

2. Crie os arquivos de configuração necessários:

- `data/auth.csv` (usuários e senhas):
```
email;password
usuario@exemplo.com;senha123
```

- `data/database.csv` (produtos em estoque):
```
Id;DESCRICAO;ESTOQUE
1;Produto Exemplo;10
```

3. Configure o endereço da API no arquivo `config.py`:
```python
BASE_URL = "http://endereco-da-sua-api:porta"
FILIAL = 1  # Código da filial
```

## 🚀 Executando a aplicação

1. Com o ambiente virtual ativado, execute:
```bash
python app.py
```

2. Acesse a aplicação no navegador:
```
http://localhost:5000
```

## 📁 Estrutura do projeto

```
site_estoque/
├── data/                 # Arquivos de dados
│   ├── auth.csv         # Usuários e senhas
│   ├── database.csv     # Produtos em estoque
│   └── registro_acessos.csv # Log de acessos (gerado automaticamente)
├── templates/           # Templates HTML
├── config.py           # Configurações da aplicação
├── app.py              # Aplicação principal Flask
├── auth_service.py     # Serviço de autenticação
├── product_service.py  # Serviço de produtos
├── estoque_service.py  # Serviço de sincronização com API
├── log_service.py      # Serviço de registro de acessos
├── requirements.txt    # Dependências do projeto
└── README.md           # Este arquivo
```

## 🔒 Segurança

- As senhas são armazenadas em texto simples no arquivo `auth.csv`
- Recomenda-se usar este sistema apenas em redes internas seguras
- Para ambientes de produção, considere implementar criptografia para as senhas

## 📝 Notas de desenvolvimento

- A aplicação usa Flask como framework web
- Os dados são armazenados em arquivos CSV para simplicidade
- A sincronização com a API externa é acionada após login bem-sucedido
- O sistema registra data, hora, IP e localização aproximada de cada acesso

## 🐛 Solução de problemas

Se encontrar erros de permissão no Windows ao ativar o ambiente virtual, execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Para dúvidas ou problemas, verifique se todos os arquivos de configuração foram criados corretamente na pasta `data/`.