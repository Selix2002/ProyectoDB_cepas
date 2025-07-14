from advanced_alchemy.repository import SQLAlchemySyncRepository
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models import Cepa, Almacenamiento, MedioCultivo, Morfologia, ActividadEnzimatica, CrecimientoTemperatura, ResistenciaAntibiotica, CaracterizacionGenetica, Proyecto
from app.models import User
from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()


class CepaRepository(SQLAlchemySyncRepository[Cepa]):
    model_type = Cepa
async def provide_cepa_repo(db_session: Session) -> CepaRepository:
    return CepaRepository(session=db_session)

class UserRepository(SQLAlchemySyncRepository[User]):
    model_type = User

    def add_with_password_hash(self, user: User, **kwargs) -> User:
        print(f"DEBUG: Intentando añadir usuario con datos: {user}")
        user.password = password_hasher.hash(user.password)

        return self.add(user, **kwargs)

    def check_password(self, username: str, password: str) -> bool:
        user = self.get_one_or_none(username=username)
        if not user:
            return False

        # --- INICIO DE CÓDIGO DE DEBUG ---
        print("--- DEBUG LOGIN ---")
        print(f"Password recibido (plain text): '{password}'")
        print(f"Hash en la BD: '{user.password}'")
        try:
            is_valid = password_hasher.verify(password, user.password)
            print(f"Resultado de la verificación: {is_valid}")
        except Exception as e:
            print(f"ERROR durante la verificación: {e}")
            is_valid = False
        print("--- FIN DEBUG ---")
        # --- FIN DE CÓDIGO DE DEBUG ---

        return is_valid # Retorna el resultado de la verificación
    def resequence_table_ids(
    self,
    table_name: str,
    sequence_name: str,
    deleted_id: int
    ) -> int:
        """
        Tras eliminar un registro con `deleted_id`, corre los IDs > deleted_id
        y reinicia la secuencia a MAX(id)+1.

        Devuelve el próximo valor de la secuencia.
        """
        session: Session = self.session
        # 1) Mover todos los IDs hacia arriba
        session.execute(
            text(f"UPDATE {table_name} SET id = id - 1 WHERE id > :deleted_id"),
            {"deleted_id": deleted_id},
        )
        # 2) Calcular nuevo máximo
        result = session.execute(text(f"SELECT MAX(id) FROM {table_name}"))
        max_id = result.scalar() or 0
        next_id = max_id + 1
        # 3) Reiniciar la secuencia
        session.execute(
            text(f"ALTER SEQUENCE {sequence_name} RESTART WITH :next_id"),
            {"next_id": next_id},
        )
        return next_id
    
    def get_next_table_id(self, table_name: str) -> int:
        """
        Calcula MAX(id) + 1 para la tabla indicada.
        Si la tabla está vacía devuelve 1.
        """
        session: Session = self.session
        result = session.execute(text(f"SELECT MAX(id) FROM {table_name}"))
        max_id = result.scalar() or 0
        return max_id + 1

    
async def provide_user_repo(db_session: Session) -> UserRepository:
    return UserRepository(session=db_session)