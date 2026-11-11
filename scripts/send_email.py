
import os
import sys
import smtplib
from email.message import EmailMessage


def enviar_email(resultado):
    destinatario = os.getenv("EMAIL_TO")
    smtp_host = os.getenv("SMTP_HOST", "localhost")
    smtp_port = int(os.getenv("SMTP_PORT", "1025"))

    if not destinatario:
        raise ValueError(
            "A variavel de ambiente EMAIL_TO nao foi configurada."
        )

    numero_build = os.getenv("BUILD_NUMBER", "N/A")
    nome_job = os.getenv("JOB_NAME", "Restful Booker")
    url_build = os.getenv("BUILD_URL", "N/A")

    mensagem = EmailMessage()

    mensagem["From"] = "jenkins@restful-booker.local"
    mensagem["To"] = destinatario
    mensagem["Subject"] = (
        f"[Jenkins] Build #{numero_build} - {resultado}"
    )

    mensagem.set_content(f"""
O pipeline do projeto Restful Booker foi finalizado.

Projeto: {nome_job}
Build: #{numero_build}
Resultado: {resultado}

Acesse os detalhes da execucao:
{url_build}

Mensagem automatica do Jenkins.
""")

    with smtplib.SMTP(
        smtp_host,
        smtp_port,
        timeout=10
    ) as servidor:
        servidor.send_message(mensagem)

    print(f"E-mail enviado com sucesso para {destinatario}")


def main():
    if len(sys.argv) != 2:
        print("Uso: python send_email.py SUCCESS ou FAILURE")
        return 1

    resultado = sys.argv[1].upper()

    if resultado not in ("SUCCESS", "FAILURE"):
        print("Resultado invalido.")
        return 1

    try:
        enviar_email(resultado)
        return 0

    except Exception as erro:
        print(f"Falha ao enviar e-mail: {erro}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
