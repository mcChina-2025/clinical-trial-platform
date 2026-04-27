"""
AE 域（Adverse Events - 不良事件）数据模型

这个文件定义了 AE 表单的数据结构。
"""

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field


class AdverseEventRecord(BaseModel):
    """
    AE 域 - 不良事件记录

    一个受试者可以有多条 AE 记录
    """

    # ========== 基础标识 ==========

    USUBJID: str = Field(
        ...,
        description="唯一受试者标识符",
        pattern=r"^[A-Z]{3}-\d{3}-\d{4}$"
    )

    AESEQ: int = Field(
        ...,
        ge=1,
        description="AE 序号（同一受试者的第几个 AE）"
    )

    # ========== 不良事件描述 ==========

    AETERM: str = Field(
        ...,
        description="不良事件术语",
        examples=["Headache", "Nausea", "Fatigue"]
    )

    # ========== 日期信息 ==========

    AESTDTC: date = Field(
        ...,
        description="AE 开始日期"
    )

    AEENDTC: Optional[date] = Field(
        default=None,
        description="AE 结束日期（可能还在持续）"
    )

    # ========== 严重程度 ==========

    AESEV: Literal["MILD", "MODERATE", "SEVERE"] = Field(
        ...,
        description="严重程度"
    )

    AESER: Literal["Y", "N"] = Field(
        ...,
        description="是否为严重不良事件（Serious AE）"
    )

    # ========== 与药物的关系 ==========

    AEREL: Literal["RELATED", "PROBABLY RELATED", "POSSIBLY RELATED", "NOT RELATED"] = Field(
        ...,
        description="与研究药物的关系"
    )


# ========== 测试代码 ==========
if __name__ == "__main__":
    # 创建一个 AE 记录
    ae = AdverseEventRecord(
        USUBJID="XYZ-001-0001",
        AESEQ=1,
        AETERM="Headache",
        AESTDTC=date(2024, 2, 15),
        AEENDTC=date(2024, 2, 20),
        AESEV="MILD",
        AESER="N",
        AEREL="POSSIBLY RELATED"
    )

    print("AE 记录创建成功")
    print(f"受试者：{ae.USUBJID}")
    print(f"不良事件：{ae.AETERM}")
    print(f"开始日期：{ae.AESTDTC}")
    print(f"结束日期：{ae.AEENDTC}")
    print(f"严重程度：{ae.AESEV}")
