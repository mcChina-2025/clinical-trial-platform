"""
DM 域（Demographics - 人口统计学）数据模型

这个文件定义了 DM 表单的数据结构。
"""

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, Field


class DemographyRecord(BaseModel):
    """
    DM 域 - 人口统计学记录

    这是一个简化版，只包含最核心的字段
    """

    # ========== 第 1 部分：基础标识 ==========

    USUBJID: str = Field(
        ...,
        description="唯一受试者标识符",
        pattern=r"^[A-Z]{3}-\d{3}-\d{4}$"
    )

    # ========== 第 2 部分：日期信息 ==========

    BRTHDTC: date = Field(
        ...,
        description="出生日期"
    )

    RFSTDTC: date = Field(
        ...,
        description="首次给药日期"
    )

    # ========== 第 3 部分：人口统计学信息 ==========

    AGE: int = Field(
        ...,
        ge=18,
        le=100,
        description="年龄"
    )

    SEX: Literal["M", "F"] = Field(
        ...,
        description="性别"
    )

    RACE: str = Field(
        ...,
        description="种族"
    )

    # ========== 第 4 部分：治疗组信息 ==========

    ARMCD: str = Field(
        ...,
        description="治疗组代码",
        examples=["TRT", "PLACEBO"]
    )

    ARM: str = Field(
        ...,
        description="治疗组描述",
        examples=["Treatment Group", "Placebo Group"]
    )


# ========== 测试代码 ==========
if __name__ == "__main__":
    # 创建一个 DM 记录
    dm = DemographyRecord(
        USUBJID="XYZ-001-0003",
        BRTHDTC=date(1990, 5, 20),
        RFSTDTC=date(2024, 1, 15),
        AGE=33,
        SEX="M",
        RACE="ASIAN",
        ARMCD="TRT",
        ARM="Treatment Group"
    )

    print("DM 记录创建成功")
    print(f"受试者：{dm.USUBJID}")
    print(f"出生日期：{dm.BRTHDTC}")
    print(f"首次给药：{dm.RFSTDTC}")
    print(f"年龄：{dm.AGE}")
    print(f"性别：{dm.SEX}")
    print(f"治疗组：{dm.ARM}")
