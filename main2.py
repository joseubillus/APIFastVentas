from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from typing import List
#Version 3.10.11
#pip install PyMySQL
#pip install uvicorn
#uvicorn main:app --reload

# Configuración de la base de datos
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/bdapifast"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MODELO: Producto (ya existente)
class Producto(Base):
    __tablename__ = "producto"
    id = Column(String, primary_key=True, index=True)
    nom = Column(String, index=True)
    pre = Column(Float)
    rang = Column(Integer)
    img = Column(String)

# 🆕 MODELO: Usuario
class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_usuario = Column(String(50), nullable=False)
    contrasena = Column(String(255), nullable=False)

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# ESQUEMAS Pydantic
class ProductoSchema(BaseModel):
    id: str
    nom: str
    pre: float
    rang: int
    img: str

    class Config:
        from_attributes = True

class UsuarioSchema(BaseModel):
    id: int
    nombre_usuario: str
    contrasena: str

    class Config:
        from_attributes = True

class UsuarioCreate(BaseModel):
    nombre_usuario: str
    contrasena: str

# DEPENDENCIA
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# APP
app = FastAPI()

# ---------------- PRODUCTOS (igual que tenías) ----------------

@app.post("/producto/", response_model=ProductoSchema)
def crear_producto(producto: ProductoSchema, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.get("/producto/{producto_id}", response_model=ProductoSchema)
def obtener_producto(producto_id: str, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.get("/productos/", response_model=List[ProductoSchema])
def listar_productos(db: Session = Depends(get_db)):
    productos = db.query(Producto).all()
    return productos

@app.put("/productos/{producto_id}", response_model=ProductoSchema)
def actualizar_producto(producto_id: str, producto: ProductoSchema, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in producto.model_dump().items():
        if key != "id":
            setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: str, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(db_producto)
    db.commit()
    return {"mensaje": "Producto eliminado exitosamente"}

# ---------------- USUARIOS (nuevo) ----------------

# 🟢 Crear un usuario
@app.post("/usuario/", response_model=UsuarioSchema)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = Usuario(**usuario.model_dump())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# 🔵 Obtener un usuario por ID
@app.get("/usuario/{usuario_id}", response_model=UsuarioSchema)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# 🟣 Listar todos los usuarios
@app.get("/usuarios/", response_model=List[UsuarioSchema])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    return usuarios

# 🔴 Eliminar usuario
@app.delete("/usuario/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado exitosamente"}

@app.post("/login/")
def login(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(
        Usuario.nombre_usuario == usuario.nombre_usuario,
        Usuario.contrasena == usuario.contrasena
    ).first()

    if not db_usuario:
        raise HTTPException(status_code=401, detail="mensaje: credenciales incorrectas")

    return {"mensaje": "Autorizado", "usuario_id": db_usuario.id}

# Ejecutar FastAPI con Uvicorn si es ejecutado directamente
if __name__ == "__main__":
    import uvicorn
    #uvicorn.run(app, host="127.0.0.1", port=8000)
    #uvicorn.run(app, host="172.56.0.238", port=8080)
    uvicorn.run(app, host="192.168.18.4", port=8080)