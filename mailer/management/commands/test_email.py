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

TO = "test@example.com"

TEMPLATES = [
    {
        "subject": "Bienvenida - Plataforma de gestión de tesis",
        "template": "email/01_tesis/4166489_DAnalytics_Education_Bienvenida_UV.html",
        "context": {
            "fullname": "Usuario",
            "articulo_nombre": "la",
            "entidad": "Universidad del Valle - Facultad de Ingeniería",
            "dominio": "https://univalle.danalytics-education.com/usuarios/acceso-por-correo",
        },
    },
    {
        "subject": "Recordatorio Jurados - Plataforma de gestión de tesis",
        "template": "email/01_tesis/4952275_DAnalytics_Education_Base_UV_ACCESO_DIRECTO_RECORDATORIO_JURADOS.html",
        "context": {
            "fullname": "Usuario",
            "articulo_nombre": "La",
            "entidad": "Universidad del Valle - Facultad de Ingeniería",
            "evento": "Evaluación de propuesta de trabajo de grado - Ingeniería de Sistemas",
            "url": "https://univalle.danalytics-education.com/usuarios/acceso-por-correo",
        },
    },
    {
        "subject": "Indicadores Semanales - Plataforma de gestión de tesis",
        "template": "email/01_tesis/4814302_DAnalytics_Education_Base_UV_INDICADORES_SEMANALES.html",
        "context": {
            "fullname": "Usuario",
            "fecha": "20 de abril de 2026",
            "entidad": "Universidad del Valle - Facultad de Ingeniería",
            "numero_total": "Total de trabajos pendientes: 3",
            "evento": [
                {
                    "programa": "Ingeniería de Sistemas",
                    "nombre": "Propuestas por revisar",
                    "valor": "5",
                    "codigo": "TG-2026-001"
                },
                {
                    "programa": "Ingeniería Industrial",
                    "nombre": "Sustentaciones pendientes",
                    "valor": "2",
                    "codigo": "TG-2026-015"
                },
                {
                    "programa": "Ingeniería Eléctrica",
                    "nombre": "Jurados por asignar",
                    "valor": "12",
                    "codigo": "TG-2026-023"
                }
            ],
            "url": "https://univalle.danalytics-education.com/usuarios/acceso-por-correo",
        },
    },
    {
        "subject": "Carta Jurado - Plataforma de gestión de tesis",
        "template": "email/01_tesis/4427808_DAnalytics_Education_Base_UV_CARTA_JURADO.html",
        "context": {
            "url": "https://univalle.danalytics-education.com/usuarios/acceso-por-correo",
        },
    },
]

# ============================================================

class Command(BaseCommand):
    help = "Envia correos de prueba usando Gmail API OAuth 2.0"

    def handle(self, *args, **options):
        gmail = GmailOAuth()
        enviados = 0
        errores = 0

        for tpl in TEMPLATES:
            self.stdout.write(f"\nEnviando: {tpl['subject']}")
            try:
                html = render_to_string(tpl["template"], tpl["context"])
                message_id = gmail.enviar(to=TO, subject=tpl["subject"], html=html)
                self.stdout.write(
                    self.style.SUCCESS(f"  [OK] Enviado. ID: {message_id}")
                )
                enviados += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"  [FAIL] Error: {e}")
                )
                errores += 1

        self.stdout.write(f"\nResumen: {enviados} enviados, {errores} errores")

