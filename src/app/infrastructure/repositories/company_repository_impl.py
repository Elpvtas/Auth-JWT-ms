from abc import ABC
from typing import List, Optional
from src.app.domain.entities.company import Company
from src.app.domain.repositories.crud_repository import CrudRepository
from src.app.infrastructure.database.db_connection_factory import DatabaseConectionFactory


class CompanyRepositoryImpl(CrudRepository[Company], ABC):

    def get_all(self) -> List[Company]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Empresa")
                rows = cursor.fetchall()
                return [
                    Company(
                        id=row[0],
                        nombre=row[1],
                        descripcion=row[2],
                        sector_economico_id=row[3],
                        created_at=row[4],
                        update_at=row[5],
                        deleted_at=row[6],
                    ) for row in rows
                ]
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def get_by_id(self, company_id: int) -> Optional[Company]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Empresa WHERE id = %s", (company_id,))
                row = cursor.fetchone()
                if row:
                    return Company(
                        id=row[0],
                        nombre=row[1],
                        descripcion=row[2],
                        sector_economico_id=row[3],
                        created_at=row[4],
                        update_at=row[5],
                        deleted_at=row[6],
                    )
                return None
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def create(self, company: Company) -> Company:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Empresa (nombre, descripcion, sector_economico_id)
                    VALUES (%s, %s, %s)
                """, (
                    company.nombre,
                    company.descripcion,
                    company.sector_economico_id
                ))
                company.id = cursor.lastrowid
                connection.commit()
                return company
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def update(self, company_id: int, company: Company) -> Optional[Company]:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Empresa SET
                        nombre = %s,
                        descripcion = %s,
                        sector_economico_id = %s,
                        update_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (
                    company.nombre,
                    company.descripcion,
                    company.sector_economico_id,
                    company_id
                ))
                connection.commit()
                return self.get_by_id(company_id)
        finally:
            DatabaseConectionFactory.release_connection(connection)

    def delete(self, company_id: int) -> bool:
        connection = DatabaseConectionFactory.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Empresa WHERE id = %s", (company_id,))
                affected = cursor.rowcount
                connection.commit()
                return affected > 0
        finally:
            DatabaseConectionFactory.release_connection(connection)
