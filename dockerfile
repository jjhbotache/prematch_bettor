# Usar una imagen base de Python
FROM python:3.12.3

# Copiar el script de Python al contenedor
ADD /python /python
ADD requirements.txt /

# instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Establecer el directorio de trabajo
WORKDIR /

# Ejecutar el script de Python
CMD ["python", "python/scrape.py"]
