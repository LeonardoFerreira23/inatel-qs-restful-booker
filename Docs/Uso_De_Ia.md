# Uso de Inteligência Artificial

## 1. Ferramentas e modelos utilizados

Durante o desenvolvimento do projeto, foram utilizadas ferramentas de Inteligência Artificial como apoio às atividades de desenvolvimento, configuração, análise e resolução de problemas.

As ferramentas utilizadas foram:

- **ChatGPT (OpenAI):** utilizado para esclarecimento de dúvidas técnicas, análise de erros, apoio à configuração do Docker Compose e do Jenkins e revisão de código.
- **Claude (Anthropic):** utilizado para auxiliar na elaboração e análise do pipeline Jenkins, configuração do Docker Compose, investigação de problemas e compreensão de conceitos relacionados aos testes automatizados.
- **Claude Code:** utilizado como ferramenta de apoio durante atividades de análise e desenvolvimento no projeto.

## 2. Finalidades de utilização

As ferramentas de IA foram utilizadas em diferentes etapas do desenvolvimento, principalmente nas seguintes atividades:

- **Docker e Docker Compose:** auxílio na configuração dos serviços, volumes, variáveis de ambiente, portas e comunicação entre contêineres, incluindo Jenkins, API e Mailpit.
- **Jenkins e CI/CD:** apoio na elaboração e revisão do Jenkinsfile, organização das etapas do pipeline, execução dos testes automatizados e configuração de notificações por e-mail para builds bem-sucedidas ou com falhas.
- **Relatórios:** auxílio na configuração de um contêiner Nginx para disponibilização dos relatórios de testes.
- **Testes automatizados:** esclarecimento de dúvidas sobre ferramentas de cobertura de código, como pytest-cov e c8, e análise de comportamentos da API.
- **Debugging:** investigação de erros relacionados à comunicação entre contêineres, variáveis de ambiente, checkout do repositório e portas ocupadas.
- **Git e GitHub:** revisão de alterações.
- **Aprendizado:** explicação de configurações e trechos de código para facilitar a compreensão das tecnologias utilizadas.

## 3. Exemplos de prompts utilizados

A seguir, são apresentados exemplos reais de prompts utilizados durante o desenvolvimento, acompanhados das decisões tomadas pelo grupo em relação às respostas recebidas.

### Prompt 1 — Investigação de erros em pull requests

**Prompt:**

> Como eu posso verificar essas questões e comprovar que elas quebram?

**Contexto:** análise de problemas identificados em um pull request relacionado à configuração do pipeline.

**Resultado:** a ferramenta sugeriu comandos e procedimentos para reproduzir os problemas. A orientação foi aceita e utilizada para executar uma build e confirmar a falha no checkout do repositório, que apresentou a mensagem `Checkout of Git remote '' aborted`.

### Prompt 2 — Ferramentas de cobertura de código

**Prompt:**

> restfull booker é caixa preta a gente n tem o código, explique melhor sobre pytest-cov

**Contexto:** discussão sobre a utilização de ferramentas de cobertura de código no projeto, considerando que a API Restful Booker é externa e não temos acesso ao seu código-fonte.

**Resultado:** a ferramenta explicou que o pytest-cov mede a cobertura do código Python utilizado no projeto e sugeriu o c8 como alternativa para medir a cobertura da API. A sugestão foi analisada, mas não adotada. O grupo manteve o pytest-cov no pull request correspondente.

### Prompt 3 — Funcionamento da geração de relatórios

**Prompt:**

> vc falou que pra gerar o relatório a gente tem que desligar o pipeline, explica isso melhor

**Contexto:** esclarecimento sobre o funcionamento da geração e disponibilização dos relatórios de testes.

**Resultado:** após a dúvida, a ferramenta corrigiu sua explicação anterior e esclareceu que a interrupção mencionada se referia à API, e não ao pipeline Jenkins. A explicação foi ajustada para evitar uma interpretação incorreta.

### Prompt 4 — Organização da resolução de problemas

**Prompt:**

> a gente tem que resolver os problemas dos 4 pr

**Contexto:** análise de problemas presentes em diferentes pull requests do projeto.

**Resultado:** a ferramenta sugeriu reunir as alterações em uma única branch. A sugestão foi descartada pelo grupo, que optou por analisar e corrigir os pull requests individualmente, facilitando a identificação e validação de cada problema.

### Prompt 5 — Análise de configuração do Docker Compose

**Contexto:** investigação de uma falha relacionada à configuração de um pull request.

**Prompt:**

> Como posso verificar se essa configuração está correta e reproduzir o erro?

**Resultado:** a ferramenta auxiliou na análise dos arquivos e identificou uma referência ao hostname `restful-booker-local`, que não correspondia ao serviço definido no Docker Compose. A hipótese foi testada durante a execução do pipeline, que apresentou a falha `Failed to resolve 'restful-booker-local'`. A análise foi utilizada para compreender o problema, e o pull request foi posteriormente fechado.

## 4. Dinâmica de utilização

A utilização das ferramentas de Inteligência Artificial ocorreu principalmente de forma individual, como apoio às atividades de desenvolvimento e investigação de problemas.

Em algumas situações, as sugestões foram discutidas entre os integrantes do grupo antes de serem aplicadas. As ferramentas também foram utilizadas para revisar configurações, explicar trechos de código, interpretar mensagens de erro e sugerir possíveis soluções.

As respostas geradas não foram incorporadas automaticamente. As sugestões foram analisadas, testadas e, quando necessário, adaptadas ou descartadas conforme as necessidades do projeto.

As alterações mais relevantes foram verificadas por meio da execução local dos serviços, testes automatizados e builds no Jenkins.

## 5. Atividades desenvolvidas manualmente

Apesar do uso de ferramentas de IA, diversas atividades foram realizadas manualmente pelos integrantes do grupo, incluindo:

- Implementação, edição e adaptação dos arquivos do projeto.
- Execução dos testes automatizados e validação dos resultados.
- Configuração e preenchimento das variáveis de ambiente.
- Execução local dos serviços utilizando Docker Compose.
- Análise dos logs e investigação de falhas durante as builds.
- Reprodução de erros identificados durante a revisão dos pull requests.
- Revisão das alterações propostas e avaliação das sugestões geradas pelas ferramentas de IA.
- Decisões sobre quais soluções seriam aceitas, adaptadas ou descartadas.
- Organização das branches, elaboração dos commits e gerenciamento dos pull requests.

Também foram realizadas manualmente correções em configurações do projeto, incluindo ajustes no pipeline e na integração entre os serviços.

## 6. Considerações finais

As ferramentas de Inteligência Artificial foram utilizadas como recursos de apoio ao desenvolvimento, contribuindo para a compreensão das tecnologias, investigação de erros e resolução de dificuldades técnicas.

Entretanto, as decisões sobre a implementação, validação e integração das alterações permaneceram sob responsabilidade dos integrantes do grupo. As sugestões das ferramentas foram avaliadas criticamente e submetidas a testes antes de serem consideradas adequadas ao projeto.