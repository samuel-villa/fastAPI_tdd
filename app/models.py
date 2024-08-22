import sqlalchemy
from sqlalchemy import (
    DECIMAL,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID

from .db_connection import Base

"""
For the DB construction we will refer to this schema:
https://lucid.app/lucidchart/dcf7e614-f071-4832-99b6-361b13db1a9f/edit?invitationId=inv_12607d3e-7a85-4489-83fd-0aa57812706f&page=0_0#
"""


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    slug = Column(String(120), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    level = Column(Integer, nullable=False, default="100", server_default="100")
    parent_id = Column(Integer, ForeignKey("category.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="category_name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="category_slug_length_check"),
        UniqueConstraint("name", "level", name="uq_category_name_level"),
        UniqueConstraint("slug", name="uq_category_slug"),
    )


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, nullable=False)
    pid = Column(
        UUID(as_uuid=True),
        nullable=False,
        server_default=text("gen_random_uuid()"),
    )
    name = Column(String(200), nullable=False)
    slug = Column(String(220), nullable=False)
    description = Column(Text, nullable=True)
    is_digital = Column(Boolean, nullable=False, default=False, server_default="False")
    created_at = Column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=sqlalchemy.func.now(),
        nullable=False,
    )
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    stock_status = Column(
        Enum("oos", "is", "obo", name="status_enum"),
        nullable=False,
        server_default="oos",
    )
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    seasonal_event_id = Column(Integer, ForeignKey("seasonal_event.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="product_name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="product_slug_length_check"),
        UniqueConstraint("pid", name="uq_product_pid"),
        UniqueConstraint("name", name="uq_product_name"),
        UniqueConstraint("slug", name="uq_product_slug"),
    )


class ProductLine(Base):
    __tablename__ = "product_line"

    id = Column(Integer, primary_key=True, nullable=False)
    price = Column(DECIMAL(5, 2), nullable=False)
    sku = Column(
        UUID(as_uuid=True),
        nullable=False,
        server_default=text("gen_random_uuid()"),
    )
    stock_qty = Column(Integer, nullable=False, default=0, server_default="0")
    is_active = Column(Boolean, nullable=False, default=False, server_default="False")
    order_num = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "price >= 0 AND price <= 999.99", name="product_line_max_value"
        ),
        CheckConstraint(
            "order_num >= 1 AND order_num <= 20", name="product_order_line_range"
        ),
        UniqueConstraint(
            "order_num", "product_id", name="uq_product_line_order_product_id"
        ),
        UniqueConstraint("sku", name="uq_product_line_sku"),
    )


class ProductImage(Base):
    __tablename__ = "product_image"

    id = Column(Integer, primary_key=True, nullable=False)
    alternative_text = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    order = Column(Integer, nullable=False)
    product_line_id = Column(Integer, ForeignKey("product_line.id"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "LENGTH(alternative_text) > 0", name="product_image_alt_text_length_check"
        ),
        CheckConstraint("LENGTH(url) > 0", name="product_image_url_length_check"),
        CheckConstraint(
            '"order" >= 1 AND "order" <= 20', name="product_image_order_range"
        ),
        UniqueConstraint(
            "order", "product_line_id", name="uq_product_image_order_product_line_id"
        ),
        UniqueConstraint("product_line_id", name="uq_product_image_product_line_id"),
    )


class SeasonalEvent(Base):
    __tablename__ = "seasonal_event"

    id = Column(Integer, primary_key=True, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    name = Column(String(100), nullable=False)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="seasonal_event_name_length_check"),
        UniqueConstraint("name", name="uq_seasonal_event_name"),
    )


class Attribute(Base):
    __tablename__ = "attribute"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="attribute_name_length_check"),
        UniqueConstraint("name", name="uq_attribute_name"),
    )


class ProductType(Base):
    __tablename__ = "product_type"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    level = Column(Integer, nullable=False)
    parent = Column(Integer, ForeignKey("product_type.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="product_type_name_length_check"),
        UniqueConstraint("name", "level", name="uq_product_type_name_level"),
    )


class AttributeValue(Base):
    __tablename__ = "attribute_value"

    id = Column(Integer, primary_key=True, nullable=False)
    attribute_value = Column(String(100), nullable=False)
    attribute_id = Column(Integer, ForeignKey("attribute_value.id"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "LENGTH(attribute_value) > 0", name="attribute_value_length_check"
        ),
        UniqueConstraint(
            "attribute_value",
            "attribute_id",
            name="uq_attribute_value_attr_value_attr_id",
        ),
    )


class ProductLineAttributeValue(Base):
    __tablename__ = "product_line_attribute_value"

    id = Column(Integer, primary_key=True, nullable=False)
    attribute_value_id = Column(
        Integer, ForeignKey("attribute_value.id"), nullable=False
    )
    product_line_id = Column(Integer, ForeignKey("product_line.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "attribute_value_id",
            "product_line_id",
            name="uq_attrval_prodline_attribute_value_id_produ_line_id",
        ),
    )


class ProductProductType(Base):
    __tablename__ = "product_product_type"

    id = Column(Integer, primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product_type_id = Column(Integer, ForeignKey("product_type.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "product_type_id",
            name="uq_prod_prodtype_prod_id_prod_type_id",
        ),
    )
