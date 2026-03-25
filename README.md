# 🛒 Sistema de Gestión Comercial + Catálogo Web (Django)

Aplicación web desarrollada con **Django y Django REST Framework** para la gestión integral de una distribuidora de artículos de gomería.

El sistema combina una **landing pública con catálogo de productos** y un **panel interno de gestión**, permitiendo centralizar operaciones comerciales y mejorar la atención al cliente.

---

## 🚀 Funcionalidades principales

### 🌐 Frontend / Landing
- Catálogo de productos con imágenes
- Navegación por categorías
- Visualización optimizada para clientes
- Enlace directo a WhatsApp para consultas rápidas

### 🔐 Panel de gestión (backend)
- Gestión completa de artículos con imágenes
- Control de stock en tiempo real
- Movimientos de stock manuales
- Registro y gestión de ventas
- Generación e impresión de presupuestos
- Administración de datos comerciales

### 🔄 API REST (Django REST Framework)
- Endpoints para consultas asincrónicas
- Integración frontend-backend
- Manejo eficiente de datos

---

## 🛠 Tecnologías utilizadas

- **Backend:** Python, Django, Django REST Framework  
- **Frontend:** HTML, CSS, Bootstrap  
- **Base de datos:** MySQL  
- **Otros:** Integración con WhatsApp, manejo de imágenes (Cloudinary)

---

## 🎯 Objetivo del proyecto

Desarrollar una solución completa para negocios que necesitan:

- Centralizar su gestión comercial  
- Controlar stock y ventas  
- Mostrar productos online  
- Facilitar el contacto con clientes  

---

## 📸 Capturas (recomendado agregar)

<!-- Agregar screenshots del sistema -->
- Catálogo público
- Panel de administración
- Vista de productos
- Generación de presupuestos

---

## ⚙️ Instalación (modo desarrollo)

```bash
git clone https://github.com/MarianoDjango/sistema-distribuidora-django.git
cd tu-repo

python -m venv venv
source venv/bin/activate  # o venv\\Scripts\\activate en Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
