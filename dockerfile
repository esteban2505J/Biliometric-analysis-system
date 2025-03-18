# Usa una imagen oficial de Python
FROM python:3.10

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de tu proyecto al contenedor
COPY . .

# Comando por defecto al ejecutar el contenedor
CMD ["python", "main.py"]
