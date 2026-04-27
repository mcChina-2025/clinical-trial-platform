"""
DM 数据生成器 - 简化版

用 Faker 生成随机的 DM 记录
"""

from faker import Faker

from src.data_generators.schemas.demography import DemographyRecord


class DMGenerator:
    """DM 数据生成器"""

    def __init__(self, n_subjects: int = 10):
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
            # 生成一条 DM 记录
            dm = DemographyRecord(
                USUBJID=f"XYZ-001-{i+1:04d}",  # XYZ-001-0001, 0002, ...
                AGE=self.fake.random_int(min=18, max=80),
                SEX=self.fake.random_element(["M", "F"]),
                RACE=self.fake.random_element([
                    "ASIAN",
                    "WHITE",
                    "BLACK OR AFRICAN AMERICAN"
                ])
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
