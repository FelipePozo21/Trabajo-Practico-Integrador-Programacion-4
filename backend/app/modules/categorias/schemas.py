from pydantic import field_validator
from sqlmodel import SQLModel, Field
class CategoriaCreate(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: str | None = None
class CategoriaUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    descripcion: str | None = None

    @field_validator("nombre", mode="before")
    @classmethod
    def nombre_no_puede_ser_nulo(cls, value):
        if value is None:
            raise ValueError("El nombre no puede ser nulo")
        return value
class CategoriaRead(SQLModel):
    id: int
    nombre: str
    descripcion: str | None
    activo: bool
