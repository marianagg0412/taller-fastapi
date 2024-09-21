#!/bin/bash

#Crear venv
python3 -m venv venv

#Activar venv
source .venv/bin/activate

#Instalar dependencias
if [ -f requirements.txt ]; then #-f es para verificar si el archivo existe
    pip install -r requirements.txt
else
    echo "requirements.txt not found"
fi

#Si los permisos no están configurados
if [ ! -x "setting-up.bash" ]; then
    chmod +x setting-up.bash 
fi
