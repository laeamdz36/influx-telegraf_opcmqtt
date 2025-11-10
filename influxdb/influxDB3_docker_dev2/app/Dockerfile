FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos de la aplicación
COPY writer.py influx_setup.py run.py ./

# Comando por defecto: ejecutar el bootstrap y luego el writer
CMD ["python", "run.py"]
