#!/usr/bin/env python3
"""
🔐 SCRIPT SEGURO DE INICIALIZACIÓN DE ADMINISTRADOR
Delizzia POS - Sistema de Punto de Venta

Este script crea el usuario administrador inicial de forma segura.
"""

import sys
import os
import secrets
import getpass
from pathlib import Path

# Agregar el directorio padre al path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, create_tables
from app.core.security import get_password_hash
from app.models.users import User


def generate_secure_password() -> str:
    """Genera una contraseña segura automáticamente"""
    return secrets.token_urlsafe(16)


    @classmethod
def validate_password(password: str) -> bool:
    """Valida que la contraseña cumple con requisitos de seguridad"""
    if len(password) < 8:
        print("❌ Error: La contraseña debe tener al menos 8 caracteres")
        return False
    
    if not any(c.isupper() for c in password):
        print("❌ Error: La contraseña debe contener al menos una mayúscula")
        return False
    
    if not any(c.islower() for c in password):
        print("❌ Error: La contraseña debe contener al menos una minúscula")
        return False
    
    if not any(c.isdigit() for c in password):
        print("❌ Error: La contraseña debe contener al menos un número")
        return False
    
    return True


def create_admin_user():
    """Crea el usuario administrador inicial"""
    
    print("🍕 DELIZZIA POS - Inicialización de Administrador")
    print("=" * 50)
    print()
    
    # Verificar si ya existe un administrador
    db: Session = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.role == "owner").first()
        if existing_admin:
            print("⚠️  Ya existe un usuario administrador en el sistema:")
            print(f"   👤 Usuario: {existing_admin.username}")
            print(f"   📧 Email: {existing_admin.email}")
            print(f"   📅 Creado: {existing_admin.created_at}")
            print()
            
            confirm = input("¿Quieres crear otro administrador? (s/N): ").lower()
            if confirm != 's':
                print("❌ Operación cancelada")
                return
            print()
    finally:
        db.close()
    
    # Crear tablas si no existen
    print("🗄️  Inicializando base de datos...")
    create_tables()
    print("✅ Base de datos inicializada")
    print()
    
    # Solicitar datos del administrador
    print("📝 Ingresa los datos del administrador:")
    print()
    
    username = input("👤 Nombre de usuario: ").strip()
    if not username:
        print("❌ Error: El nombre de usuario es obligatorio")
        return
    
    full_name = input("👨‍💼 Nombre completo: ").strip()
    if not full_name:
        print("❌ Error: El nombre completo es obligatorio")
        return
    
    email = input("📧 Email: ").strip()
    if not email or "@" not in email:
        print("❌ Error: Email inválido")
        return
    
    print()
    print("🔐 Configuración de contraseña:")
    print("   Opción 1: Generar contraseña segura automáticamente (recomendado)")
    print("   Opción 2: Ingresar contraseña manualmente")
    print()
    
    password_option = input("Selecciona opción (1/2): ").strip()
    
    if password_option == "1":
        password = generate_secure_password()
        print(f"🔑 Contraseña generada: {password}")
        print("⚠️  ¡GUARDA ESTA CONTRASEÑA EN UN LUGAR SEGURO!")
        print()
        input("Presiona Enter cuando hayas guardado la contraseña...")
    else:
        while True:
            password = getpass.getpass("🔑 Contraseña: ")
            if validate_password(password):
                confirm_password = getpass.getpass("🔑 Confirma contraseña: ")
                if password == confirm_password:
                    break
                else:
                    print("❌ Error: Las contraseñas no coinciden")
            print()
    
    print()
    print("🔄 Creando usuario administrador...")
    
    # Crear usuario en base de datos
    db: Session = SessionLocal()
    try:
        # Verificar que no exista el username o email
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            print("❌ Error: Ya existe un usuario con ese nombre de usuario o email")
            return
        
        # Crear usuario
        hashed_password = get_password_hash(password)
        admin_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role="owner",
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Usuario administrador creado exitosamente!")
        print()
        print("📋 Detalles del usuario:")
        print(f"   👤 Usuario: {admin_user.username}")
        print(f"   📧 Email: {admin_user.email}")
        print(f"   👨‍💼 Nombre: {admin_user.full_name}")
        print(f"   🎭 Rol: {admin_user.role}")
        print(f"   📅 Creado: {admin_user.created_at}")
        print()
        print("🚀 Ahora puedes iniciar sesión en el sistema con estas credenciales")
        
    except Exception as e:
        print(f"❌ Error creando usuario: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    try:
        create_admin_user()
    except KeyboardInterrupt:
        print("\n❌ Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")