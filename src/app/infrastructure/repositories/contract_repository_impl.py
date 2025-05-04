# src/app/infrastructure/repositories/contrato_repository_impl.py

from abc import ABC
from typing import List, Optional
from datetime import datetime
from src.app.domain.entities.contract import Contract
from src.app.domain.repositories.crud_repository import CrudRepository
from src.app.infrastructure.database.db_connection_factory import DatabaseConectionFactory


class ContratoRepositoryImpl(CrudRepository[Contract], ABC):

    def get_all(self) -> List[Contract]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Contrato WHERE deleted_at IS NULL")
                rows = cursor.fetchall()
                return [
                    Contract(
                        numero_contrato=row[0],
                        fecha_hora_inicio=row[1],
                        fecha_hora_fin=row[2],
                        comision=row[3],
                        inversionista_id=row[4],
                        comisionista_id=row[5],
                        created_at=row[6],
                        update_at=row[7],
                        deleted_at=row[8]
                    ) for row in rows
                ]
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def get_by_id(self, numero_contrato: int) -> Optional[Contract]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Contrato WHERE numero_contrato = %s AND deleted_at IS NULL", (numero_contrato,))
                row = cursor.fetchone()
                if row:
                    return Contract(
                        numero_contrato=row[0],
                        fecha_hora_inicio=row[1],
                        fecha_hora_fin=row[2],
                        comision=row[3],
                        inversionista_id=row[4],
                        comisionista_id=row[5],
                        created_at=row[6],
                        update_at=row[7],
                        deleted_at=row[8]
                    )
                return None
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def create(self, contrato: Contract) -> Contract:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Contrato (
                        fecha_hora_inicio, fecha_hora_fin, comision,
                        inversionista_id, comisionista_id
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (
                    contrato.fecha_hora_inicio,
                    contrato.fecha_hora_fin,
                    contrato.comision,
                    contrato.inversionista_id,
                    contrato.comisionista_id
                ))

                connection.commit()
                # Obtener el ID autogenerado
                cursor.execute("SELECT LAST_INSERT_ID()")
                contrato.numero_contrato = cursor.fetchone()[0]
                return contrato
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def update(self, numero_contrato: int, contrato: Contract) -> Optional[Contract]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Contrato SET
                        fecha_hora_inicio = %s,
                        fecha_hora_fin = %s,
                        comision = %s,
                        inversionista_id = %s,
                        comisionista_id = %s
                    WHERE numero_contrato = %s
                """, (
                    contrato.fecha_hora_inicio,
                    contrato.fecha_hora_fin,
                    contrato.comision,
                    contrato.inversionista_id,
                    contrato.comisionista_id,
                    numero_contrato
                ))
                connection.commit()
                return self.get_by_id(numero_contrato)
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def delete(self, numero_contrato: int) -> bool:
        """Soft delete: actualiza el campo deleted_at"""
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Contrato SET deleted_at = %s WHERE numero_contrato = %s
                """, (datetime.now(), numero_contrato))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            DatabaseConectionFactory.release_connection(connection)
