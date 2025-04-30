

# 🧠 backend-Andina Trading

Proyecto base con FastAPI para levantar una API localmente.

## 🚀 Instalación

1. Clona el repositorio y entra al directorio del proyecto:

```bash
   git clone <URL-del-repo>
   cd backend-at
   ```
1.1 Si es linux se debe de activar el entorno del proyeceto:

```bash
  source venv/bin/activate
   ```

1.2 Si es windows se ejecuta con conda


2. Crea y activa el entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias necesarias:


   ```bash
      pip install fastapi uvicorn autopep8 python-multipart
   ```

## ▶️ Ejecución del servidor

Con el entorno virtual activado, ejecuta:

```bash
   uvicorn main:app --reload
```

Esto levantará el servidor en `http://127.0.0.1:8000`.

## 🧪 Endpoints de prueba

- Documentación interactiva: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Documentación alternativa: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
```
