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

TO = "hinatadeross@gmail.com"
SUBJECT = "Notificación de Sistema - Universidad del Valle"

# Carpeta del template a usar. Opciones:
#   01_tesis | 02_semilleros | 03_acompañate | 04_curriculos | 99_otros
TEMPLATE_FOLDER = "01_tesis"
TEMPLATE_NAME = "3665005_DAnalytics_Education_Plantilla_Base.html"


# ============================================================

class Command(BaseCommand):
    help = "Envia un correo de prueba usando Gmail API OAuth 2.0"

    def handle(self, *args, **options):
        self.stdout.write(f"Preparando correo para: {TO}")

        context = {
            "siglas": "PGT",
            "asunto": "Actualización del Sistema de Gestión de Tesis",
            "evento": "Se han abierto las inscripciones para el nuevo período académico",
            "dominio": "https://tesis.univalle.edu.co/",
            "entidad": "Escuela de Ingeniería Eléctrica y Electrónica - Universidad del Valle"
        }

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