"""
Aplicación para cambiar contraseñas mediante SSH en un rango de IPs
Ejecuta el comando 'passwd' en cada servidor del rango especificado
                    Maded By Shadow205014
"""

import paramiko
import time
import sys
import getpass
from typing import List, Tuple

class SSHPasswordChanger:
    def __init__(self, username: str, current_password: str):
        """
        Inicializa el cambiador de contraseñas SSH
        
        Args:
            username: Usuario para conectar via SSH
            current_password: Contraseña actual del usuario
        """
        self.username = username
        self.current_password = current_password
        self.timeout = 30  # Timeout de conexión en segundos
        
    def generate_ip_range(self, base_ip: str, start_octet: int, end_octet: int) -> List[str]:
        """
        Genera una lista de IPs basada en el rango del último octeto
        
        Args:
            base_ip: IP base (ej: "192.168.1")
            start_octet: Octeto inicial del rango
            end_octet: Octeto final del rango
            
        Returns:
            Lista de IPs en el rango especificado
        """
        ips = []
        for i in range(start_octet, end_octet + 1):
            ips.append(f"{base_ip}.{i}")
        return ips
    
    def test_ssh_connection(self, ip: str) -> bool:
        """
        Prueba la conexión SSH a una IP específica
        
        Args:
            ip: Dirección IP a probar
            
        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=ip,
                username=self.username,
                password=self.current_password,
                timeout=self.timeout
            )
            client.close()
            return True
        except Exception as e:
            print(f"❌ Error conectando a {ip}: {str(e)}")
            return False
    
    def change_password_on_server(self, ip: str, new_password: str) -> Tuple[bool, str]:
        """
        Cambia la contraseña en un servidor específico
        
        Args:
            ip: Dirección IP del servidor
            new_password: Nueva contraseña a establecer
            
        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            # Crear cliente SSH
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Conectar al servidor
            print(f"🔄 Conectando a {ip}...")
            client.connect(
                hostname=ip,
                username=self.username,
                password=self.current_password,
                timeout=self.timeout
            )
            
            # Abrir canal interactivo para el comando passwd
            channel = client.invoke_shell()
            
            # Ejecutar comando passwd
            print(f"📝 Ejecutando 'passwd' en {ip}...")
            channel.send('passwd\n')
            time.sleep(2)
            
            # Esperar prompt de contraseña actual
            output = ""
            while True:
                if channel.recv_ready():
                    output += channel.recv(1024).decode('utf-8')
                if 'current' in output.lower() or 'actual' in output.lower():
                    break
                time.sleep(0.5)
            
            # Enviar contraseña actual
            channel.send(f'{self.current_password}\n')
            time.sleep(2)
            
            # Esperar prompt de nueva contraseña
            output = ""
            while True:
                if channel.recv_ready():
                    output += channel.recv(1024).decode('utf-8')
                if 'new' in output.lower() or 'nueva' in output.lower():
                    break
                time.sleep(0.5)
            
            # Enviar nueva contraseña
            channel.send(f'{new_password}\n')
            time.sleep(2)
            
            # Confirmar nueva contraseña
            output = ""
            while True:
                if channel.recv_ready():
                    output += channel.recv(1024).decode('utf-8')
                if 'retype' in output.lower() or 'confirm' in output.lower() or 'again' in output.lower():
                    break
                time.sleep(0.5)
            
            channel.send(f'{new_password}\n')
            time.sleep(3)
            
            # Verificar resultado
            final_output = ""
            while channel.recv_ready():
                final_output += channel.recv(1024).decode('utf-8')
            
            client.close()
            
            if 'successfully' in final_output.lower() or 'success' in final_output.lower():
                return True, f"✅ Contraseña cambiada exitosamente en {ip}"
            else:
                return False, f"⚠️ Posible error al cambiar contraseña en {ip}: {final_output}"
                
        except Exception as e:
            return False, f"❌ Error al cambiar contraseña en {ip}: {str(e)}"
    
    def change_passwords_in_range(self, base_ip: str, start_octet: int, end_octet: int, new_password: str):
        """
        Cambia contraseñas en un rango de IPs
        
        Args:
            base_ip: IP base (ej: "192.168.1")
            start_octet: Octeto inicial del rango
            end_octet: Octeto final del rango
            new_password: Nueva contraseña a establecer
        """
        ips = self.generate_ip_range(base_ip, start_octet, end_octet)
        
        print(f"🚀 Iniciando cambio de contraseñas en rango {base_ip}.{start_octet}-{end_octet}")
        print(f"📊 Total de servidores: {len(ips)}")
        print("-" * 60)
        
        successful = []
        failed = []
        
        for ip in ips:
            print(f"\n🔧 Procesando {ip}...")
            
            # Probar conexión primero
            if not self.test_ssh_connection(ip):
                failed.append((ip, "No se pudo establecer conexión SSH"))
                continue
            
            # Intentar cambiar contraseña
            success, message = self.change_password_on_server(ip, new_password)
            
            if success:
                successful.append(ip)
                print(message)
            else:
                failed.append((ip, message))
                print(message)
            
            # Pequeña pausa entre servidores
            time.sleep(1)
        
        # Resumen final
        print("\n" + "="*60)
        print("📋 RESUMEN FINAL")
        print("="*60)
        print(f"✅ Exitosos: {len(successful)}")
        print(f"❌ Fallidos: {len(failed)}")
        
        if successful:
            print(f"\n🎉 Servidores con contraseña cambiada exitosamente:")
            for ip in successful:
                print(f"  • {ip}")
        
        if failed:
            print(f"\n⚠️ Servidores con errores:")
            for ip, error in failed:
                print(f"  • {ip}: {error}")

def main():
    """Función principal de la aplicación"""
    print("🔐 CAMBIADOR DE CONTRASEÑAS SSH")
    print("="*50)
    
    try:
        # Solicitar datos de conexión
        username = input("👤 Usuario SSH: ")
        current_password = getpass.getpass("🔒 Contraseña actual: ")
        
        # Solicitar rango de IPs
        base_ip = input("🌐 IP base (ej: 192.168.1): ")
        start_octet = int(input("📍 Octeto inicial (ej: 1): "))
        end_octet = int(input("📍 Octeto final (ej: 10): "))
        
        # Solicitar nueva contraseña
        new_password = getpass.getpass("🔑 Nueva contraseña: ")
        confirm_password = getpass.getpass("🔑 Confirmar nueva contraseña: ")
        
        if new_password != confirm_password:
            print("❌ Las contraseñas no coinciden. Saliendo...")
            sys.exit(1)
        
        # Confirmación de seguridad
        ips_to_process = end_octet - start_octet + 1
        print(f"\n⚠️ ADVERTENCIA: Se intentará cambiar la contraseña en {ips_to_process} servidores")
        print(f"📡 Rango: {base_ip}.{start_octet} a {base_ip}.{end_octet}")
        
        confirm = input("¿Continuar? (s/N): ").lower()
        if confirm != 's' and confirm != 'si':
            print("🚫 Operación cancelada por el usuario")
            sys.exit(0)
        
        # Crear instancia del cambiador
        changer = SSHPasswordChanger(username, current_password)
        
        # Ejecutar cambio de contraseñas
        changer.change_passwords_in_range(base_ip, start_octet, end_octet, new_password)
        
    except KeyboardInterrupt:
        print("\n🚫 Operación interrumpida por el usuario")
        sys.exit(0)
    except ValueError as e:
        print(f"❌ Error en los datos ingresados: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Verificar que paramiko esté instalado
    try:
        import paramiko
    except ImportError:
        print("❌ Error: La librería 'paramiko' no está instalada")
        print("📦 Instálala con: pip install paramiko")
        sys.exit(1)
    
    main()
