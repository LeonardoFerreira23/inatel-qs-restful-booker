# Testes Automatizados — Restful Booker API

Suíte de testes automatizados de API desenvolvida para a disciplina de **Qualidade de Software** — INATEL — Prof. Christopher Lima.

Na segunda parte (**DevOps — S07**), a suíte passou a rodar em um pipeline Jenkins conteinerizado, orquestrado com Docker Compose.

## Sistema sob teste (SUT)

[Restful Booker](https://restful-booker.herokuapp.com) — API REST pública de reservas de hotel, criada por Mark Winteringham para treino de testes.

Documentação: <https://restful-booker.herokuapp.com/apidoc/index.html>

Escolhida por ser pública, expor um CRUD completo com autenticação e conter defeitos propositais, o que gera cenários negativos ricos.

> **Nota:** a API pública reseta para o estado inicial a cada 10 minutos. Os testes não dependem dos registros pré-carregados: cada cenário cria a própria massa. No Docker Compose, os testes usam uma instância local da API.

## Ferramentas e versões

| Item | Versão |
| --- | --- |
| Python | 3.12.10 |
| pytest | 9.1.1 |
| pytest-html | 4.2.0 |
| pytest-cov | 7.1.0 |
| requests | 2.34.2 |
| Jenkins | 2.580.2 LTS (JDK 21) |
| Mailpit | v1.21.8 |
| Nginx | 1.27-alpine |
| Docker Compose | v2+ |

## Estrutura do projeto

```text
inatel-qs-restful-booker/
├── conftest.py                  # fixtures compartilhadas
├── pytest.ini                   # configuração e flags padrão
├── requirements.txt             # dependências com versões fixadas
├── run_tests.py                 # execução unificada
├── Jenkinsfile                  # pipeline: Dependencias, Testes, Build e e-mail
├── docker-compose.yml           # jenkins, API, mailpit e relatorios
├── .env.example                 # modelo das variáveis de ambiente
├── data/
│   └── bookings.json            # massa de teste separada do código
├── utils/
│   └── api_client.py            # cliente HTTP da API
├── tests/                       # casos de teste TC-001 a TC-020
├── scripts/
│   ├── package_project.py       # gera o pacote .tar.gz no estágio Build
│   └── send_email.py            # envia o e-mail com o resultado do pipeline
├── reports/                     # relatórios gerados (ignorados pelo git)
├── jenkins/
│   ├── Dockerfile               # imagem do Jenkins com Python 3.12.10
│   ├── casc.yaml                # configuração como código (usuário e job)
│   └── plugins.txt              # plugins instalados na imagem
├── relatorios/
│   ├── Dockerfile               # Nginx que serve os relatórios
│   └── default.conf             # configuração do Nginx
└── Docs/
    └── Uso_De_Ia.md             # documentação sobre o uso de IA
```

## Execução local (sem Docker)

```bash
git clone https://github.com/LeonardoFerreira23/inatel-qs-restful-booker.git
cd inatel-qs-restful-booker
python -m venv .venv
source .venv/Scripts/activate     # Windows (Git Bash)
source .venv/bin/activate         # Linux / macOS
pip install -r requirements.txt
```

| Comando | Descrição |
| --- | --- |
| `pytest` | Executa a suíte completa e gera os relatórios |
| `python run_tests.py` | Mesma execução, pelo script unificado |
| `pytest --cov=utils.api_client --cov-report=term-missing` | Executa e mostra a cobertura |

Os relatórios são gerados em `reports/relatorio.html` (HTML) e `reports/junit.xml` (JUnit). As flags já estão no `pytest.ini`.

Por padrão os testes usam a API pública. Para usar outra instância, defina `BOOKER_BASE_URL` (ex.: `http://localhost:3001`).

## Execução com Docker Compose

Pré-requisitos: Docker Desktop (ou Docker Engine) com Compose v2 e Git.

```bash
git clone https://github.com/LeonardoFerreira23/inatel-qs-restful-booker.git
cd inatel-qs-restful-booker
cp .env.example .env              # depois, edite o EMAIL_TO
docker compose up -d --build
```

Depois de 1 a 2 minutos, abra <http://localhost:8080>, entre com `admin` / `admin`, abra o job `restful-booker` e clique em **Construir agora**.

### Variáveis do `.env`

| Variável | Padrão | Para que serve |
| --- | --- | --- |
| `JENKINS_ADMIN_PASSWORD` | `admin` | Senha do usuário `admin` do Jenkins |
| `REPO_BRANCH` | `*/main` | Branch que o job do Jenkins executa |
| `EMAIL_TO` | (nenhum) | Destinatário do e-mail com o resultado do pipeline |
| `SMTP_HOST` / `SMTP_PORT` | `mailpit` / `1025` | Servidor SMTP usado no envio |

O `.env` está no `.gitignore`: os dados de cada pessoa não vão para o repositório.

### Serviços

| Serviço | Endereço | Imagem | Para que serve |
| --- | --- | --- | --- |
| `jenkins` | <http://localhost:8080> | Docker Hub (publicada pelo grupo) | Pipeline (usuário `admin`) |
| `restful-booker` | <http://localhost:3001> | Docker Hub (`mwinteringham/restfulbooker`) | API local usada pelos testes |
| `mailpit` | <http://localhost:8025> | Docker Hub (`axllent/mailpit`) | Caixa de e-mail de teste |
| `relatorios` | <http://localhost:8081> | Dockerfile local (`relatorios/`) | Nginx com os relatórios dos builds |

Os containers se comunicam pela rede do Compose: o Jenkins chama a API em `http://restful-booker:3001` e envia o e-mail para `mailpit:1025`.

Os dados ficam em volumes nomeados (`jenkins_home`, `mailpit_data` e `relatorios`) e continuam lá depois de um `docker compose down`. Para apagar tudo, use `docker compose down -v`.

> Em Mac com chip Apple, a imagem da API roda emulada (`platform: linux/amd64`), porque não existe versão arm64 dela.

### Imagem no Docker Hub

A imagem do Jenkins (gerada a partir de `jenkins/Dockerfile`) está publicada em <https://hub.docker.com/r/juliocesarcorrea001/inatel-qs-jenkins>.

## Pipeline

O job `restful-booker` é criado automaticamente pelo `casc.yaml` e lê o `Jenkinsfile` da branch definida em `REPO_BRANCH`. Todas as etapas estão no `Jenkinsfile`.

| Estágio | O que faz |
| --- | --- |
| Dependencias | Confere o Python 3.12.10, cria o venv e instala o `requirements.txt` |
| Testes | Roda a suíte com cobertura mínima de 90%, publica o `junit.xml`, arquiva a pasta `reports/` e copia os relatórios para o volume `relatorios` |
| Build | Gera `dist/restful-booker-tests-<build>.tar.gz` com `scripts/package_project.py` e arquiva o pacote |
| Pós-build | Envia um e-mail de sucesso ou de falha para `EMAIL_TO` com `scripts/send_email.py` |

### Relatórios

- No Jenkins: artefatos de cada build (`relatorio.html`, `junit.xml`, `coverage-html/` e o `.tar.gz`).
- No Nginx: <http://localhost:8081/ultimo/> (último build) e `build-<número>/` (histórico).

### Cobertura

A cobertura é medida com `pytest-cov` sobre o cliente HTTP do projeto (`utils/api_client.py`). Se ficar abaixo de 90%, o estágio Testes falha (`--cov-fail-under=90`). O relatório fica em `reports/coverage-html/`.

A Restful Booker é uma API externa (caixa-preta), então o `pytest-cov` mede o código Python do projeto, não o código da API.

## Situação do projeto (S07)

- [x] Jenkins em container com configuração como código
- [x] Pipeline com estágios de dependências, testes e build
- [x] Envio de e-mail ao final do pipeline (Mailpit)
- [x] Docker Compose com 4 containers, volumes e comunicação entre eles
- [x] Container de relatórios (Nginx) com volume compartilhado
- [x] Cobertura de testes ≥ 90%
- [x] Imagem publicada no Docker Hub

## Equipe e divisão dos casos

| Integrante | Tema | Casos |
| --- | --- | --- |
| Leonardo S. Ferreira | Autenticação | TC-001, TC-002, TC-010, TC-011, TC-012 |
| Júlio César Corrêa | Criação de reserva | TC-003, TC-004, TC-013, TC-014, TC-015 |
| Matheus Reis | Atualização (PUT/PATCH) | TC-005, TC-006, TC-016, TC-017, TC-019 |
| Otavio Lima | Persistência e exclusão | TC-007, TC-008, TC-009, TC-018, TC-020 |

## Defeitos conhecidos da API

Comportamentos da Restful Booker que fogem do esperado para uma API REST. Os testes que os evidenciam validam o comportamento real da API e citam o esperado na docstring.

| Endpoint | Esperado | Recebido | Teste |
| --- | --- | --- | --- |
| `DELETE /booking/{id}` com ID inexistente | 404 | 405 | TC-020 |

## Uso de Inteligência Artificial

### Modelos utilizados

- **ChatGPT (OpenAI):** dúvidas técnicas, análise de erros, apoio na configuração do Docker Compose e do Jenkins e revisão de código.
- **Claude (Anthropic), no app e no Claude Code:** elaboração e análise do pipeline Jenkins, configuração do Docker Compose, investigação de problemas e estudo dos conceitos usados no projeto.

### Para que a IA foi usada

- **Testes (NP1):** revisão do plano de testes, organização dos casos de teste e geração e revisão de trechos dos testes automatizados.
- **Docker e Docker Compose:** configuração dos serviços, volumes, variáveis de ambiente, portas e comunicação entre os containers (Jenkins, API, Mailpit e Nginx).
- **Jenkins:** elaboração e revisão do `Jenkinsfile`, organização dos estágios e notificação por e-mail.
- **Cobertura:** dúvidas sobre `pytest-cov` e `c8` e sobre o que cada ferramenta mede.
- **Debugging:** erros de comunicação entre containers, variáveis de ambiente vazias, checkout do repositório e portas ocupadas.
- **Revisão e estudo:** análise dos pull requests do grupo e explicação linha a linha das configurações.

### Exemplos de prompts reais

Prompts registrados pela equipe durante a revisão dos pull requests.

| Prompt | Resposta da IA | Resultado |
| --- | --- | --- |
| "Como eu posso verificar essas questões e comprovar que elas quebram?" (PR #9) | Comandos para reproduzir cada problema | **Aceito**: o build confirmou o erro `Checkout of Git remote '' aborted` |
| "restfull booker é caixa preta a gente n tem o código, explique melhor sobre pytest-cov" | O `pytest-cov` mede só o cliente Python; sugeriu medir a API com o `c8` | **Descartado**: o grupo manteve o `pytest-cov` (PR #11) |
| "vc falou que pra gerar o relatório a gente tem que desligar o pipeline, explica isso melhor" | Corrigiu a própria explicação: quem para é a API, não o pipeline | **Ajustado**: a resposta anterior estava imprecisa |
| "a gente tem que resolver os problemas dos 4 pr" | Começou a montar uma branch juntando todos os PRs | **Descartado**: os PRs foram corrigidos um por um |
| Pedido de análise do PR #12 | Apontou que o host `restful-booker-local` não existe no Compose | **Aceito**: o build falhou com `Failed to resolve 'restful-booker-local'` e o PR foi fechado |

### Dinâmica de uso

- O uso foi principalmente individual. Em alguns casos, as sugestões foram discutidas no grupo antes de serem aplicadas.
- As respostas não foram incorporadas automaticamente: cada sugestão foi analisada, testada e, quando necessário, adaptada ou descartada.
- As mudanças mais relevantes foram validadas com a execução local dos containers e com builds no Jenkins.

### O que foi feito manualmente

- Edição e adaptação dos arquivos do projeto e correções nos pull requests.
- Execução dos testes, dos containers e dos builds, com análise dos logs.
- Reprodução dos erros encontrados na revisão dos pull requests.
- Decisões sobre o que aceitar, adaptar ou descartar.
- Organização das branches, commits, revisões e merges.

A versão detalhada está em [Docs/Uso_De_Ia.md](Docs/Uso_De_Ia.md).
