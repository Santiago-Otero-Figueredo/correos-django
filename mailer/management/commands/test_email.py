"""
Management command para probar el envio de correos via Gmail API OAuth 2.0.

Uso:
    python manage.py test_email
"""

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string

from mailer.gmail_oauth import GmailOAuth


# ============================================================
# VARIABLES DE PRUEBA - Edita estos valores
# ============================================================

TO = "correoprueba@gmail.com"
NOMBRE = "Usuario"
SUBJECT = "Correo de prueba - Django"

# Carpeta del template a usar. Opciones:
#   01_tesis | 02_semilleros | 03_acompañate | 04_curriculos | 99_otros
TEMPLATE_FOLDER = "01_tesis"
TEMPLATE_NAME = "5668329_Notificaciones_Dexia.html"


# ============================================================

class Command(BaseCommand):
    help = "Envia un correo de prueba usando Gmail API OAuth 2.0"

    def handle(self, *args, **options):
        self.stdout.write(f"Preparando correo para: {TO}")

        context = {}

        html = render_to_string(f"email/{TEMPLATE_FOLDER}/{TEMPLATE_NAME}", context)

        try:
            gmail = GmailOAuth()
            message_id = gmail.enviar(to=TO, subject=SUBJECT, html=html)
            self.stdout.write(
                self.style.SUCCESS(f"Correo enviado exitosamente. ID: {message_id}")
            )
        except FileNotFoundError as e:
            raise CommandError(str(e))
        except Exception as e:
            raise CommandError(f"Error al enviar el correo: {e}")
