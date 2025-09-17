# Sistema de Puntuación tipo Duolingo

Este documento describe cómo estructurar e implementar un sistema de puntuación inspirado en Duolingo para practicantes, con un backend en Django (organizado por apps), un frontend en HTML/CSS/JS puro y una base de datos MySQL. La guía cubre objetivos, alcance, estructura del proyecto, responsabilidades por app, conexión a MySQL, flujo de datos y un roadmap de extensiones.

---

## 1) Descripción general del sistema

- **Objetivo**: Motivar hábitos de ingeniería mediante actividades puntuables (commits válidos, presentaciones en Sprint Review, puntualidad, completar sistemas), mostrando transparencia con un leaderboard y paneles de usuario.
- **Alcance inicial (MVP)**:
  - Ingreso manual de puntos por parte de un rol Admin.
  - Cálculo de ranking y KPIs a partir de datos persistidos en la base.
  - Vistas diferenciadas por rol (Admin/Practicante/Visor opcional).
  - Exportes a Excel y PDF desde reportes.
  - Periodos visibles Diario/Semanal/Quincenal.
- **Tecnologías**:
  - **Backend**: Django organizado por apps.
  - **Frontend**: HTML, CSS y JavaScript (sin frameworks externos).
  - **Base de datos**: MySQL.

---

## 2) Instalación y ejecución

### Requisitos previos

Antes de comenzar, asegúrate de tener instalados:

- Python 3.1x
- MySQL
- Pip (gestor de paquetes de Python)

### Pasos para la instalación

1. Clona este repositorio en tu máquina local:

    ```bash
    git clone https://github.com/Fabiano2503/Sistema-Puntuacion-v1.git
    cd Sistema-Puntuacion-v1
    ```

2. Crea un entorno virtual para aislar las dependencias:

    ```bash
    python -m venv .env
    ```

3. Activa el entorno virtual:

    - En Windows:

      ```bash
      .env\Scripts\activate
      ```

    - En macOS/Linux:

      ```bash
      source .env/bin/activate
      ```

4. Instala las dependencias necesarias:

    ```bash
    pip install -r requirements.txt
    ```

5. Configura la base de datos:  
   Abre `settings.py` en la carpeta `config` y ajusta las credenciales de MySQL (usuario, contraseña, nombre de la base de datos, etc.).

6. Realiza las migraciones para crear las tablas en la base de datos:

    ```bash
    python manage.py migrate
    ```

7. Crea un superusuario para acceder al panel de administración:

    ```bash
    python manage.py createsuperuser
    ```

8. Ejecuta el servidor de desarrollo:

    ```bash
    python manage.py runserver
    ```

¡Listo! Ahora puedes acceder a la aplicación en [http://localhost:8000/](http://localhost:8000/) en tu navegador.

---

## 3) Estado de la Integración Continua

[![Django CI](https://github.com/Fabiano2503/Sistema-Puntuacion-v1/actions/workflows/django.yml/badge.svg)](https://github.com/Fabiano2503/Sistema-Puntuacion-v1/actions/workflows/django.yml)

> El ícono anterior refleja el estado actual del pipeline de Integración Continua.  
> Si está en verde, todas las pruebas y checks pasan correctamente.

---

## 4) Estructura del proyecto Django

El proyecto sigue una estructura modular basada en apps, cada una con responsabilidades claras:

- **Raíz del proyecto Django**:
  - Configuración central (`settings.py`, `urls.py`, middlewares, etc.).
  - Conexión a MySQL.
  - Gestión de apps instaladas y autenticación.

- **Apps principales**:
  - `users`: Gestión de usuarios y roles.
  - `teams`: Administración de equipos.
  - `activities`: Registro de actividades y puntos.
  - `reports`: Exportes de datos en formatos Excel/PDF.
  - `dashboard`: Vista de leaderboard y KPIs.

---

## 5) Flujo de datos

1. El Admin ingresa una actividad desde el frontend.
2. El backend valida y persiste la actividad.
3. El servicio de agregaciones recalcula los totales por usuario y equipo.
4. El dashboard muestra el leaderboard, KPIs y panel "Mis puntos".
5. Los reportes permiten la exportación a Excel y PDF.

---

## 6) Frontend (HTML/CSS/JS sin frameworks)

El frontend consiste en páginas para login, dashboard, ingreso de puntos (solo Admin), reportes, usuarios y equipos. La interacción se realiza con JavaScript nativo para:

- Autenticación y manejo de roles.
- Consumo de datos del backend.
- Envío de formularios para registrar actividades y gestionar usuarios/equipos.
- Exportes de datos a Excel/PDF.

---

## 7) Seguridad y permisos

- Los endpoints y vistas respetan los roles: Admin, Practicante y Visor.
- Las operaciones de ABM de usuarios/equipos requieren permisos de Admin.
- Las vistas del frontend deben ocultar acciones no permitidas por el rol actual.

---

## 8) Extensiones futuras (roadmap)

- Flujo de aprobación: estados Pendiente/Aprobado/Rechazado para actividades.
- Notificaciones automáticas: envíos semanales y quincenales.
- Límites de puntuación: topes por tipo/periodo y validación de evidencia.
- Actividades de equipo: distribución de puntos entre miembros.
- Cierres automáticos: corte semanal/quincenal y publicación del ganador.

---

## 9) Checklist funcional (MVP)

- Credenciales y roles operativos.
- Ingreso de puntos impacta el ranking y los KPIs.
- Leaderboard y panel “Mis puntos” coherentes con el periodo seleccionado.
- ABM de Usuarios y Equipos disponible para Admin.
- Reportes con historial y exportación a Excel/PDF.

---

## 10) Consideraciones de despliegue

- Asegúrate de configurar las variables de entorno para las credenciales de MySQL y ajustes de seguridad.
- Ejecuta las migraciones para todas las apps.
- Verifica la zona horaria y localización.
- Archivos estáticos del frontend deben estar habilitados para cacheado controlado.