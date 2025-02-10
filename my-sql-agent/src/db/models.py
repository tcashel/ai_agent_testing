"""
Database models and schema definitions.
"""
from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship, declarative_base, Mapped

Base = declarative_base()

class Customer(Base):
    """Customer model representing business clients."""
    __tablename__ = 'customers'
    
    customer_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sales: Mapped[List["Sale"]] = relationship("Sale", back_populates="customer")
    
    # Indexes
    __table_args__ = (
        Index('idx_customer_email', email),
    )

class Sale(Base):
    """Sales transactions with revenue and amount tracking."""
    __tablename__ = 'sales'
    
    sale_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    sales_amount = Column(Float, nullable=False)
    revenue = Column(Float, nullable=False)
    product_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    customer: Mapped["Customer"] = relationship("Customer", back_populates="sales")
    
    # Indexes
    __table_args__ = (
        Index('idx_sale_date', date),
        Index('idx_sale_customer', customer_id),
    )

class Product(Base):
    """Product catalog with pricing information."""
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1000))
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes
    __table_args__ = (
        Index('idx_product_name', name),
    ) 