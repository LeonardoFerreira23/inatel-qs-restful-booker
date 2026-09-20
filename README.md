# Testes Automatizados — Restful Booker API

Suíte de testes automatizados de API desenvolvida para a disciplina de **Qualidade de Software** — INATEL — Prof. Christopher Lima.

## Sistema sob teste (SUT)

[Restful Booker](https://restful-booker.herokuapp.com) — API REST pública de reservas de hotel, criada por Mark Winteringham para treino de testes.

Documentação: <https://restful-booker.herokuapp.com/apidoc/index.html>

Escolhida por ser pública, permitir explicitamente automação de testes, expor um CRUD completo com autenticação e conter defeitos propositais — o que gera cenários negativos ricos.

> **Nota:** a API reseta para o estado inicial a cada 10 minutos. Os testes não dependem dos registros pré-carregados: cada cenário cria a própria massa.

## Ferramentas e versões

| Item | Versão |
| --- | --- |
| Python | 3.12.10 |
| pytest | 9.1.1 |
| requests | 2.34.2 |
| pytest-html | 4.2.0 |
| CI | GitHub Actions |

## Estrutura do projeto

```text
inatel-qs-restful-booker/
├── conftest.py                  # fixtures compartilhadas
├── pytest.ini                   # configuração e flags padrão
├── requirements.txt             # dependências com versões fixadas
├── run_tests.py                 # execução unificada
├── data/
│   └── bookings.json            # massa de teste separada do código
├── utils/
│   ├── __init__.py
│   └── api_client.py            # cliente HTTP da API
├── tests/                       # casos de teste TC-001 a TC-020
├── reports/                     # relatórios gerados (ignorados pelo git)
└── .github/
    └── workflows/
        └── tests.yml            # execução automática no CI
```

## Instalação

```bash
git clone https://github.com/LeonardoFerreira23/inatel-qs-restful-booker.git
cd inatel-qs-restful-booker
```

Crie e ative o ambiente virtual:

```bash
python -m venv .venv
```

```bash
source .venv/Scripts/activate     # Windows (Git Bash)
source .venv/bin/activate         # Linux / macOS
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

| Comando | Descrição |
| --- | --- |
| `pytest` | Executa a suíte completa e gera o relatório HTML |
| `pytest -v` | Executa apresentando informações detalhadas de cada caso |
| `pytest --html=reports/relatorio.html --self-contained-html` | Executa e gera o relatório explicitamente |
| `python run_tests.py` | Executa por meio do script de execução unificada |

O relatório é gerado automaticamente em `reports/relatorio.html` — as flags já estão configuradas no `pytest.ini`.

## Equipe e divisão dos casos

| Integrante | Tema | Casos |
| --- | --- | --- |
| Leonardo S. Ferreira | Autenticação, consultas e fluxo E2E | TC-001, TC-002, TC-010, TC-011, TC-012 |
| Júlio César Corrêa | Criação de reservas | TC-003, TC-004, TC-013, TC-014, TC-015 |
| Matheus Reis | Atualização (PUT/PATCH) | TC-005, TC-006, TC-016, TC-017, TC-019 |
| Otavio Lima | Persistência e exclusão | TC-007, TC-008, TC-009, TC-018, TC-020 |

## Defeitos conhecidos da API

Comportamentos da Restful Booker que fogem do esperado para uma API REST. Os testes que os evidenciam validam o comportamento real da API e citam o esperado na docstring.

| Endpoint | Esperado | Recebido | Teste |
| --- | --- | --- | --- |
| `DELETE /booking/{id}` com ID inexistente | 404 | 405 | TC-020 |


## Uso de Inteligência Artificial.

Durante o desenvolvimento deste projeto, foram utilizadas ferramentas de IA como recurso de apoio ao trabalho dos integrantes do grupo.

A IA foi utilizada nas seguintes atividades:

- apoio na revisão do plano de testes;
- auxílio na organização dos casos de teste;
- geração e revisão de trechos de código dos testes automatizados;
- apoio na revisão da estrutura e organização do porjeto.

Os integrantes do grupo analisaram, adaptaram e validaram o conteúdo produzido com auxílio de IA.