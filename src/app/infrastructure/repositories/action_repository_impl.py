# src/app/infrastructure/repositories/accion_repository_impl.py
from abc import ABC
from typing import List, Optional
from src.app.domain.entities.action import Accion
from src.app.domain.repositories.crud_repository import CrudRepository
from src.app.infrastructure.database.db_connection_factory import DatabaseConectionFactory


class AccionRepositoryImpl(CrudRepository[Accion], ABC):

    def get_all(self) -> List[Accion]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Accion")
                rows = cursor.fetchall()
                return [
                    Accion(
                        id=row[0],
                        nombre=row[1],
                        valor=row[2],
                        fecha_hora=row[3],
                        empresa_id=row[4],
                    ) for row in rows
                ]
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def get_by_id(self, accion_id: int) -> Optional[Accion]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Accion WHERE id = %s", (accion_id,))
                row = cursor.fetchone()
                if row:
                    return Accion(
                        id=row[0],
                        nombre=row[1],
                        valor=row[2],
                        fecha_hora=row[3],
                        empresa_id=row[4],
                    )
                return None
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def create(self, accion: Accion) -> Accion:
        connection = DatabaseConectionFactory.get_connection()
        try:
            all_acciones = self.get_all()  # Obtén todas las acciones
            nuevo_id = len(all_acciones) + 1

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Accion (nombre, valor, fecha_hora, empresa_id)
                    VALUES (%s, %s, %s, %s)
                """, (
                    accion.nombre,
                    accion.valor,
                    accion.fecha_hora,
                    accion.empresa_id
                ))
                accion.id = nuevo_id
                connection.commit()
                return accion
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def update(self, accion_id: int, accion: Accion) -> Optional[Accion]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Accion SET
                        nombre = %s,
                        valor = %s,
                        fecha_hora = %s,
                        empresa_id = %s
                    WHERE id = %s
                """, (
                    accion.nombre,
                    accion.valor,
                    accion.fecha_hora,
                    accion.empresa_id,
                    accion_id
                ))
                connection.commit()
                return self.get_by_id(accion_id)
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def delete(self, accion_id: int) -> bool:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Accion WHERE id = %s", (accion_id,))
                affected = cursor.rowcount
                connection.commit()
                return affected > 0
        finally:
            DatabaseConectionFactory.release_connection(connection)
