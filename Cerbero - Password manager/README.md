## 🔐 Características de Seguridad

**Criptografía robusta:**
- Usa PBKDF2HMAC con 480,000 iteraciones para derivar la clave
- Cifrado autenticado con Fernet (AES 128 en modo CBC + HMAC SHA256)
- Sal criptográfica única de 16 bytes generada con `secrets`

**Arquitectura de archivos:**
- `vault.enc`: Todas las credenciales cifradas en un solo archivo
- `salt.key`: Sal para la derivación de clave (no es secreta pero necesaria)

## 🚀 Instalación y Uso

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Primera ejecución (configuración):**
```bash
python password_manager.py setup
```

3. **Uso normal:**
```bash
python password_manager.py
```

## 💻 Comandos Disponibles

Una vez desbloqueado el almacén:

- `add <sitio> <usuario> <contraseña>` - Añadir nueva credencial
- `get <sitio>` - Obtener credencial (copia la contraseña al portapapeles)
- `list` - Listar todos los sitios guardados
- `delete <sitio>` - Eliminar una credencial
- `help` - Mostrar ayuda
- `exit` - Salir

## 🛡️ Medidas de Seguridad Implementadas

1. **Nunca almacena la contraseña maestra** - solo se usa para derivar la clave
2. **Validación de contraseña** - falla seguro si la contraseña es incorrecta
3. **Memoria limpia** - los datos descifrados solo existen en memoria durante la sesión
4. **Confirmaciones** - para operaciones destructivas como sobrescribir o eliminar
5. **Manejo de errores** - respuestas seguras ante fallos


### **Múltiples Cuentas por Sitio**
- Puedes guardar varias cuentas para el mismo sitio web
- Cada cuenta puede tener un nombre identificativo opcional
- Las credenciales se organizan como listas dentro de cada sitio

**Añadir credenciales:**
```bash
# Sintaxis básica
add <sitio> <usuario> <contraseña> [nombre_cuenta]

# Ejemplos:
add gmail juan@trabajo.com miPass123 trabajo
add gmail juan@personal.com miPass456 personal
add facebook usuario1 pass1
add facebook usuario2 pass2 secundaria
```

**Obtener credenciales:**
```bash
# Si hay una sola cuenta, la obtiene automáticamente
get facebook

# Si hay múltiples, puedes especificar por usuario o nombre de cuenta
get gmail trabajo
get gmail juan@personal.com

# Si no especificas, te muestra un menú para elegir
get gmail
```

**Eliminar credenciales:**
```bash
# Eliminar cuenta específica
delete gmail trabajo
delete gmail juan@personal.com

# Si no especificas, te muestra un menú para elegir
delete gmail
```

## 📋 Ejemplo de Uso Completo

```bash
🔒 password-manager> add gmail juan@trabajo.com pass123 trabajo
✅ Credencial para 'gmail' (cuenta: trabajo) añadida exitosamente.

🔒 password-manager> add gmail juan@personal.com pass456 personal  
✅ Credencial para 'gmail' (cuenta: personal) añadida exitosamente.

🔒 password-manager> add gmail backup@gmail.com pass789
✅ Credencial para 'gmail' añadida exitosamente.

🔒 password-manager> list
📋 Credenciales almacenadas (3 cuentas en 1 sitios):
--------------------------------------------------
🌐 gmail
   1. 👤 juan@trabajo.com (trabajo)
   2. 👤 juan@personal.com (personal)
   3. 👤 backup@gmail.com

🔒 password-manager> get gmail trabajo
✅ Credencial encontrada para 'gmail' (trabajo):
   👤 Usuario: juan@trabajo.com
   🔑 Contraseña copiada al portapapeles

🔒 password-manager> get gmail
🔍 Múltiples cuentas encontradas para 'gmail':
  1. juan@trabajo.com (trabajo)
  2. juan@personal.com (personal)
  3. backup@gmail.com
Selecciona el número de cuenta (o 'q' para cancelar): 2
✅ Credencial encontrada para 'gmail' (personal):
   👤 Usuario: juan@personal.com
   🔑 Contraseña copiada al portapapeles
```


