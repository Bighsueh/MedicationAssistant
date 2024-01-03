from sqlalchemy import create_engine, Column, BigInteger, String, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import os

DATABASE_URL = os.environ.get("DATABASE_URL")
#DATABASE_URL='postgresql://postgres:0921457822@localhost:5432/postgres'
#DATABASE_URL='postgresql://postgres:1234@localhost:5432/aitest'

# 創建資料庫引擎
engine = create_engine(DATABASE_URL)

# 声明基底
Base = declarative_base()

class MedicationRecord(Base):
    __tablename__ = "medication_records"

    record_id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(String(50))
    redate = Column(Date, default=None)
    pres_hosp = Column(String(255), default=None)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    #medication_record_details = relationship("MedicationRecordDetail", back_populates="medication_record")

class MedicationRecordDetail(Base):
    __tablename__ = "medication_record_detail"

    detail_id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    record_id = Column(BigInteger, ForeignKey("medication_records.record_id"))
    trade_name = Column(String(255), default=None)
    generic_name = Column(String(255), default=None)
    # dose = Column(String(255), default=None)
    dose_per_unit = Column(String(255), default=None)
    dose_per_time = Column(String(255), default=None)
    dose_per_day = Column(String(255), default=None)
    # freq = Column(String(255), default=None)
    day_limit = Column(String(255), default=None)
    morning =  Column(Boolean, default=False)
    noon = Column(Boolean, default=False)
    night = Column(Boolean, default=False)
    bed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    medication_record = relationship("MedicationRecord", back_populates="medication_record_details")

# 在資料庫中創建資料表
def create_tables():
    Base.metadata.create_all(engine)