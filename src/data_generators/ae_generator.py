"""
AE 数据生成器

用 Faker 生成随机的 AE 记录
"""

from datetime import date, timedelta

from faker import Faker

from src.data_generators.schemas.adverse_event import AdverseEventRecord


class AEGenerator:
    """AE 数据生成器"""

    # 常见的不良事件术语
    AE_TERMS = [
        "Headache",
        "Nausea",
        "Fatigue",
        "Dizziness",
        "Diarrhea",
        "Vomiting",
        "Fever",
        "Cough",
        "Rash",
        "Insomnia"
    ]

    def __init__(self, n_subjects: int = 10, ae_rate: float = 0.7):
        """
        初始化生成器

        参数：
            n_subjects: 受试者数量
            ae_rate: AE 发生率（0-1），0.7 表示 70% 的受试者会有 AE
        """
        self.n_subjects = n_subjects
        self.ae_rate = ae_rate
        self.fake = Faker()

    def generate(self, dm_records: list = None) -> list[AdverseEventRecord]:
        """
        生成 AE 记录

        参数：
            dm_records: DM 记录列表（用于获取受试者信息和首次给药日期）

        返回：
            AE 记录列表
        """
        records = []

        for i in range(self.n_subjects):
            usubjid = f"XYZ-001-{i+1:04d}"

            # 70% 的受试者会有 AE
            if self.fake.random.random() > self.ae_rate:
                continue  # 这个受试者没有 AE

            # 每个有 AE 的受试者，随机生成 1-3 个 AE
            n_aes = self.fake.random_int(min=1, max=3)

            for seq in range(1, n_aes + 1):
                # 生成 AE 开始日期（2024年）
                ae_start = self.fake.date_between(
                    start_date=date(2024, 2, 1),
                    end_date=date(2024, 11, 30)
                )

                # 80% 的 AE 会结束，20% 还在持续
                ae_end = None
                if self.fake.random.random() < 0.8:
                    # 持续 1-30 天
                    duration = self.fake.random_int(min=1, max=30)
                    ae_end = ae_start + timedelta(days=duration)

                # 严重程度分布：60% MILD, 30% MODERATE, 10% SEVERE
                rand = self.fake.random.random()
                if rand < 0.6:
                    severity = "MILD"
                elif rand < 0.9:
                    severity = "MODERATE"
                else:
                    severity = "SEVERE"

                # 严重不良事件（SAE）：只有 SEVERE 的才可能是 SAE
                is_serious = "Y" if severity == "SEVERE" and self.fake.random.random() < 0.3 else "N"

                # 与药物的关系
                relationship = self.fake.random_element([
                    "RELATED",
                    "PROBABLY RELATED",
                    "POSSIBLY RELATED",
                    "NOT RELATED"
                ])

                ae = AdverseEventRecord(
                    USUBJID=usubjid,
                    AESEQ=seq,
                    AETERM=self.fake.random_element(self.AE_TERMS),
                    AESTDTC=ae_start,
                    AEENDTC=ae_end,
                    AESEV=severity,
                    AESER=is_serious,
                    AEREL=relationship
                )
                records.append(ae)

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

        print(f"已生成 {len(records)} 条 AE 记录，保存到 {filename}")


# ========== 测试代码 ==========
if __name__ == "__main__":
    # 创建生成器
    generator = AEGenerator(n_subjects=10, ae_rate=0.7)

    # 生成数据
    records = generator.generate()

    # 打印统计信息
    print(f"生成了 {len(records)} 条 AE 记录")
    print(f"涉及 {len(set(r.USUBJID for r in records))} 个受试者\n")

    # 打印前 5 条
    print("前 5 条记录：")
    for i, ae in enumerate(records[:5], 1):
        status = "已结束" if ae.AEENDTC else "持续中"
        print(f"{i}. {ae.USUBJID} - {ae.AETERM} - {ae.AESEV} - {status}")

    # 导出 CSV
    generator.to_csv("ae_sample.csv")
