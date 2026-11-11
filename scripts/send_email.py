
import os
import sys
import smtplib
from email.message import EmailMessage


def send_email(status):
    # Configurações SMTP
    smtp_host = os.getenv("SMTP_HOST", "mailpit")
    smtp_port = int(os.getenv("SMTP_PORT", "1025"))

    # Destinatário
    email_to = os.getenv("EMAIL_TO", "").strip()

    # Dados da execução do Jenkins
    job_name = os.getenv("JOB_NAME", "restful-booker")
    build_number = os.getenv("BUILD_NUMBER", "N/A")
    build_url = os.getenv("BUILD_URL", "")

    # Sem destinatário, a notificação é ignorada explicitamente.
    if not email_to:
        print(
            "AVISO: EMAIL_TO não configurado. "
            "Notificação por e-mail ignorada."
        )
        return

    # Permite múltiplos destinatários separados por vírgula ou ponto e vírgula.
    recipients = [
        address.strip()
        for address in email_to.replace(";", ",").split(",")
        if address.strip()
    ]

    if not recipients:
        print("AVISO: Nenhum destinatário válido configurado.")
        return

    # Define assunto e mensagem conforme o resultado da pipeline.
    if status == "SUCCESS":
        subject = f"[Jenkins] SUCESSO - {job_name} #{build_number}"
        message = (
            "A pipeline foi executada com sucesso!\n\n"
            f"Projeto: {job_name}\n"
            f"Build: #{build_number}\n"
            "Resultado: SUCCESS\n"
        )

    elif status == "FAILURE":
        subject = f"[Jenkins] FALHA - {job_name} #{build_number}"
        message = (
            "A pipeline apresentou uma falha durante sua execução.\n\n"
            f"Projeto: {job_name}\n"
            f"Build: #{build_number}\n"
            "Resultado: FAILURE\n"
        )

    else:
        subject = f"[Jenkins] {status} - {job_name} #{build_number}"
        message = (
            "A pipeline foi finalizada.\n\n"
            f"Projeto: {job_name}\n"
            f"Build: #{build_number}\n"
            f"Resultado: {status}\n"
        )

    if build_url:
        message += f"\nAcesse os detalhes da execução:\n{build_url}\n"

    # Monta o e-mail.
    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = os.getenv("EMAIL_FROM", "jenkins@localhost")
    email["To"] = ", ".join(recipients)
    email.set_content(message)

    # Envia o e-mail.
    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.send_message(email)

        print(f"E-mail enviado com sucesso para: {', '.join(recipients)}")

    except (OSError, smtplib.SMTPException) as error:
        print(f"ERRO ao enviar e-mail: {error}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/send_email.py <SUCCESS|FAILURE>")
        sys.exit(1)

    build_status = sys.argv[1].upper()
    send_email(build_status)
