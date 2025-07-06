from advanced_alchemy.repository import SQLAlchemySyncRepository
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
    
async def provide_user_repo(db_session: Session) -> UserRepository:
    return UserRepository(session=db_session)