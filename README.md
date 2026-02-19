# correos-django

Herramienta para enviar correos HTML desde Django usando Gmail API con OAuth 2.0.
El flujo principal es: editar variables en el comando → ejecutar → revisar el correo recibido.

---

## Requisitos

- Python 3.9+
- Credenciales de Gmail API en `credentials/` (ver `.env.example`)
- Dependencias instaladas: `pip install -r requirements.txt`

---

## Comando de prueba

```bash
python manage.py test_email
```

Carga el template configurado, lo renderiza con el contexto definido y lo envía por Gmail API.

---

## Variables de configuración

Todas se editan al inicio de `mailer/management/commands/test_email.py`:

```python
TO              = "destinatario@email.com"   # A quién se envía
NOMBRE          = "Usuario"                  # Variable disponible en el template
SUBJECT         = "Asunto del correo"        # Asunto

TEMPLATE_FOLDER = "01_tesis"                 # Carpeta dentro de templates/email/
TEMPLATE_NAME   = "prueba.html"              # Archivo HTML dentro de esa carpeta
```

El template que se carga es siempre:

```
templates/email/{TEMPLATE_FOLDER}/{TEMPLATE_NAME}
```

---

## Estructura de templates

```
templates/
└── email/
    ├── 01_tesis/
    ├── 02_semilleros/
    ├── 03_acompañate/
    ├── 04_curriculos/
    └── 99_otros/
```

Cada carpeta corresponde a una categoría de correo. Dentro de cada una puedes tener varios archivos HTML con distintos diseños o versiones.

---

## Probar templates uno por uno

### Cambiar de carpeta

Para probar los templates de otra categoría, cambia `TEMPLATE_FOLDER`:

```python
TEMPLATE_FOLDER = "02_semilleros"
```

### Cambiar de template dentro de la misma carpeta

Si una carpeta tiene varios templates, cambia solo `TEMPLATE_NAME`:

```python
TEMPLATE_FOLDER = "01_tesis"
TEMPLATE_NAME   = "<codigo-mailjet-1>_<nombre-maijet-1>.html"   # primer diseño
```

```python
TEMPLATE_FOLDER = "01_tesis"
TEMPLATE_NAME   = "<codigo-mailjet-2>_<nombre-maijet-2>.html"   # segundo diseño
```

Ejemplo de flujo para revisar todos los templates de una carpeta:

```
templates/email/01_tesis/
├── bienvenida.html
├── recordatorio.html
└── resultado.html
```

```python
# Iteración 1
TEMPLATE_NAME = "<codigo-mailjet-n>_<nombre-maijet-n>.html"
# → python manage.py test_email → revisar correo

```

---

## Variables disponibles en los templates

El diccionario `context` en el comando define qué datos recibe el template:

```python
context = {
    "nombre":  NOMBRE,
    "mensaje": "Este es un correo de prueba...",
    "items": [
        "Autenticacion: OAuth 2.0 Client ID",
        "Framework: Django",
    ],
}
```

| Variable  | Descripción                |
| --------- | -------------------------- |
| `nombre`  | Nombre del destinatario    |
| `mensaje` | Texto principal del correo |
| `items`   | Lista de puntos (opcional) |

Ejemplo de uso en el HTML:

```html
<p>Hola, {{ nombre }}.</p>
<p>{{ mensaje }}</p>

{% if items %} {% for item in items %}
<p>• {{ item }}</p>
{% endfor %} {% endif %}
```

### Agregar o quitar variables

Para pasar datos nuevos al template, añade la clave al diccionario `context`:

```python
context = {
    "nombre":   NOMBRE,
    "mensaje":  "Texto del correo.",
    "items":    ["punto 1", "punto 2"],
    "fecha":    "2026-02-19",          # variable nueva
    "programa": "Ingeniería de Sistemas",
}
```

Y úsala en el HTML con `{{ nombre_variable }}`:

```html
<p>Programa: {{ programa }}</p>
<p>Fecha: {{ fecha }}</p>
```

Para quitar una variable que el template no necesite, elimínala del `context`. Si el template la referencia con `{% if variable %}` no romperá nada; si la usa directamente sin guard puede quedar en blanco.
