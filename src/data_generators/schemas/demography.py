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

    # ========== 第 2 部分：人口统计学信息 ==========

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


# ========== 测试代码 ==========
if __name__ == "__main__":
    # 创建一个 DM 记录
    dm = DemographyRecord(
        USUBJID="XYZ-001-0001",
        AGE=35,
        SEX="M",
        RACE="ASIAN"
    )

    print("DM 记录创建成功")
    print(f"受试者：{dm.USUBJID}")
    print(f"年龄：{dm.AGE}")
    print(f"性别：{dm.SEX}")
