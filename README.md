# Grupo 15

- Integrantes:  Ariana Marchi, Catalina Gaitán, Nicolas Gonzalez, Santiago Lizondo
- Ayudante a cargo: Facundo Diaz

## URLs

- URL de aplicación de administración: [Link Admin](https://admin-grupo15.proyecto2023.linti.unlp.edu.ar/)
- URL del portal público: [Link Publico](https://grupo15.proyecto2023.linti.unlp.edu.ar/)

## Datos de la aplicación de admin
- Lenguajes utilizados: ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
- Frameworks: ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
- Estilos y motor de plantillas: ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)

## Datos de la aplicación del portal
- Lenguajes utilizados: ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
- Frameworks: ![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D) 
- Estilos: ![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white) 

## Instalación

- [Instalacion Admin](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2023/proyectos/grupo15/-/blob/main/admin/README.md?ref_type=heads)
- [Instalacion Portal](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2023/proyectos/grupo15/-/blob/main/portal/README.md?ref_type=heads)

## Librerias

- [Librerias Admin](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2023/proyectos/grupo15/-/blob/main/admin/README.md?ref_type=heads)
- [Librerias Portal](https://gitlab.catedras.linti.unlp.edu.ar/proyecto2023/proyectos/grupo15/-/blob/main/portal/README.md?ref_type=heads)

## Credenciales de prueba

SuperAdmin
- Correo: superAdmin@gmail.com
- Contraseña: admin

Dueño de: Rodriguez Ltd Inc
- Correo: laura@gmail.com
- Contraseña: 12345

Admininistrador de: Rodriguez Ltd Inc
- Correo: jorge@gmail.com
- Contraseña: 12345

Operario de: Rodriguez Ltd Inc
- Correo: ricarda44@hotmail.com
- Contraseña: 12345

## Base de Datos

### PostgreSQL nativo
- [Documentacion PostgreSQL](https://www.postgresql.org/docs/current/tutorial-start.html)
- Utilizar las siguientes credenciales:
  - Host: localhost
  - Port: 5432
  - User: grupo15
  - Password: 123
  - Database: grupo15_db

### Con Docker
```yml
version: '3.9'
services:
  db:
    image: postgres:alpine3.18
    ports:
      - "5432:5432"
    volumes:
      - .:/postgressDB/
    environment:
      - POSTGRES_USER=grupo15
      - POSTGRES_PASSWORD=123
      - POSTGRES_DB=grupo15_db
```
Guardar el archivo con el nombre "docker-compose.yml".
Posicionarse sobre el directorio donde esta el archivo y ejecutar:
```bash
  docker compose up
```

### Seeds Base de Datos
Ejecutar estos comandos (para resetear la base de datos y cargar datos de prueba):
```bash
cd admin
poetry shell
flask resetdb
flask seedsdb
```

## Coleccion de peticiones para la API
En los siguientes links se encuentran los archivos que se pueden importar el respectivo REST Client:
- Para Postman: [Link](https://drive.google.com/file/d/1UpeV8Xpr6AOz8gV9KaCRAVLHUa6ck0gm/view)
- Para la extensión de VSCode ThunderClient: [Link](https://drive.google.com/file/d/1007S0YT87-InqqoaWYnZahahncpinLCt/view)

