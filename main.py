from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from typing import List
#Version 3.10.11
#pip install PyMySQL
#pip install uvicorn
#uvicorn main:app
#http://127.0.0.1:8000/docs
#https://www.uvicorn.org/
#https://fastapi.tiangolo.com/es/deployment/manually/#usa-el-comando-fastapi-run

#python -m venv .venv
#python -m pip install --upgrade pip
#pip install "fastapi[standard]"

# Configuración de la base de datos
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/bdapifast"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definición del modelo Producto (corregido según la base de datos)
class Producto(Base):
    __tablename__ = "producto"
    id = Column(String, primary_key=True, index=True)
    nom = Column(String, index=True)
    pre = Column(Float)
    rang = Column(Integer)
    img = Column(String)

# Creación de la tabla en la BD (si no existe)
Base.metadata.create_all(bind=engine)

# Esquema de validación con Pydantic
class ProductoSchema(BaseModel):
    id: str
    nom: str
    pre: float
    rang: int
    img: str

    class Config:
        from_attributes = True  # Para Pydantic v2

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicialización de FastAPI
app = FastAPI()

# 🟢 Crear un producto
@app.post("/producto/", response_model=ProductoSchema)
def crear_producto(producto: ProductoSchema, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

# 🔵 Obtener un producto por ID
@app.get("/producto/{producto_id}", response_model=ProductoSchema)
def obtener_producto(producto_id: str, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# 🟣 Listar todos los productos
@app.get("/productos/", response_model=List[ProductoSchema])
def listar_productos(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    if not productos:
        raise HTTPException(status_code=404, detail="No hay productos registrados")
    return productos

# 🟠 Actualizar un producto
@app.put("/productos/{producto_id}", response_model=ProductoSchema)
def actualizar_producto(producto_id: str, producto: ProductoSchema, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    datos_actualizados = producto.model_dump()
    datos_actualizados.pop("id", None)  # Evitar actualizar la clave primaria

    for key, value in datos_actualizados.items():
        setattr(db_producto, key, value)

    db.commit()
    db.refresh(db_producto)
    return db_producto

# 🔴 Eliminar un producto
@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: str, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(db_producto)
    db.commit()
    return {"mensaje": "Producto eliminado exitosamente"}


# Ejecutar FastAPI con Uvicorn
if __name__ == "__main__":
    import uvicorn
    #uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run(app, host="172.56.0.238", port=8080)