"""
基础数据模型定义

这个文件包含所有临床数据表单共用的基础类和工具函数。
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ClinicalRecord(BaseModel):
    """
    所有临床数据记录的基类

    为什么要有这个基类？
    - 所有临床数据都有 STUDYID 和 USUBJID
    - 统一定义一次，其他表单继承就行
    - 类似于 CRF 表单的"公共页眉"
    """

    STUDYID: str = Field(
        ...,
        description="Study Identifier（研究编号）",
        pattern=r"^[A-Z]{3}-\d{3}$",  # 格式：XYZ-001
        examples=["XYZ-001", "ABC-002"]
    )

    USUBJID: str = Field(
        ...,
        description="Unique Subject Identifier（唯一受试者标识符）",
        pattern=r"^[A-Z]{3}-\d{3}-\d{4}$",  # 格式：XYZ-001-0001
        examples=["XYZ-001-0001", "ABC-002-0123"]
    )

    class Config:
        """
        Pydantic 配置类

        这里可以设置模型的行为：
        - str_strip_whitespace: 自动去除字符串首尾空格
        - validate_assignment: 赋值时也验证（不只是初始化时）
        """
        str_strip_whitespace = True
        validate_assignment = True


# 常用的 CDISC 受控术语（Controlled Terminology）
# 这些是 CDISC 标准规定的固定值，不能随便写

SEX_VALUES = ["M", "F", "U", "UNDIFFERENTIATED"]  # 性别
"""
M = Male（男性）
F = Female（女性）
U = Unknown（未知）
UNDIFFERENTIATED = 未分化（罕见）
"""

RACE_VALUES = [
    "AMERICAN INDIAN OR ALASKA NATIVE",
    "ASIAN",
    "BLACK OR AFRICAN AMERICAN",
    "NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER",
    "WHITE",
    "MULTIPLE",
    "OTHER",
    "UNKNOWN"
]
"""CDISC 标准种族分类"""

ETHNIC_VALUES = [
    "HISPANIC OR LATINO",
    "NOT HISPANIC OR LATINO",
    "NOT REPORTED",
    "UNKNOWN"
]
"""CDISC 标准民族分类"""

AGE_UNIT_VALUES = ["YEARS", "MONTHS", "WEEKS", "DAYS"]
"""年龄单位"""


def generate_usubjid(study_id: str, site_id: str, subject_seq: int) -> str:
    """
    生成标准格式的 USUBJID

    参数：
        study_id: 研究编号，如 "XYZ-001"
        site_id: 中心编号，如 "001"
        subject_seq: 受试者序号，如 1, 2, 3...

    返回：
        USUBJID，如 "XYZ-001-001-0001"

    例子：
        >>> generate_usubjid("XYZ-001", "001", 1)
        'XYZ-001-001-0001'
        >>> generate_usubjid("ABC-002", "005", 123)
        'ABC-002-005-0123'
    """
    return f"{study_id}-{site_id}-{subject_seq:04d}"


def calculate_age(birth_date: date, reference_date: date) -> int:
    """
    计算年龄（按年）

    参数：
        birth_date: 出生日期
        reference_date: 参考日期（通常是知情同意日期或首次给药日期）

    返回：
        年龄（整数）

    例子：
        >>> from datetime import date
        >>> calculate_age(date(1990, 5, 15), date(2024, 1, 10))
        33
    """
    age = reference_date.year - birth_date.year

    # 如果今年还没过生日，年龄减 1
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age
