from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL
from datetime import datetime

#models that will be converted into tables using the sqlalchemy later!
class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    sales = relationship("Sales", back_populates="user", cascade="all, delete", passive_deletes=True)


class Categories(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)

    products = relationship("Products", back_populates="category", cascade="all, delete", passive_deletes=True)


class Suppliers(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)

    products = relationship("Products", back_populates="supplier", cascade="all, delete", passive_deletes=True)


class Products(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.category_id", ondelete="CASCADE"))
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id", ondelete="CASCADE"))
    cost_price = Column(DECIMAL, nullable=False)
    selling_price = Column(DECIMAL, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    category = relationship("Categories", back_populates="products", passive_deletes=True)
    supplier = relationship("Suppliers", back_populates="products", passive_deletes=True)
    inventory = relationship("Inventory", back_populates="product", uselist=False, cascade="all, delete", passive_deletes=True)
    sales = relationship("Sales", back_populates="product", cascade="all, delete", passive_deletes=True)


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship("Products", back_populates="inventory", passive_deletes=True)


class Sales(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)
    selling_price = Column(DECIMAL, nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    customer_name = Column(String, nullable=False)

    user = relationship("Users", back_populates="sales", passive_deletes=True)
    product = relationship("Products", back_populates="sales", passive_deletes=True)
