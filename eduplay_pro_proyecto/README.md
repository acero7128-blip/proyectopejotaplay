# EduPlay Pro - Plataforma Web de Juegos Educativos

Plataforma web interactiva de juegos educativos bajo modelo de suscripción mensual ($5 USD pagaderos en Bolívares a la Tasa Oficial del BCV del día), desarrollada en Python (Flask), SQLite, HTML5, CSS3 y JavaScript Vanilla.

## Características Principales
1. **Gestión de Usuarios:** Registro e inicio de sesión seguro con contraseñas encriptadas (hashing).
2. **Gestión de Suscripciones y Pagos Manuales:**
   - Estados controlados: `inactive`, `pending`, `active`, `cancelled`.
   - Reporte de pago con número de referencia tras enviar el soporte a los canales autorizados:
     - Correo: `angelcontrerasoficial@gmail.com` / `profesorangeloficial@gmail.com`
     - WhatsApp: `+58 04168029177` / `+58 04129006008`
   - Opción de cancelación inmediata desde el perfil del usuario.
3. **Catálogo Estricto de 3 Juegos Educativos (Exclusivo para usuarios Activos):**
   - **Matemática Básica:** Desafíos numéricos de agilidad mental (sumas, restas, multiplicaciones y divisiones simples).
   - **Ortografía:** Ejercicios interactivos de completar palabras, uso de b/v, c/s/z y tildes.
   - **Geografía de Venezuela:** Trivia interactiva sobre estados, capitales, relieves, ríos y símbolos naturales del país.

## Instalación y Ejecución
1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar el servidor:
   ```bash
   python app.py
   ```
3. Abrir en el navegador: `http://127.0.0.1:5000`
