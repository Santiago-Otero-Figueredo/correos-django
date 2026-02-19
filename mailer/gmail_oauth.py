"""
Logica de autenticacion OAuth 2.0 y envio de correos via Gmail API.
"""

import base64
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# ============================================================
# CREDENCIALES - Edita estos valores
# ============================================================

SENDER_EMAIL = "tu-correo@gmail.com"
OAUTH_CLIENT_SECRETS = "credentials/oauth2.json"
OAUTH_TOKEN_FILE = "credentials/oauth_token.json"


# ============================================================

class GmailOAuth:
    """Cliente Gmail API con autenticacion OAuth 2.0 (Client ID)."""

    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

    def __init__(self):
        self.sender_email = SENDER_EMAIL
        self.client_secrets = OAUTH_CLIENT_SECRETS
        self.token_file = OAUTH_TOKEN_FILE
        self._service = None

    def _obtener_credenciales(self):
        """
        Carga, refresca o genera token OAuth 2.0.

        - Si existe oauth_token.json lo reutiliza.
        - Si el token expiro lo refresca automaticamente.
        - Si no hay token, inicia el flujo OAuth (muestra URL para abrir en navegador).

        Returns:
            Objeto Credentials listo para usar.

        Raises:
            FileNotFoundError: Si no se encuentra oauth2.json.
            ValueError: Si el archivo no tiene formato OAuth 2.0 valido.
        """
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow

        if not os.path.exists(self.client_secrets):
            raise FileNotFoundError(
                f"No se encontro el archivo de credenciales: {self.client_secrets}\n"
                "Descargalo desde Google Cloud Console > APIs y Servicios > Credenciales."
            )

        with open(self.client_secrets) as f:
            raw = json.load(f)

        if "web" not in raw and "installed" not in raw:
            raise ValueError(
                f"El archivo {self.client_secrets} no es un OAuth 2.0 Client ID. "
                "Debe contener la clave 'web' o 'installed'."
            )

        creds = None

        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Token expirado, renovando...")
                creds.refresh(Request())
            else:
                print("Iniciando flujo OAuth 2.0...")
                print("Copia la URL que aparece abajo y pegala en tu navegador.\n")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets, self.SCOPES
                )
                creds = flow.run_local_server(port=8080, open_browser=False)

            os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
            with open(self.token_file, "w") as f:
                f.write(creds.to_json())
            print(f"Token guardado en {self.token_file}")

        return creds

    def _get_service(self):
        """Obtiene o crea el servicio de Gmail API (singleton)."""
        if self._service is None:
            from googleapiclient.discovery import build

            creds = self._obtener_credenciales()
            self._service = build("gmail", "v1", credentials=creds)
        return self._service

    def enviar(self, to: str, subject: str, html: str) -> str:
        """
        Construye un mensaje MIME y lo envia via Gmail API.

        Args:
            to: Correo del destinatario.
            subject: Asunto del correo.
            html: Cuerpo en HTML.

        Returns:
            ID del mensaje enviado.

        Raises:
            Exception: Si la API retorna un error.
        """
        mensaje = MIMEMultipart("alternative")
        mensaje["From"] = self.sender_email
        mensaje["To"] = to
        mensaje["Subject"] = subject
        mensaje.attach(MIMEText(html, "html", "utf-8"))

        raw = base64.urlsafe_b64encode(mensaje.as_bytes()).decode("utf-8")

        service = self._get_service()
        result = service.users().messages().send(
            userId="me",
            body={"raw": raw},
        ).execute()

        return result["id"]
