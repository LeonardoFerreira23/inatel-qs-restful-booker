# Testes Automatizados — Restful Booker API

Suíte de testes automatizados de API desenvolvida para a disciplina de **Qualidade de Software** — INATEL — Prof. Christopher Lima.

Na segunda parte (**DevOps — S07**), a suíte passou a rodar em um pipeline Jenkins conteinerizado, orquestrado com Docker Compose.

## Sistema sob teste (SUT)

[Restful Booker](https://restful-booker.herokuapp.com) — API REST pública de reservas de hotel, criada por Mark Winteringham para treino de testes.

Documentação: <https://restful-booker.her

Escolhida por ser pública, permitir expli, expor um CRUD completo com autenticaçãoe conter defeitos propositais — o que gera cenários negativos ricos.

> **Nota:** a API pública reseta para o estado inicial a cada 10 minutos. Os testes não dependem dos registros pré-carregados: cada cenário cria a própria massa. No Docker Compose, os testes usam uma instância local da API.

## Ferramentas e versões

| Item | Versão |
| --- | --- |
| Python | 3.12.10 |
| pytest | 9.1.1 |
| requests | 2.34.2 |
| pytest-html | 4.2.0 |
| Jenkins | 2.580.2 LTS (JDK 21) |
| Docker Compose | v2+ |

## Estrutura do projeto

```text
inatel-qs-restful-booker/
├── conftest.py                  # fixtures compartilhadas
├── pytest.ini                   # configuração e flags padrão
├── requirements.txt             # depend
├── run_tests.py                 # execução unificada
├── Jenkinsfile                  # pipeline: Dependencias, Testes, Build
├── docker-compose.yml           # jenkin
├── data/
│   └── bookings.json            # massa de teste separada do código
├── utils/
│   ├── __init__.py
│   └── api_client.py            # cliente HTTP da API
├── tests/                       # casos de teste TC-001 a TC-020
├── reports/                     # relatórios gerados (ignorados pelo git)
└── jenkins/
    ├── Dockerfile               # imagem0
    ├── casc.yaml                # configuração como código (usuário e job)
    └── plugins.txt              # plugins instalados na imagem
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

O relatório é gerado automaticamente em `reports/relatorio.html` e o JUnit em `reports/junit.xml` — as flags já
estão configuradas no `pytest.ini`.

Por padrão os testes usam a API pública. ncia, defina `BOOKER_BASE_URL` (ex.:`http://localhost:3001`).

## Execução com Docker Compose

```bash
docker compose up -d --build
```

| Serviço | Endereço | Função |
| --- | --- | --- |
| jenkins | <http://localhost:8080> | pipeline (usuário `admin`, senha em `JENKINS_ADMIN_PASSWORD`, padrão `admin`) |
| restful-booker | <http://localhost:3001> | API local usada pelos testes do pipeline |

Dentro do Compose os testes apontam para a API local via `BOOKER_BASE_URL`, sem depender do Heroku.
O volume `jenkins_home` mantém jobs e histórico entre reinícios. Para zerar tudo: `docker compose down -v`.

O job `restful-booker` é criado automaticamente pelo `casc.yaml` e lê o `Jenkinsfile` da branch `main` do
GitHub. Para testar outra branch, defina (ex.: `*/minha-branch`).

### Pipeline

| Estágio | O que faz |
| --- | --- |
| Dependencias | cria o venv e instala o `requirements.txt` |
| Testes | roda a suíte e publica `junit.xml` e o relatório HTML |
| Build | empacota a suíte em `dist/restful-booker-tests-<build>.tar.gz` |



- [x] Jenkins em container com configuração como código
- [x] Pipeline com estágios de dependências, testes e build
- [x] Docker Compose com Jenkins e API local, com volume persistente
- [ ] Envio de e-mail ao final do pipeline (Mailpit)
- [ ] Container de relatórios (nginx) com volume compartilhado
- [ ] Cobertura de testes >= 90%
- [ ] Imagem publicada no Docker Hub

## Equipe e divisão dos casos

| Integrante | Tema | Casos |
| --- | --- | --- |
| Leonardo S. Ferreira | Autenticação | TC-001, TC-002, TC-010, TC-011, TC-012|
| Júlio César Corrêa | Criação de reserva | TC-003, TC-004, TC-013, TC-014, TC-015 |
| Matheus Reis | Atualização (PUT/PATCH) | TC-005, TC-006, TC-016, TC-017, TC-019 |
| Otavio Lima | Persistência e exclusão | TC-007, TC-008, TC-009, TC-018, TC-020 |

## Defeitos conhecidos da API

Comportamentos da Restful Booker que fogem do esperado para uma API REST. Os testes que os evidenciam validam o comportamento real da API e citam o esperado na docstring.

| Endpoint | Esperado | Recebido | Teste |
| --- | --- | --- | --- |
| `DELETE /booking/{id}` com ID inexistente | 404 | 405 | TC-020 |

## Uso de Inteligência Artificial

Durante o desenvolvimento deste projeto, foram utilizadas ferramentas de IA como recurso de apoio ao trabalho dos integrantes do grupo.

A IA foi utilizada nas seguintes atividades:

- apoio na revisão do plano de testes;
- auxílio na organização dos casos de tes
- geração e revisão de trechos de código dos testes automatizados;
- apoio na revisão da estrutura e organização do projeto;
- apoio na configuração do pipeline Jenkins e do Docker Compose.

Os integrantes do grupo analisaram, adaptaram e validaram o conteúdo produzido com auxílio de IA.