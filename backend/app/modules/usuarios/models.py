from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50)
    full_name: str = Field(max_length=120)
    email: str = Field(index=True, unique=True, max_length=255)
    hashed_password: str
    role: str = Field(default="user", max_length=20)
    disabled: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    pedidos: list["Pedido"] = Relationship(back_populates="usuario")
