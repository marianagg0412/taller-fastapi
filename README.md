# PASOS PARA EJECUTAR EL PROYECTO:

*Notas preliminares:* 
- Asegúrese de clonar correctamente el proyecto de git. Se recomienda `git clone <URL>`. 
- Su máquina debe tener python3 instalado de manera global.
- La base de datos usada está en la nube (neontech). Los datos allí contenidos corresponden al archivo `calendar.csv`. Si se desea validar su funcionamiento, se puede ejecutar el archivo SQL `inserts.sql` en una base de datos local.

## Pasos para la instalación
1. Instalar la librería "dos2unix" de manera global y ejecutar el comando: `dos2unix setting-up.bash`.
2. Crear el entorno virtual dedicado para este proyecto.
3. Si usted tiene la carpeta bin, ejecute el archivo setting-up.bash con 
```bash
 bash setting-up.bash
 ```

## Ejecución
1. Cree el archivo .env y configure las variables de entorno del `DB_URL`, `PORT`, `HOST` y `BASE_URL`.
2. Si desea probar los endpoints, ejecute main.py. En su navegador ingrese: `http://localhost:{PORT}/docs` para poder realizarlo.
3. Si desea realizar las pruebas, ejecutar el archivo testing-endpoints.
4. Habilitar systemd en WSL. Ubique el archivo `fastapi_taller.service` en `/etc/systemd/system/` y
    ejecutar los comandos:
    - Recargar los servicios de systemd:`sudo systemctl daemon-reload`
    -  Iniciar el servicio: `sudo systemctl start fastapi_prueba`
    - Habilitar el servicio para que se inicie al arrancar el sistema: `sudo systemctl enable fastapi_prueba`
    - Verificar el estado del servicio: `sudo systemctl status fastapi_prueba`
    - Parar el servicio: `sudo systemctl stop fastapi_prueba`
5. Ubique el archivo `ngrok-fastapi.service` en el mismo directorio anterior. Asegúrese de cambiar el `<token>` por sus credenciales y ejecute los comandos modificando el nombre de `fastapi_taller` a `ngrok-fastapi` del paso 4.
6. Para probar el servicio local, la URL seguirá siendo la misma: `http://localhost:{PORT}/docs`.
7. Para probar el servicio en ngrok, ingrese a su cuenta de ngrok para obtener el URL. Copie el URL a portapapeles y peguelo en su navegador. Agregue al final `/docs`.