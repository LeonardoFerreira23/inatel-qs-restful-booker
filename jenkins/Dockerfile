FROM jenkins/jenkins:2.580.2-lts-jdk21

USER root
# o apt do Debian so oferece o Python 3.13; o uv instala a versao exata do projeto
COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /usr/local/bin/uv
RUN uv python install 3.12.10 --install-dir /opt/uv-python \
    && mv /opt/uv-python/cpython-3.12.10-* /opt/python \
    && rm -rf /opt/uv-python
# no PATH, sem symlink: por symlink o venv nao acha a biblioteca padrao do Python
ENV PATH=/opt/python/bin:$PATH
# pasta do volume compartilhado com o nginx; o volume herda o dono na primeira montagem
RUN mkdir -p /var/relatorios && chown jenkins:jenkins /var/relatorios
USER jenkins

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

COPY casc.yaml /var/jenkins_casc/casc.yaml
ENV CASC_JENKINS_CONFIG=/var/jenkins_casc/casc.yaml
ENV JAVA_OPTS=-Djenkins.install.runSetupWizard=false
