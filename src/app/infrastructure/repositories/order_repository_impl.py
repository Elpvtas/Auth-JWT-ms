from abc import ABC
from typing import List, Optional
from datetime import datetime
from src.app.domain.entities.order import Order
from src.app.domain.repositories.crud_repository import CrudRepository
from src.app.infrastructure.database.db_connection_factory import DatabaseConectionFactory


class OrdenRepositoryImpl(CrudRepository[Order], ABC):

    def get_all(self) -> List[Order]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM Orden WHERE deleted_at IS NULL")
                rows = cursor.fetchall()
                return [Order(**row) for row in rows]
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def get_by_id(self, id: int) -> Optional[Order]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM Orden WHERE id = %s AND deleted_at IS NULL", (id,))
                row = cursor.fetchone()
                return Order(**row) if row else None
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def create(self, orden: Order) -> Order:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Orden (tipo_orden, precio, fecha_hora, comision, usuario_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    orden.tipo_orden,
                    orden.precio,
                    orden.fecha_hora,
                    orden.comision,
                    orden.usuario_id
                ))
                connection.commit()
                cursor.execute("SELECT LAST_INSERT_ID()")
                orden.id = cursor.fetchone()[0]
                return orden
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def update(self, id: int, orden: Order) -> Optional[Order]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Orden SET
                        tipo_orden = %s,
                        precio = %s,
                        fecha_hora = %s,
                        comision = %s,
                        usuario_id = %s,
                        update_at = NOW()
                    WHERE id = %s AND deleted_at IS NULL
                """, (
                    orden.tipo_orden,
                    orden.precio,
                    orden.fecha_hora,
                    orden.comision,
                    orden.usuario_id,
                    id
                ))
                connection.commit()
                return self.get_by_id(id)
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def delete(self, id: int) -> bool:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE Orden SET deleted_at = %s WHERE id = %s AND deleted_at IS NULL", (datetime.now(), id))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            DatabaseConectionFactory.release_connection(connection)
