# inatel-qs-restful-booker

Testes Automatizados — Restful Booker API

Suíte de testes automatizados de API desenvolvida para a disciplina de Qualidade de Software — INATEL — Prof. Christopher Lima.

Sistema sob teste (SUT)

Restful Booker — API REST pública de reservas de hotel, criada por Mark Winteringham para treino de testes. Documentação: https://restful-booker.herokuapp.com/apidoc/index.html

Foi escolhida por ser pública, permitir explicitamente automação de testes, expor um CRUD completo com autenticação e conter defeitos propositais — o que gera cenários negativos ricos.

A API reseta para o estado inicial a cada 10 minutos. Os testes não dependem dos registros pré-carregados: cada cenário cria a própria massa.

Ferramenta
Item	Escolha
Linguagem	Python 3.12
Framework	Pytest
Cliente HTTP	Requests
Relatório	pytest-html (HTML) + pytest-json-report (JSON)
CI	GitHub Actions
