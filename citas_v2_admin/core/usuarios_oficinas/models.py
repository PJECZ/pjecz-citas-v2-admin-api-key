"""
Usuarios-Oficinas, modelos
"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class UsuarioOficina(Base, UniversalMixin):
    """UsuarioOficina"""

    # Nombre de la tabla
    __tablename__ = "usuarios_oficinas"

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True)

    # Clave foránea
    oficina_id: Mapped[int] = mapped_column(ForeignKey("oficinas.id"), index=True)
    oficina: Mapped["Oficina"] = relationship(back_populates="usuarios_oficinas")
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    usuario: Mapped["Usuario"] = relationship(back_populates="usuarios_oficinas")

    # Columnas
    descripcion: Mapped[str] = mapped_column(String(256))

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
