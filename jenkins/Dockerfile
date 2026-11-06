FROM jenkins/jenkins:2.580.2-lts-jdk21

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-venv \
    && rm -rf /var/lib/apt/lists/*
USER jenkins

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

COPY casc.yaml /var/jenkins_casc/casc.yaml
ENV CASC_JENKINS_CONFIG=/var/jenkins_casc/casc.yaml
ENV JAVA_OPTS=-Djenkins.install.runSetupWizard=false
