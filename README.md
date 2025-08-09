# SSH-MASS-PSWRD-RESET-SMPR-
Conecta via SSH a un rango de IPs (ej: 192.168.1.1-50), ejecuta comando 'passwd' automáticamente en cada servidor, maneja la interacción interactiva y proporciona resumen de éxitos/fallos. 


## INSTRUCCIONES DE USO:

1. Instalación de dependencias:
   pip install paramiko

2. Ejecución:
   python ssh_password_changer.py

3. Configuración:
   - Ingresa el usuario SSH
   - Ingresa la contraseña actual
   - Define el rango de IPs (ej: 192.168.1.1 a 192.168.1.50)
   - Establece la nueva contraseña

CARACTERÍSTICAS:
- ✅ Conexión SSH segura
- ✅ Manejo de errores robusto
- ✅ Interfaz de usuario intuitiva
- ✅ Resumen detallado de resultados
- ✅ Confirmaciones de seguridad
- ✅ Timeout configurable
- ✅ Logging detallado del proceso

CONSIDERACIONES DE SEGURIDAD:
- 🔒 Las contraseñas se manejan de forma segura (getpass)
- 🛡️ Verificación de conexión antes de cambiar contraseñas
- ⚠️ Confirmación explícita antes de ejecutar cambios masivos
- 🔍 Validación de resultados

NOTAS:
- Asegúrate de tener acceso SSH a todos los servidores
- Prueba primero en un rango pequeño
- Mantén un respaldo de las contraseñas actuales
- Considera implementar logging a archivo para auditoría

