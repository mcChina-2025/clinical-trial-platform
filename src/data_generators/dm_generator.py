"""
DM 数据生成器 - 简化版

用 Faker 生成随机的 DM 记录
"""

from datetime import date

from faker import Faker

from src.data_generators.schemas.demography import DemographyRecord


class DMGenerator:
    """DM 数据生成器"""

    def __init__(self, n_subjects: int = 100):
        """
        初始化生成器

        参数：
            n_subjects: 要生成的受试者数量
        """
        self.n_subjects = n_subjects
        self.fake = Faker()

    def generate(self) -> list[DemographyRecord]:
        """
        生成 DM 记录

        返回：
            DM 记录列表
        """
        records = []

        for i in range(self.n_subjects):
            # 生成首次给药日期（2024年）
            rfstdtc = self.fake.date_between(
                start_date=date(2024, 1, 1),
                end_date=date(2024, 12, 31)
            )

            # 生成年龄（18-80 岁）
            age = self.fake.random_int(min=18, max=80)

            # 根据年龄和首次给药日期计算出生日期
            birth_year = rfstdtc.year - age
            # 随机生成月和日
            birth_date = self.fake.date_between(
                start_date=date(birth_year, 1, 1),
                end_date=date(birth_year, 12, 31)
            )

            # 重新验证年龄（确保准确）
            calculated_age = rfstdtc.year - birth_date.year
            if (rfstdtc.month, rfstdtc.day) < (birth_date.month, birth_date.day):
                calculated_age -= 1

            # 如果计算出的年龄不对，调整出生日期
            if calculated_age != age:
                birth_date = date(birth_year - 1, birth_date.month, birth_date.day)

            # 随机分配治疗组
            arm_choice = self.fake.random_element(["TRT", "PLACEBO"])
            arm_desc = "Treatment Group" if arm_choice == "TRT" else "Placebo Group"

            # 生成一条 DM 记录
            dm = DemographyRecord(
                USUBJID=f"XYZ-001-{i+1:04d}",
                BRTHDTC=birth_date,
                RFSTDTC=rfstdtc,
                AGE=age,
                SEX=self.fake.random_element(["M", "F"]),
                RACE=self.fake.random_element([
                    "ASIAN",
                    "WHITE",
                    "BLACK OR AFRICAN AMERICAN"
                ]),
                ARMCD=arm_choice,
                ARM=arm_desc
            )
            records.append(dm)

        return records

    def to_csv(self, filename: str):
        """
        导出为 CSV 文件

        参数：
            filename: 输出文件名
        """
        import pandas as pd

        records = self.generate()
        data = [r.model_dump() for r in records]

        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

        print(f"已生成 {len(records)} 条记录，保存到 {filename}")


# ========== 测试代码 ==========
if __name__ == "__main__":
    # 创建生成器
    generator = DMGenerator(n_subjects=10)

    # 生成数据
    records = generator.generate()

    # 打印前 3 条
    print(f"生成了 {len(records)} 条 DM 记录\n")
    print("前 3 条记录：")
    for i, dm in enumerate(records[:3], 1):
        print(f"{i}. {dm.USUBJID} - {dm.AGE}岁 - {dm.SEX} - {dm.RACE}")

    # 导出 CSV
    generator.to_csv("dm_sample.csv")
