import datetime
import uuid
from typing import List, Optional

from sqlalchemy import UUID, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.extensions import db

dataset_field = db.Table(
    "dataset_field",
    db.Column("dataset", Text, ForeignKey("dataset.dataset"), primary_key=True),
    db.Column("field", Text, ForeignKey("field.field"), primary_key=True),
)


class DateModel(db.Model):
    __abstract__ = True

    entry_date: Mapped[datetime.date] = mapped_column(
        Date, default=datetime.datetime.today
    )
    start_date: Mapped[Optional[datetime.date]] = mapped_column(
        Date, onupdate=datetime.datetime.today
    )
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)


class Specification(DateModel):
    __tablename__ = "specification"

    specification: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    datasets: Mapped[List["Dataset"]] = relationship(
        "Dataset",
        back_populates="specification",
    )

    @property
    def parent_dataset(self):
        return self.ordered_datasets[0]

    @property
    def ordered_datasets(self):
        ds = []
        for dataset in sorted(
            self.datasets, key=lambda d: (d.parent is not None, d.dataset)
        ):
            ds.append(dataset)
        return ds


class Dataset(DateModel):
    __tablename__ = "dataset"

    dataset: Mapped[str] = mapped_column(primary_key=True)
    parent: Mapped[Optional[str]] = mapped_column(
        ForeignKey("dataset.dataset"), nullable=True
    )
    specification_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("specification.specification"), nullable=True
    )
    is_geography: Mapped[bool] = mapped_column(default=False)
    specification: Mapped[Optional["Specification"]] = relationship(
        "Specification",
        back_populates="datasets",
    )
    fields: Mapped[List["Field"]] = relationship(
        "Field",
        secondary=dataset_field,
        back_populates="datasets",
    )
    records: Mapped[List["Record"]] = relationship(
        "Record",
        back_populates="dataset",
    )
    children: Mapped[List["Dataset"]] = relationship(
        "Dataset",
    )

    @property
    def name(self):
        return self.dataset.replace("-", " ")


# @total_ordering
class Field(DateModel):
    __tablename__ = "field"

    field: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    category_reference: Mapped[Optional[str]] = mapped_column(
        Text, ForeignKey("category.reference")
    )
    datatype: Mapped[Optional[str]] = mapped_column(Text)
    datasets: Mapped[List["Dataset"]] = relationship(
        "Dataset",
        secondary=dataset_field,
        back_populates="fields",
    )
    category: Mapped[Optional["Category"]] = relationship(
        "Category",
    )


class Record(DateModel):
    __tablename__ = "record"

    id: Mapped[uuid.uuid4] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    data: Mapped[dict] = mapped_column(MutableDict.as_mutable(JSONB))
    dataset_dataset: Mapped[str] = mapped_column(ForeignKey("dataset.dataset"))
    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="records")


class Category(DateModel):
    __tablename__ = "category"
    reference: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(Text)
    values: Mapped[List["CategoryValue"]] = relationship(
        "CategoryValue",
        back_populates="category",
    )


class CategoryValue(DateModel):
    __tablename__ = "category_value"

    prefix: Mapped[str] = mapped_column(Text, primary_key=True)
    reference: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    category_reference: Mapped[str] = mapped_column(ForeignKey("category.reference"))
    category: Mapped["Category"] = relationship("Category", back_populates="values")
