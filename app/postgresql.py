# from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm import declarative_base, Session, relationship
# from sqlalchemy.sql import func
# from databases import Database

# DATABASE_URL = "postgresql://postgres:0921457822@localhost:5432/PostgreSQL16"

# database = Database(DATABASE_URL)
# metadata = declarative_base()


# class MedicationRecord(metadata):
#     __tablename__ = "medication_records"

#     record_id = Column(Integer, primary_key=True, index=True)
#     redate = Column(DateTime, default=None)
#     pres_hosp = Column(String(255), default=None)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


# class MedicationRecordDetail(metadata):
#     __tablename__ = "medication_record_detail"

#     detail_id = Column(Integer, primary_key=True, index=True)
#     record_id = Column(Integer, ForeignKey("medication_records.record_id"))
#     trade_name = Column(String(255), default=None)
#     generic_name = Column(String(255), default=None)
#     dose = Column(String(255), default=None)
#     dose_per_unit = Column(String(255), default=None)
#     daily_dose = Column(String(255), default=None)
#     freq = Column(String(255), default=None)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

#     medication_record = relationship("MedicationRecord", back_populates="medication_record_details")

# MedicationRecord.medication_record_details = relationship("MedicationRecordDetail", back_populates="medication_record")
# MedicationRecordDetail.medication_record = relationship("MedicationRecord", back_populates="medication_record_details")


from sqlalchemy import create_engine, Column, BigInteger, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import os

DATABASE_URL = os.environ.get("DATABASE_URL")
# DATABASE_URL='postgresql://postgres:0921457822@localhost:5432/postgres'

# 創建資料庫引擎
engine = create_engine(DATABASE_URL)

# 声明基底
Base = declarative_base()

class MedicationRecord(Base):
    __tablename__ = "medication_records"

    record_id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    redate = Column(Date, default=None)
    pres_hosp = Column(String(255), default=None)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    medication_record_details = relationship("MedicationRecordDetail", back_populates="medication_record")

class MedicationRecordDetail(Base):
    __tablename__ = "medication_record_detail"

    detail_id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    record_id = Column(BigInteger, ForeignKey("medication_records.record_id"))
    trade_name = Column(String(255), default=None)
    generic_name = Column(String(255), default=None)
    dose = Column(String(255), default=None)
    dose_per_unit = Column(String(255), default=None)
    daily_dose = Column(String(255), default=None)
    freq = Column(String(255), default=None)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    medication_record = relationship("MedicationRecord", back_populates="medication_record_details")

# 在資料庫中創建資料表
def create_tables():
    Base.metadata.create_all(engine)