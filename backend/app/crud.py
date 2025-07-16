from typing import Annotated, Sequence,Any, Union
from typing import Any
from litestar import Controller, Response, get, post, patch,Request,delete
from litestar.exceptions import HTTPException
from advanced_alchemy.exceptions import NotFoundError
from litestar.dto import DTOData
from litestar.di import Provide
from litestar.contrib.jwt import OAuth2Login, Token
from litestar import get, Request
from litestar.connection import ASGIConnection
from litestar.handlers import BaseRouteHandler
from litestar.params import Body
from litestar.enums import RequestEncodingType
from sqlalchemy import text
from sqlalchemy.orm import Session


from app.repositories import (
    CepaRepository,
    provide_cepa_repo,
    UserRepository,
    provide_user_repo,
)
from app.dtos import (
    CepaReadDTO,
    CepaUpdateDTO,
    CepaCreateDTO,
    CepaUpdateJSONBDTO,
    UserCreateDTO,
    UserReadDTO,
    UserUpdateDTO,
    UserLoginDTO,
)
from app.models import (
    Cepa,
    User,
)
from .security import oauth2_auth

def admin_user_guard(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    if not connection.user.is_admin:
        pass
        raise HTTPException(
            status_code=403,
            detail="Not authorized.",
        )


class CepaController(Controller):
    path = "/cepas"
    tags = ["Cepa"]
    dto = CepaReadDTO
    dependencies = {
        "cepa_repo": Provide(provide_cepa_repo),
    }
    @get("/get-all")
    async def get_all(self, cepa_repo: CepaRepository = Provide(provide_cepa_repo)) -> list[dict[str, Any]]:
        # 1) Recupero todas las Cepa
            # Intentamos obtener todas las cepas
        print("DEBUG: Llamada a cepa_repo.list()")
        cepas: Sequence[Cepa] = cepa_repo.list()
        print(f"DEBUG: Se encontraron {len(cepas)} cepas")
        def filter_ids(obj: Any) -> Union[dict[str, Any], list, Any]:
            # Si es lista, aplico recursividad a cada elemento
            if isinstance(obj, list):
                return [filter_ids(item) for item in obj]

            # Si no es un objeto mapeado por SQLAlchemy, lo devuelvo tal cual
            cls = obj.__class__
            if not hasattr(cls, "__mapper__"):
                return obj

            result: dict[str, Any] = {}

            # 2.1) Columnas simples: tomo cada columna mapeada y omito las que terminen en "id",
            #       salvo que sea la PK "id" de la propia Cepa
            for column in cls.__mapper__.columns:
                col_name = column.key

                # Si termina en "id":
                if col_name.endswith("id"):
                    # --- Permitimos "id" únicamente para la clase Cepa ---
                    if col_name == "id" and isinstance(obj, Cepa):
                        # incluimos cepa.id
                        result[col_name] = getattr(obj, col_name)
                        continue
                    # Para cualquier otro "id" (ej. "cepa_id", o "id" de otras tablas), lo saltamos
                    continue

                # columnas que no terminan en "id"
                result[col_name] = getattr(obj, col_name)

            # 2.2) Relaciones: recorro cada relación definida
            for rel in cls.__mapper__.relationships:
                rel_name = rel.key

                # Si la relación apunta de vuelta a Cepa, la salto (backref)
                if rel_name == "cepa":
                    continue

                related_obj = getattr(obj, rel_name)

                if related_obj is None:
                    result[rel_name] = None
                else:
                    # Si la relación es 1-a-muchos (lista), aplico recursividad a cada elemento
                    if isinstance(related_obj, list):
                        result[rel_name] = [filter_ids(item) for item in related_obj]
                    else:
                        # Relación 1-a-1 o nulo
                        result[rel_name] = filter_ids(related_obj)

            return result
        # 3) Aplico el filtrado a cada Cepa y retorno la lista de diccionarios
        return [filter_ids(cepa) for cepa in cepas]
    @get("/get-by-id/{id:int}", dto=CepaReadDTO)  # READ
    async def get_by_id(self, id: int, cepa_repo: CepaRepository) -> Cepa:
        try:
            return cepa_repo.get(id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Cepa not found")
    @post("/create", dto=CepaCreateDTO,guards=[admin_user_guard]) #CREATE
    async def add_cepa(self,cepa_repo: CepaRepository,data: Cepa) -> Sequence[Cepa]:
        
        nueva = cepa_repo.add(data, auto_commit=True)
        return [nueva]
        
    @patch("/update/{cepa_id:int}", dto=CepaUpdateDTO,guards=[admin_user_guard])  # UPDATE
    async def update(self, cepa_id: int, data: DTOData[Cepa], cepa_repo: CepaRepository,request: Request,) -> Cepa:
        try:
            # 1. Obtenemos la instancia de la Cepa que vamos a actualizar.
            #    Usamos .get() en lugar de .get_and_update() por ahora.
            cepa_a_actualizar = cepa_repo.get(cepa_id)
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Cepa not found")

        # 2. Obtener el diccionario directamente de la solicitud, NO del DTO.
        update_data = await request.json()

        # 3. Iteramos sobre los datos recibidos para actualizar el objeto Cepa y sus relaciones.
        for key, value in update_data.items():
            if isinstance(value, dict):
                # Si el valor es un diccionario, es una relación anidada (ej. "almacenamiento").
                related_obj = getattr(cepa_a_actualizar, key, None)
                if related_obj:
                    # Si el objeto relacionado existe (ej. cepa.almacenamiento no es None),
                    # actualizamos sus atributos uno por uno.
                    for     sub_key, sub_value in value.items():
                        setattr(related_obj, sub_key, sub_value)
            # else:
                # Opcional: si la relación no existiera, aquí podrías crearla.
                # Por ejemplo:
                # from app.models import Almacenamiento
                # nuevo_almacenamiento = Almacenamiento(**value)
                # cepa_a_actualizar.almacenamiento = nuevo_almacenamiento
            else:
                # Si no es un diccionario, es un atributo simple de Cepa (ej. "nombre").
                setattr(cepa_a_actualizar, key, value)

    # 4. Añadimos el objeto modificado a la sesión y hacemos commit.
    #    SQLAlchemy detectará los cambios y generará las sentencias UPDATE correctas.
        cepa_repo.session.add(cepa_a_actualizar)
        cepa_repo.session.commit()
        cepa_repo.session.refresh(cepa_a_actualizar) # Refrescamos para obtener los datos actualizados de la DB.

        return cepa_a_actualizar

    @patch("/update-jsonb/{cepa_name:str}", dto=CepaUpdateJSONBDTO,guards=[admin_user_guard]) #UPDATE JSONB
    async def update_jsonb(
        self,
        cepa_name: str,
        data: DTOData[Cepa],
        cepa_repo: CepaRepository = Provide(provide_cepa_repo),
    ) -> Cepa:
        try:
            # 1) Extraer sólo el parche para datos_extra
            patch_data = data.as_builtins().get("datos_extra", {})
            
            # 2) Obtener la cepa actual y su JSONB existente
            cepa_actual = cepa_repo.get_and_update(  # o cepa_repo.get(...)
                match_fields=["nombre"],
                nombre=cepa_name,
                auto_commit=False,  # sólo lectura por ahora
            )[0]
            existing_json = cepa_actual.datos_extra or {}

            # 3) Fusionar los dos diccionarios (merge)
            merged_json = {**existing_json, **patch_data}

            # 4) Aplicar el update con el JSON combinado
            updated_cepa, _ = cepa_repo.get_and_update(
                match_fields=["nombre"],
                nombre=cepa_name,
                datos_extra=merged_json,
                auto_commit=True,
            )
            return updated_cepa

        except NotFoundError:
            raise HTTPException(status_code=404, detail="Cepa not found")
        
class UserController(Controller):
    path = "/users"
    tags = ["User"]
    dto = UserReadDTO
    dependencies = {
        "user_repo": Provide(provide_user_repo),
    }

    @get("/get-all")
    async def get_all_users(self, user_repo: UserRepository) -> list[User]:
        return user_repo.list()
        
    @get("/me")
    async def get_my_user(self, request: "Request[User, Token, Any]") -> User:
        return request.user
    
    @post("/create", dto=UserCreateDTO)  # CREATE
    async def create_user(self, user_repo: UserRepository, data: User) -> User:
        # 1) Calculamos el próximo ID manualmente
        next_id = user_repo.get_next_table_id("users")
        data.id = next_id

        print(f"DEBUG: Creando usuario con ID {data.id} y datos: {data}")
        
        # 2) Insertamos con hash de password y commit
        return user_repo.add_with_password_hash(data, auto_commit=True)

    
    @patch("/update/{user_id:int}", dto=UserUpdateDTO, guards=[admin_user_guard])
    async def update_user(
        self, user_repo: UserRepository, user_id: int, data: DTOData[User]
    ) -> User:
        user, _ = user_repo.get_and_update(
            match_fields="id", id=user_id, **data.as_builtins(), auto_commit=True
        )
        return user
    @delete("/delete/{user_id:int}",guards=[admin_user_guard],)
    async def delete_user(self, user_repo: UserRepository, user_id: int) -> None:
        user_repo.delete(user_id, auto_commit=True)

        # 2) Reajustamos IDs y secuencia
        session: Session = user_repo.session
        next_id = user_repo.resequence_table_ids(
            table_name="users",
            sequence_name="users_id_seq",
            deleted_id=user_id,
        )
        # 3) Commit de todo el cambio (borrado + resecuenciación)
        session.commit()

        print(f"DEBUG: Usuario {user_id} borrado y IDs reajustados. Siguiente ID será {next_id}.")
    
    
class AuthController(Controller):
    path = "/auth"
    tags = ["auth"]

    @post(
        "/login",
        dto=UserLoginDTO,
        dependencies={"users_repo": Provide(provide_user_repo)},
    )
    async def login(
        self,
        data: Annotated[User, Body(media_type=RequestEncodingType.URL_ENCODED)],
        users_repo: UserRepository,
    ) -> Response[OAuth2Login]:
        user = users_repo.get_one_or_none(username=data.username)

        if user is None or not users_repo.check_password(data.username, data.password):
            print(f"DEBUG: Intento de inicio de sesión fallido para el usuario '{data.username}' con contraseña '{data.password}'")
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrecta")

        return oauth2_auth.login(identifier=user.username)