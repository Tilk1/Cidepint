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


## Instalación y ejecucion en entorno de desarrollo
En caso de no tener poetry instalado
```bash
pip install poetry
```
Instalar version de python 3.8 o superior en caso de no poseer
```bash
pip install pyenv
pyenv install 3.8
pyenv global 3.8
```
Una vez posicionado en el directorio activar el entorno virtual y usar poetry para instalar dependencias
```bash
cd admin
poetry install
```
Para activar entorno y ejecutar
```bash
poetry shell
flask run
```

## Librerias
```bash
python = "^3.8"
flask = "^2.3.3"
psycopg2-binary = "^2.9.7"
flask-sqlalchemy = "^3.1.1"
flask-mail = "^0.9.1"
flask-session = "^0.5.0"
flask-bcrypt = "^1.0.1"
jsonfy = "^0.4"
faker = "^19.6.2"
flask-cors = "^4.0.0"
flask-jwt-extended = "^4.5.3"
authlib = "^1.2.1"
requests = "^2.31.0"
pyopenssl = "^23.3.0"
geopy = "^2.4.0"
```



