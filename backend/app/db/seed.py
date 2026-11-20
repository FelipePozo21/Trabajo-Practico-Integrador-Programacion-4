from sqlmodel import Session, select
from app.core.database import create_all_tables, engine
from app.core.security import hash_password
from app.modules.usuarios.models import Usuario
from app.modules.categorias.models import Categoria
from app.modules.productos.models import Producto

def seed():
    create_all_tables()
    with Session(engine) as s:
        admin=s.exec(select(Usuario).where(Usuario.username=="admin")).first()
        if admin is None:
            admin=Usuario(username="admin",full_name="Administrador Food Store",email="admin@foodstore.local",hashed_password=hash_password("Admin1234!"),role="admin",disabled=False)
            s.add(admin)
        else:
            # Reestablece las credenciales publicadas para el usuario demo al volver a correr el seed.
            admin.full_name="Administrador Food Store"
            admin.email="admin@foodstore.local"
            admin.hashed_password=hash_password("Admin1234!")
            admin.role="admin"
            admin.disabled=False
            s.add(admin)
        cats=[("Hamburguesas","Clásicas y especiales"),("Pizzas","Pizzas artesanales"),("Bebidas","Bebidas frías")]
        category_images={
            "Hamburguesas":"/images/products/hamburguesa.png",
            "Pizzas":"/images/products/pizza.png",
            "Bebidas":"/images/products/bebida.png",
        }
        for name,desc in cats:
            c=s.exec(select(Categoria).where(Categoria.nombre==name)).first()
            if not c: c=Categoria(nombre=name,descripcion=desc);s.add(c);s.flush()
            products=[(f"{name} especial", "Selección de la casa", 8500.0, 20),(f"{name} clásica", "Un favorito", 6500.0, 25),(f"{name} premium", "Ingredientes frescos", 9900.0, 12)]
            for pname,d,p,stock in products:
                product=s.exec(select(Producto).where(Producto.nombre==pname)).first()
                if not product:
                    s.add(Producto(categoria_id=c.id,nombre=pname,descripcion=d,precio_base=p,stock=stock,imagen_url=category_images[name],disponible=True))
                elif not product.imagen_url:
                    product.imagen_url=category_images[name]
                    s.add(product)
        s.commit()
if __name__=="__main__": seed()
