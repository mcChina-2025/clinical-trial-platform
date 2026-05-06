"""
统一数据生成脚本

一次性生成完整的临床试验数据集
"""

import pandas as pd
from pathlib import Path

from src.data_generators.dm_generator import DMGenerator
from src.data_generators.ae_generator import AEGenerator


def generate_complete_dataset(n_subjects: int = 100, output_dir: str = "data"):
    """
    生成完整的临床试验数据集

    参数：
        n_subjects: 受试者数量
        output_dir: 输出目录
    """
    print(f"开始生成 {n_subjects} 个受试者的数据...\n")

    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # ========== 1. 生成 DM 数据 ==========
    print("1. 生成 DM（人口统计学）数据...")
    dm_generator = DMGenerator(n_subjects=n_subjects)
    dm_records = dm_generator.generate()

    # 转换为 DataFrame
    dm_data = [r.model_dump() for r in dm_records]
    dm_df = pd.DataFrame(dm_data)

    # 保存 CSV
    dm_file = output_path / "dm.csv"
    dm_df.to_csv(dm_file, index=False)
    print(f"   已生成 {len(dm_records)} 条 DM 记录 -> {dm_file}")

    # ========== 2. 生成 AE 数据 ==========
    print("\n2. 生成 AE（不良事件）数据...")
    ae_generator = AEGenerator(n_subjects=n_subjects, ae_rate=0.7)
    ae_records = ae_generator.generate()

    # 转换为 DataFrame
    ae_data = [r.model_dump() for r in ae_records]
    ae_df = pd.DataFrame(ae_data)

    # 保存 CSV
    ae_file = output_path / "ae.csv"
    ae_df.to_csv(ae_file, index=False)
    print(f"   已生成 {len(ae_records)} 条 AE 记录 -> {ae_file}")

    # ========== 3. 数据统计 ==========
    print("\n" + "=" * 60)
    print("数据集统计")
    print("=" * 60)

    print(f"\n【DM 数据】")
    print(f"  受试者总数: {len(dm_df)}")
    print(f"  性别分布:")
    print(f"    男性 (M): {len(dm_df[dm_df['SEX'] == 'M'])} ({len(dm_df[dm_df['SEX'] == 'M']) / len(dm_df) * 100:.1f}%)")
    print(f"    女性 (F): {len(dm_df[dm_df['SEX'] == 'F'])} ({len(dm_df[dm_df['SEX'] == 'F']) / len(dm_df) * 100:.1f}%)")

    print(f"\n  年龄统计:")
    print(f"    平均年龄: {dm_df['AGE'].mean():.1f} 岁")
    print(f"    年龄范围: {dm_df['AGE'].min()} - {dm_df['AGE'].max()} 岁")

    print(f"\n  治疗组分布:")
    arm_counts = dm_df['ARMCD'].value_counts()
    for arm, count in arm_counts.items():
        print(f"    {arm}: {count} ({count / len(dm_df) * 100:.1f}%)")

    print(f"\n【AE 数据】")
    print(f"  AE 总数: {len(ae_df)}")
    print(f"  有 AE 的受试者: {ae_df['USUBJID'].nunique()}")
    print(f"  AE 发生率: {ae_df['USUBJID'].nunique() / len(dm_df) * 100:.1f}%")

    print(f"\n  严重程度分布:")
    sev_counts = ae_df['AESEV'].value_counts()
    for sev, count in sev_counts.items():
        print(f"    {sev}: {count} ({count / len(ae_df) * 100:.1f}%)")

    print(f"\n  最常见的 AE（Top 5）:")
    top_ae = ae_df['AETERM'].value_counts().head(5)
    for term, count in top_ae.items():
        print(f"    {term}: {count} 次")

    print("\n" + "=" * 60)
    print(f"数据已保存到 {output_dir}/ 目录")
    print("=" * 60)

    return dm_df, ae_df


if __name__ == "__main__":
    # 生成数据
    dm_df, ae_df = generate_complete_dataset(n_subjects=100, output_dir="data")

    print("\n提示：你可以用 pandas 进一步分析数据")
    print("例如：")
    print("  import pandas as pd")
    print("  dm = pd.read_csv('data/dm.csv')")
    print("  ae = pd.read_csv('data/ae.csv')")
