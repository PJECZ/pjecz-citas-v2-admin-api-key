"""
PJECZ Plataforma Web API Key
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from config.settings import get_settings

from .v3.autoridades.paths import autoridades
from .v3.bitacoras.paths import bitacoras
from .v3.distritos.paths import distritos
from .v3.domicilios.paths import domicilios
from .v3.entradas_salidas.paths import entradas_salidas
from .v3.modulos.paths import modulos
from .v3.oficinas.paths import oficinas
from .v3.permisos.paths import permisos
from .v3.roles.paths import roles
from .v3.usuarios.paths import usuarios
from .v3.usuarios_roles.paths import usuarios_roles


def create_app() -> FastAPI:
    """Crea la aplicación FastAPI"""

    # FastAPI
    app = FastAPI(
        title="PJECZ Plataforma Web API Key",
        description="Bienvenido a PJECZ Plataforma Web API Key. Esta API es para trabajar con los datos de Plataforma Web. Se requiere tener una api-key para usarse.",
    )

    # CORSMiddleware
    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.origins.split(","),
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rutas
    app.include_router(autoridades)
    app.include_router(bitacoras)
    app.include_router(distritos)
    app.include_router(domicilios)
    app.include_router(entradas_salidas)
    app.include_router(modulos)
    app.include_router(oficinas)
    app.include_router(permisos)
    app.include_router(roles)
    app.include_router(usuarios)
    app.include_router(usuarios_roles)

    # Paginación
    add_pagination(app)

    # Mensaje de Bienvenida
    @app.get("/")
    async def root():
        """Mensaje de Bienvenida"""
        return {"message": "Bienvenido a PJECZ Plataforma Web API Key. Esta API es para trabajar con los datos de Plataforma Web. Se requiere tener una api-key para usarse."}

    # Entregar
    return app
