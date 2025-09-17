### Sistema de Puntuación tipo Duolingo — README del Proyecto

Este documento describe, en redacción y sin fragmentos de código, cómo estructurar e implementar un sistema de puntuación inspirado en Duolingo para practicantes, con un backend en Django (organizado por apps), un frontend en HTML/CSS/JS puro y una base de datos MySQL. La guía cubre objetivos, alcance, estructura del proyecto, responsabilidades por app, conexión a MySQL, flujo de datos y un roadmap de extensiones.

---

## 1) Descripción general del sistema

- **Objetivo**: Motivar hábitos de ingeniería mediante actividades puntuables (commits válidos, presentaciones en Sprint Review, puntualidad, completar sistemas), mostrando transparencia con un leaderboard y paneles de usuario. Se busca rapidez de validación con una UX clara y exportes básicos.
- **Alcance inicial (MVP)**:
  - Ingreso manual de puntos por parte de un rol Admin.
  - Cálculo de ranking y KPIs a partir de datos persistidos en la base.
  - Vistas diferenciadas por rol (Admin/Practicante/Visor opcional) en el frontend.
  - Exportes a Excel y PDF desde reportes.
  - Periodos visibles Diario/Semanal/Quincenal (etiquetados y filtros de rango de fechas).
- **Tecnologías**:
  - **Backend**: Django organizado por apps (recomendable agregar API REST con DRF para servir datos al frontend sin frameworks).
  - **Frontend**: HTML, CSS y JavaScript sin frameworks externos (solo librerías de terceros vía CDN para exportes si se desea, p. ej. SheetJS, jsPDF).
  - **Base de datos**: MySQL.

---

## 2) Estructura del proyecto Django

Se recomienda una arquitectura por apps, cada una encapsulando su dominio. A nivel alto, el proyecto debe contemplar:

- Carpeta raíz del proyecto Django con:
  - Configuración central (`settings`, `urls`, middlewares, variables de entorno, templates base si aplica).
  - Gestión de conexión a MySQL (credenciales, host, puerto, nombre de BD, charset, tz).
  - Configuración de apps instaladas y autenticación.
- Apps principales (modulares y desacopladas): `users`, `teams`, `activities`, `reports`, `dashboard`.
- Separación de capas dentro de cada app (conceptual):
  - Modelos y reglas de persistencia.
  - Servicios de dominio (cálculos, recálculos, agregaciones, validaciones de negocio que no sean triviales).
  - Vistas/controladores (endpoints o vistas server-side) que orquestan peticiones y respuestas.
  - Serialización/transformación para exponer datos al frontend (si se usa API REST).
  - Tareas programadas (si aplica en futuras iteraciones; p. ej. notificaciones).

El frontend se servirá como un conjunto de archivos estáticos (HTML/CSS/JS) que consumen los datos del backend vía endpoints o vistas. No se emplean frameworks de frontend; la interacción será con JavaScript nativo.

---

## 3) Apps recomendadas y responsabilidades

Las siguientes apps segmentan el dominio para mantener claridad y escalabilidad.

### 3.1) `users`

- **Propósito**: Gestionar usuarios del sistema y su ciclo de vida.
- **Responsabilidades**:
  - Gestión de cuentas: creación, edición, desactivación y eliminación de usuarios.
  - Manejo de **roles**: Admin, Practicante y (opcional) Visor; restricciones de acceso por rol.
  - Autenticación y autorización: inicio/cierre de sesión, recuperación de contraseña, políticas mínimas de seguridad.
  - Relación con equipos (vía `teams`) y con actividades registradas (vía `activities`).
  - Exposición de datos propios del usuario para el panel “Mis puntos”.
  - Integración con el sistema de permisos de Django para resguardar endpoints y vistas.

### 3.2) `teams`

- **Propósito**: Administrar equipos y mantener agregados de puntos por equipo.
- **Responsabilidades**:
  - Alta, edición y eliminación de equipos.
  - Asignación de usuarios a equipos y sincronización de relación usuario–equipo.
  - Cálculo y recálculo de puntos totales por equipo (acumulados desde `activities`).
  - Exposición de listados de equipos con totales, promedios y métricas básicas.
  - Reglas para cambios de equipo y su impacto en totales históricos (decidir política en la app: mover histórico o conservarlo por periodo).

### 3.3) `activities`

- **Propósito**: Mantener el catálogo de tipos de actividad y registrar la “bitácora” de puntos.
- **Responsabilidades**:
  - Catálogo de actividades con reglas de puntuación base (p. ej., commit válido 4 pts, presentación 4 pts, puntualidad 1 pt, completar sistema 16 pts).
  - Registro de actividades: usuario, tipo, fecha/hora, evidencia (texto/URL), notas; cálculo de puntos derivados del tipo seleccionado.
  - Historial de actividades consultable con filtros por periodo (diario/semanal/quincenal/personalizado), usuario y equipo.
  - Políticas de edición/corrección: permitir ajustes por Admin, dejando trazas de cambios en futuras extensiones.
  - Agregaciones por usuario y por equipo para alimentar `dashboard` y `reports`.
  - Validaciones de negocio imprescindibles (en esta versión, mínimas; validaciones más estrictas quedarán para el roadmap).

### 3.4) `reports`

- **Propósito**: Exponer reportes y exportes en formatos ofimáticos.
- **Responsabilidades**:
  - Reportes de historial de actividades, métricas agregadas y usuarios activos.
  - Exportación a **Excel** y **PDF** a partir de datos consultados (el backend puede generar archivos o el frontend puede exportar desde los datos recibidos).
  - Filtros por periodo y criterios (usuario, equipo, tipo de actividad) con paginación si es necesario.
  - Endpoints/vistas para descargar archivos y metadatos de reportes.

### 3.5) `dashboard`

- **Propósito**: Proveer datos del leaderboard y KPIs, además de la vista personalizada por usuario.
- **Responsabilidades**:
  - Cálculo del ranking por periodo y ordenación por puntos (con desempates definidos si aplica).
  - Exposición de KPIs: puntos totales del periodo, posición del usuario autenticado, conteo de actividades.
  - Panel “Mis puntos”: desglose por tipo de actividad y total acumulado en el periodo.
  - Indicadores de periodo: Diario, Semanal y Quincenal, incluyendo días restantes para quincena (cómputo por rango de fechas definido).
  - Consistencia con `activities` para que cualquier alta/edición impacte de inmediato en los resultados consultados.

---

## 4) Conexión a MySQL

La configuración de base de datos se realiza en la configuración central del proyecto. Debe incluir:

- Motor MySQL, host, puerto, nombre de la base, usuario y contraseña.
- Charset/colación adecuados y zona horaria consistente (por ejemplo, America/Lima).
- Parámetros de conexión y “pooling” si aplica.
- Gestión de variables de entorno para no exponer credenciales.

No se requiere mostrar código aquí; basta con asegurar que el entorno de ejecución carga correctamente las credenciales y que las migraciones de cada app están contempladas.

---

## 5) Flujo de datos (de la carga de puntos al dashboard)

1. Un **Admin** registra una actividad desde el frontend (tipo, usuario, fecha/hora, evidencia y notas); el formulario obtiene el puntaje estimado según el tipo.
2. El **backend** valida la solicitud mínima y persiste la actividad en `activities` (registro en el historial y cálculo de puntos asociados). Opcionalmente, registra la relación con equipo a través del usuario.
3. El servicio de **agregaciones** recalcula totales por usuario y por equipo (puede ser on-the-fly en consultas o pre-agrupado para eficiencia; en MVP se puede calcular en consulta).
4. El **dashboard** consulta los datos agregados y muestra:
   - Leaderboard por periodo (ranking de usuarios con puntos y número de actividades).
   - KPIs globales del periodo y “Mi posición” para el usuario autenticado.
   - Panel “Mis puntos” con desglose por tipo de actividad.
5. Los **reportes** consumen las mismas fuentes para historial y estadísticas y permiten exportar a Excel/PDF.

Este flujo debe reflejarse en tiempo cercano al real: tras guardar una actividad válida, las vistas de dashboard y reportes deben incorporar el cambio al consultar nuevamente la API o refrescar la vista.

---

## 6) Frontend (HTML/CSS/JS sin frameworks)

- **Estructura**: páginas o secciones para Login, Dashboard, Ingresar Puntos (solo Admin), Reportes, Usuarios (Admin) y Equipos (Admin).
- **Interacción**: JavaScript nativo para:
  - Autenticación (inicio/cierre de sesión) y manejo de rol para mostrar/ocultar secciones.
  - Consumo de endpoints del backend para listar ranking, KPIs, historial, usuarios y equipos.
  - Envío de formularios para registrar actividades y ABM de usuarios/equipos.
  - Exportes activados desde la UI, ya sea descargando archivos generados por el backend o construyéndolos en el navegador a partir de datos recibidos.
- **Accesibilidad y responsive**: estilos con buen contraste y diseño adaptable.

---

## 7) Reglas y periodos de cálculo

- **Tipos de actividad** (configurables en catálogo):
  - Commit válido, Presentación en Sprint Review, Llegar temprano, Completar un sistema.
- **Periodos**: Diario, Semanal y Quincenal. Se definen como rangos de fechas consultados por las vistas/resultados.
- **Desempates** (si se requiere): número de actividades únicas, días con actividad, conteo de puntualidad u otro criterio documentado.
- **Políticas mínimas**: la evidencia puede ser opcional en MVP; validaciones más estrictas se reservan para el roadmap.

---

## 8) Seguridad y permisos

- Los endpoints y vistas deben respetar los **roles**: Admin (acceso total a gestión y carga), Practicante (consulta de dashboard y reportes), Visor (lectura de dashboards/reportes).
- Las operaciones de ABM de usuarios/equipos y la carga/corrección de actividades requieren permisos de Admin.
- Las vistas del frontend deben ocultar acciones no permitidas al rol vigente, sin reemplazar la verificación real en el backend.

---

## 9) Métricas clave y UX

- **Leaderboard**: posición, nombre, equipo, puntos y número de actividades.
- **KPIs**: puntos totales del periodo, posición personal, días restantes en quincena.
- **Panel personal**: desglose por tipo de actividad y total.
- **Reportes**: historial con filtros, estadísticas agregadas, exportación a Excel/PDF.

---

## 10) Extensiones futuras (roadmap)

- **Flujo de aprobación**: estados Pendiente/Aprobado/Rechazado para actividades, con bitácora de auditoría.
- **Notificaciones automáticas**: envíos semanales y quincenales (correo/Slack) en zona horaria definida.
- **Límites de puntuación**: topes por tipo/periodo, detección de duplicados y validación de evidencia.
- **Actividades de equipo**: distribución de puntos de “completar sistema” entre miembros o prorrateo parametrizable.
- **Cierres automáticos**: corte semanal/quincenal y publicación del ganador.
- **Reportes avanzados**: generación del lado servidor con filtros y paginación.

---

## 11) Checklist funcional (MVP)

- Credenciales y roles operativos.
- Ingreso de puntos por Admin impacta ranking y KPIs.
- Leaderboard y panel “Mis puntos” coherentes con el periodo seleccionado.
- ABM de Usuarios y Equipos disponible para Admin.
- Reportes con historial y exportación a Excel/PDF.

---

## 12) Consideraciones de despliegue

- Variables de entorno para credenciales MySQL y ajustes de seguridad.
- Migraciones ejecutadas para todas las apps.
- Revisión de zona horaria y localización.
- Archivos estáticos del frontend servidos correctamente y habilitados para cacheado controlado.


