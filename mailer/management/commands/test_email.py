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

TO = "sebastianmarulandapsg@gmail.com"
NOMBRE = "Usuario"
SUBJECT = "Correo de prueba - Django"

# Carpeta del template a usar. Opciones:
#   01_tesis | 02_semilleros | 03_acompañate | 04_curriculos | 99_otros
TEMPLATE_FOLDER = "02_semilleros"
TEMPLATE_NAME = "7300879_Notificacion_desvinculacion_al_estudiante_aprobacion.html"


# ============================================================

class Command(BaseCommand):
    help = "Envia un correo de prueba usando Gmail API OAuth 2.0"

    def handle(self, *args, **options):
        self.stdout.write(f"Preparando correo para: {TO}")

        context = {
            "nombre": NOMBRE,
            "nombre_estudiante": "Sebastian Marulanda",
            "nombre_semillero": "Semillero de Inteligencia Artificial aplicada a la Salud (SIAS)",
            "mensaje": "Este es un correo de prueba enviado desde Django usando Gmail API con OAuth 2.0.",
            "items": [
                "Autenticacion: OAuth 2.0 Client ID",
                "Framework: Django",
                "API: Gmail API v1",
                "Template: Django Templates",
            ],
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
