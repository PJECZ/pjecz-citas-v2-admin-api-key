"""
Usuarios-Oficinas, modelos
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class UsuarioOficina(Base, UniversalMixin):
    """UsuarioOficina"""

    # Nombre de la tabla
    __tablename__ = "usuarios_oficinas"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    oficina_id = Column(Integer, ForeignKey("oficinas.id"), index=True, nullable=False)
    oficina = relationship("Oficina", back_populates="usuarios_oficinas")
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), index=True, nullable=False)
    usuario = relationship("Usuario", back_populates="usuarios_oficinas")

    # Columnas
    descripcion = Column(String(256), nullable=False)

    @property
    def oficina_clave(self):
        """Oficina clave"""
        return self.oficina.clave

    @property
    def usuario_email(self):
        """Email del usuario"""
        return self.usuario.email

    @property
    def usuario_nombre(self):
        """Nombre del usuario"""
        return self.usuario.nombre

    def __repr__(self):
        """Representación"""
        return f"<UsuarioOficina {self.id}>"
