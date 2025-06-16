"""
Sistema de Gestión de Contraseñas Local y Seguro
Autor: Claude
Descripción: Gestor de contraseñas CLI con cifrado fuerte y almacenamiento local
"""

import os
import sys
import json
import getpass
import pyperclip
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
import secrets

class PasswordManager:
    def __init__(self):
        self.vault_file = "vault.enc"
        self.salt_file = "salt.key"
        self.iterations = 480000  # Número alto de iteraciones para PBKDF2
        self.vault_data = {}
        self.cipher_key = None
        
    def generate_salt(self):
        """Genera una sal criptográfica segura de 16 bytes"""
        return secrets.token_bytes(16)
    
    def save_salt(self, salt):
        """Guarda la sal en el archivo salt.key"""
        with open(self.salt_file, 'wb') as f:
            f.write(salt)
    
    def load_salt(self):
        """Carga la sal desde el archivo salt.key"""
        try:
            with open(self.salt_file, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            print("❌ Error: Archivo de sal no encontrado. Ejecuta la configuración inicial.")
            sys.exit(1)
    
    def de
rive_key(self, password, salt):
        """Deriva una clave de cifrado usando PBKDF2HMAC"""
        password_bytes = password.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    
    def encrypt_data(self, data):
        """Cifra los datos usando Fernet"""
        if self.cipher_key is None:
            raise ValueError("Clave de cifrado no disponible")
        
        fernet = Fernet(self.cipher_key)
        json_data = json.dumps(data).encode('utf-8')
        encrypted_data = fernet.encrypt(json_data)
        return encrypted_data
    
    def decrypt_data(self, encrypted_data):
        """Descifra los datos usando Fernet"""
        if self.cipher_key is None:
            raise ValueError("Clave de cifrado no disponible")
        
        fernet = Fernet(self.cipher_key)
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode('utf-8'))
        except Exception:
            raise ValueError("Error al descifrar: contraseña incorrecta")
    
    def save_vault(self):
        """Guarda el almacén cifrado en el archivo vault.enc"""
        encrypted_data = self.encrypt_data(self.vault_data)
        with open(self.vault_file, 'wb') as f:
            f.write(encrypted_data)
    
    def load_vault(self):
        """Carga y descifra el almacén desde vault.enc"""
        try:
            with open(self.vault_file, 'rb') as f:
                encrypted_data = f.read()
            self.vault_data = self.decrypt_data(encrypted_data)
        except FileNotFoundError:
            print("❌ Error: Archivo de almacén no encontrado. Ejecuta la configuración inicial.")
            sys.exit(1)
    
    def setup_initial_configuration(self):
        """Configuración inicial del sistema"""
        print("🔧 Configuración inicial del Sistema de Gestión de Contraseñas")
        print("=" * 60)
        
        # Verificar si ya existe configuración
        if os.path.exists(self.vault_file) or os.path.exists(self.salt_file):
            print("⚠️  Ya existe una configuración. ¿Deseas sobrescribirla? (s/N): ", end="")
            response = input().lower()
            if response != 's':
                print("Configuración cancelada.")
                return False
        
        # Crear contraseña maestra
        while True:
            master_password = getpass.getpass("🔐 Crea tu contraseña maestra: ")
            if len(master_password) < 8:
                print("❌ La contraseña debe tener al menos 8 caracteres.")
                continue
            
            confirm_password = getpass.getpass("🔐 Confirma tu contraseña maestra: ")
            if master_password != confirm_password:
                print("❌ Las contraseñas no coinciden.")
                continue
            break
        
        # Generar y guardar sal
        salt = self.generate_salt()
        self.save_salt(salt)
        
        # Derivar clave y configurar cifrado
        self.cipher_key = self.derive_key(master_password, salt)
        
        # Crear almacén vacío
        self.vault_data = {}
        self.save_vault()
        
        print("✅ Configuración completada exitosamente.")
        print(f"📁 Archivos creados: {self.vault_file}, {self.salt_file}")
        return True
    
    def unlock_vault(self):
        """Desbloquea el almacén con la contraseña maestra"""
        if not os.path.exists(self.vault_file) or not os.path.exists(self.salt_file):
            print("❌ Sistema no configurado. Ejecuta la configuración inicial primero.")
            return False
        
        # Solicitar contraseña maestra
        master_password = getpass.getpass("🔐 Ingresa tu contraseña maestra: ")
        
        # Cargar sal y derivar clave
        salt = self.load_salt()
        self.cipher_key = self.derive_key(master_password, salt)
        
        # Intentar descifrar el almacén
        try:
            self.load_vault()
            print("✅ Almacén desbloqueado exitosamente.")
            return True
        except ValueError as e:
            print(f"❌ {e}")
            return False
    
    def add_credential(self, website, username, password, account_name=None):
        """Añade una nueva credencial al almacén"""
        # Inicializar estructura si el sitio no existe
        if website not in self.vault_data:
            self.vault_data[website] = []
        
        # Verificar si ya existe esta combinación usuario/nombre de cuenta
        for existing in self.vault_data[website]:
            if existing['username'] == username and existing.get('account_name') == account_name:
                print(f"⚠️  Ya existe una credencial para '{username}' en '{website}'", end="")
                if account_name:
                    print(f" (cuenta: {account_name})", end="")
                print(". ¿Deseas sobrescribirla? (s/N): ", end="")
                response = input().lower()
                if response != 's':
                    print("Operación cancelada.")
                    return
                # Actualizar credencial existente
                existing['password'] = password
                self.save_vault()
                print(f"✅ Credencial actualizada exitosamente.")
                return
        
        # Añadir nueva credencial
        credential = {
            'username': username,
            'password': password
        }
        if account_name:
            credential['account_name'] = account_name
        
        self.vault_data[website].append(credential)
        self.save_vault()
        account_info = f" (cuenta: {account_name})" if account_name else ""
        print(f"✅ Credencial para '{website}'{account_info} añadida exitosamente.")
    
    def get_credential(self, website, identifier=None):
        """Obtiene una credencial y la copia al portapapeles"""
        if website not in self.vault_data:
            print(f"❌ No se encontró credencial para '{website}'.")
            return
        
        credentials = self.vault_data[website]
        if not credentials:
            print(f"❌ No hay credenciales para '{website}'.")
            return
        
        # Si hay una sola credencial, usarla directamente
        if len(credentials) == 1:
            selected_credential = credentials[0]
        else:
            # Múltiples credenciales - necesitamos identificar cuál usar
            if identifier is None:
                print(f"🔍 Múltiples cuentas encontradas para '{website}':")
                for i, cred in enumerate(credentials, 1):
                    account_info = f" ({cred['account_name']})" if cred.get('account_name') else ""
                    print(f"  {i}. {cred['username']}{account_info}")
                
                while True:
                    try:
                        choice = input("Selecciona el número de cuenta (o 'q' para cancelar): ").strip()
                        if choice.lower() == 'q':
                            print("Operación cancelada.")
                            return
                        choice = int(choice)
                        if 1 <= choice <= len(credentials):
                            selected_credential = credentials[choice - 1]
                            break
                        else:
                            print(f"❌ Número inválido. Debe estar entre 1 y {len(credentials)}.")
                    except ValueError:
                        print("❌ Por favor ingresa un número válido.")
            else:
                # Buscar por identificador (usuario o nombre de cuenta)
                found_credentials = []
                for cred in credentials:
                    if (cred['username'] == identifier or 
                        cred.get('account_name') == identifier):
                        found_credentials.append(cred)
                
                if not found_credentials:
                    print(f"❌ No se encontró credencial para '{identifier}' en '{website}'.")
                    return
                elif len(found_credentials) == 1:
                    selected_credential = found_credentials[0]
                else:
                    print(f"🔍 Múltiples coincidencias encontradas:")
                    for i, cred in enumerate(found_credentials, 1):
                        account_info = f" ({cred['account_name']})" if cred.get('account_name') else ""
                        print(f"  {i}. {cred['username']}{account_info}")
                    
                    while True:
                        try:
                            choice = input("Selecciona el número: ").strip()
                            choice = int(choice)
                            if 1 <= choice <= len(found_credentials):
                                selected_credential = found_credentials[choice - 1]
                                break
                            else:
                                print(f"❌ Número inválido. Debe estar entre 1 y {len(found_credentials)}.")
                        except ValueError:
                            print("❌ Por favor ingresa un número válido.")
        
        # Mostrar y copiar la credencial seleccionada
        account_info = f" ({selected_credential['account_name']})" if selected_credential.get('account_name') else ""
        try:
            pyperclip.copy(selected_credential['password'])
            print(f"✅ Credencial encontrada para '{website}'{account_info}:")
            print(f"   👤 Usuario: {selected_credential['username']}")
            print(f"   🔑 Contraseña copiada al portapapeles")
        except:
            print(f"✅ Credencial encontrada para '{website}'{account_info}:")
            print(f"   👤 Usuario: {selected_credential['username']}")
            print(f"   🔑 Contraseña: {selected_credential['password']}")
            print("   ⚠️  No se pudo copiar al portapapeles")
    
    def list_credentials(self):
        """Lista todos los sitios web almacenados"""
        if not self.vault_data:
            print("📭 No hay credenciales almacenadas.")
            return
        
        total_credentials = sum(len(creds) for creds in self.vault_data.values())
        print(f"📋 Credenciales almacenadas ({total_credentials} cuentas en {len(self.vault_data)} sitios):")
        print("-" * 50)
        
        for website, credentials in self.vault_data.items():
            print(f"🌐 {website}")
            if not credentials:
                print("   ⚠️  Sin credenciales")
                continue
            
            for i, credential in enumerate(credentials, 1):
                account_info = f" ({credential['account_name']})" if credential.get('account_name') else ""
                if len(credentials) > 1:
                    print(f"   {i}. 👤 {credential['username']}{account_info}")
                else:
                    print(f"   👤 {credential['username']}{account_info}")
            print()
    
    def delete_credential(self, website, identifier=None):
        """Elimina una credencial del almacén"""
        if website not in self.vault_data:
            print(f"❌ No se encontró credencial para '{website}'.")
            return
        
        credentials = self.vault_data[website]
        if not credentials:
            print(f"❌ No hay credenciales para '{website}'.")
            return
        
        # Si hay una sola credencial
        if len(credentials) == 1:
            credential_to_delete = credentials[0]
            account_info = f" ({credential_to_delete['account_name']})" if credential_to_delete.get('account_name') else ""
            print(f"⚠️  ¿Estás seguro de eliminar la credencial '{credential_to_delete['username']}{account_info}' de '{website}'? (s/N): ", end="")
            response = input().lower()
            if response != 's':
                print("Operación cancelada.")
                return
            
            del self.vault_data[website]
            self.save_vault()
            print(f"✅ Credencial eliminada exitosamente.")
            return
        
        # Múltiples credenciales
        if identifier is None:
            print(f"🔍 Múltiples cuentas encontradas para '{website}':")
            for i, cred in enumerate(credentials, 1):
                account_info = f" ({cred['account_name']})" if cred.get('account_name') else ""
                print(f"  {i}. {cred['username']}{account_info}")
            
            while True:
                try:
                    choice = input("Selecciona el número a eliminar (o 'q' para cancelar): ").strip()
                    if choice.lower() == 'q':
                        print("Operación cancelada.")
                        return
                    choice = int(choice)
                    if 1 <= choice <= len(credentials):
                        credential_to_delete = credentials[choice - 1]
                        break
                    else:
                        print(f"❌ Número inválido. Debe estar entre 1 y {len(credentials)}.")
                except ValueError:
                    print("❌ Por favor ingresa un número válido.")
        else:
            # Buscar por identificador
            found_credentials = []
            found_indices = []
            for i, cred in enumerate(credentials):
                if (cred['username'] == identifier or 
                    cred.get('account_name') == identifier):
                    found_credentials.append(cred)
                    found_indices.append(i)
            
            if not found_credentials:
                print(f"❌ No se encontró credencial para '{identifier}' en '{website}'.")
                return
            elif len(found_credentials) == 1:
                credential_to_delete = found_credentials[0]
                credential_index = found_indices[0]
            else:
                print(f"🔍 Múltiples coincidencias encontradas:")
                for i, cred in enumerate(found_credentials, 1):
                    account_info = f" ({cred['account_name']})" if cred.get('account_name') else ""
                    print(f"  {i}. {cred['username']}{account_info}")
                
                while True:
                    try:
                        choice = input("Selecciona el número a eliminar: ").strip()
                        choice = int(choice)
                        if 1 <= choice <= len(found_credentials):
                            credential_to_delete = found_credentials[choice - 1]
                            credential_index = found_indices[choice - 1]
                            break
                        else:
                            print(f"❌ Número inválido. Debe estar entre 1 y {len(found_credentials)}.")
                    except ValueError:
                        print("❌ Por favor ingresa un número válido.")
        
        # Confirmar eliminación
        account_info = f" ({credential_to_delete['account_name']})" if credential_to_delete.get('account_name') else ""
        print(f"⚠️  ¿Estás seguro de eliminar la credencial '{credential_to_delete['username']}{account_info}' de '{website}'? (s/N): ", end="")
        response = input().lower()
        if response != 's':
            print("Operación cancelada.")
            return
        
        # Eliminar credencial
        if len(credentials) == 1:
            del self.vault_data[website]
        else:
            credentials.remove(credential_to_delete)
        
        self.save_vault()
        print(f"✅ Credencial eliminada exitosamente.")
    
    def show_help(self):
        """Muestra la ayuda del sistema"""
        print("\n🔐 Sistema de Gestión de Contraseñas")
        print("=" * 50)
        print("Comandos disponibles:")
        print("  setup                              - Configuración inicial")
        print("  add <sitio> <usuario> <contraseña> [nombre_cuenta] - Añadir credencial")
        print("  get <sitio> [usuario_o_cuenta]     - Obtener credencial")
        print("  list                               - Listar todos los sitios")
        print("  delete <sitio> [usuario_o_cuenta]  - Eliminar credencial")
        print("  help                               - Mostrar esta ayuda")
        print("  exit                               - Salir del programa")
        print()
        print("💡 Ejemplos:")
        print("  add gmail juan@work.com pass123 trabajo")
        print("  add gmail juan@personal.com pass456 personal")
        print("  get gmail trabajo")
        print("  get gmail juan@work.com")
        print("  delete gmail personal")
        print()
    
    def run_interactive_mode(self):
        """Ejecuta el modo interactivo del gestor"""
        print("🔐 Sistema de Gestión de Contraseñas")
        print("Escribe 'help' para ver los comandos disponibles.")
        print()
        
        while True:
            try:
                command = input("🔒 password-manager> ").strip().split()
                if not command:
                    continue
                
                cmd = command[0].lower()
                
                if cmd == 'exit':
                    print("👋 ¡Hasta luego!")
                    break
                elif cmd == 'help':
                    self.show_help()
                elif cmd == 'setup':
                    self.setup_initial_configuration()
                elif cmd == 'add':
                    if len(command) < 4 or len(command) > 5:
                        print("❌ Uso: add <sitio> <usuario> <contraseña> [nombre_cuenta]")
                        continue
                    website, username, password = command[1], command[2], command[3]
                    account_name = command[4] if len(command) == 5 else None
                    self.add_credential(website, username, password, account_name)
                elif cmd == 'get':
                    if len(command) < 2 or len(command) > 3:
                        print("❌ Uso: get <sitio> [usuario_o_cuenta]")
                        continue
                    website = command[1]
                    identifier = command[2] if len(command) == 3 else None
                    self.get_credential(website, identifier)
                elif cmd == 'list':
                    self.list_credentials()
                elif cmd == 'delete':
                    if len(command) < 2 or len(command) > 3:
                        print("❌ Uso: delete <sitio> [usuario_o_cuenta]")
                        continue
                    website = command[1]
                    identifier = command[2] if len(command) == 3 else None
                    self.delete_credential(website, identifier)
                else:
                    print(f"❌ Comando desconocido: {cmd}")
                    print("Escribe 'help' para ver los comandos disponibles.")
                
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Función principal del programa"""
    manager = PasswordManager()
    
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        if sys.argv[1] == 'setup':
            manager.setup_initial_configuration()
            return
        elif sys.argv[1] == 'help':
            manager.show_help()
            return
    
    # Verificar si el sistema está configurado
    if not os.path.exists(manager.vault_file) or not os.path.exists(manager.salt_file):
        print("🔧 Sistema no configurado. Ejecutando configuración inicial...")
        if not manager.setup_initial_configuration():
            return
    
    # Desbloquear el almacén
    if not manager.unlock_vault():
        print("❌ No se pudo acceder al almacén. Programa terminado.")
        return
    
    # Ejecutar modo interactivo
    manager.run_interactive_mode()

if __name__ == "__main__":
    main()
