# 临床试验数据智能平台

## 项目简介

这是一个**企业级临床试验数据智能平台**，融合现代大数据技术栈与临床试验领域知识，展示端到端的数据工程、AI 应用、以及监管合规能力。

**核心目标**
- 🏗️ 掌握现代数据工程技术栈（Lakehouse、实时流处理、编排）
- 🔬 深化临床试验领域知识（CDISC 标准、数据质量、监管合规）
- 🤖 集成 AI/LLM 能力（RAG、异常检测、自然语言查询）
- 📊 构建企业级可视化仪表板

## 技术栈

### 核心技术
| 组件 | 技术 | 用途 |
|---|---|---|
| **云平台** | Azure | 云基础设施 |
| **Lakehouse** | Delta Lake + Azure Databricks | 数据存储与处理 |
| **流处理** | Apache Kafka + Spark Streaming | 实时数据摄取 |
| **批处理** | Apache Spark | 数据转换与聚合 |
| **编排** | Apache Airflow | 数据管道编排 |
| **数据质量** | Great Expectations | 自动化验证 |
| **后端** | FastAPI | REST API 服务 |
| **前端** | React + TypeScript | 仪表板可视化 |
| **AI/LLM** | Claude API | 智能助手与分析 |
| **基础设施** | Terraform + Docker | 基础设施即代码 |

## 项目结构

```
clinical-trial-platform/
├── src/
│   ├── data_generators/       # 合成数据生成器
│   ├── ingestion/             # 数据摄取层（Kafka → Bronze）
│   ├── transformation/        # 数据转换层（Bronze → Silver → Gold）
│   ├── quality/               # 数据质量验证引擎
│   ├── ai/                    # AI/LLM 模块（RAG、异常检测、NL2SQL）
│   └── api/                   # FastAPI 后端
├── frontend/                  # React 前端
├── orchestration/             # Airflow DAGs
├── infra/                     # Terraform 基础设施配置
├── tests/                     # 单元 & 集成测试
├── docs/                      # 技术文档
├── pyproject.toml             # 项目配置
├── docker-compose.yml         # 本地开发环境
└── Makefile                   # 常用命令
```

## 快速开始

### 前置条件
- Python 3.12+
- Git 2.40+
- Docker & Docker Compose（可选，用于完整体验）

### 本地开发环境设置

1. **克隆仓库**
   ```bash
   git clone <repo-url>
   cd clinical-trial-platform
   ```

2. **创建虚拟环境**
   ```bash
   uv venv
   source .venv/bin/activate  # 在 Windows 上: .venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   uv pip install -e ".[dev]"
   ```

4. **验证环境**
   ```bash
   make test        # 运行测试
   make lint        # 代码检查
   make format      # 代码格式化
   ```

## 学习路线（6 个月）

### 第 0 周：项目骨架 + Python 工程化
- ✅ 虚拟环境与依赖管理
- ✅ 代码风格与 linting（ruff）
- ✅ 测试框架（pytest）
- ✅ Git 工作流

### 第 1-2 周：闭环 1 — 合成数据生成器
- 学 Faker + Pydantic 数据建模
- 生成逼真的临床试验数据（DM/AE/CM/VS/LB）
- 单元测试覆盖

### 第 3-4 周：闭环 2 — Docker + Kafka + 数据流
- Docker Compose 编排本地 Kafka（Redpanda）
- Kafka 生产者/消费者
- 端到端数据流验证

### 第 5-8 周：闭环 3 — Spark + Delta Lake + Airflow
- PySpark 基础与 Delta Lake
- Bronze → Silver 数据转换
- Airflow DAG 编排

### 第 9-12 周：闭环 4 — 数据质量 + CDISC（业务优势）
- Great Expectations 自定义验证规则
- SDTM/ADaM 数据集生成
- Define-XML 生成

### 第 13-16 周：闭环 5 — FastAPI + React 前端
- REST API 开发
- React 仪表板（试验、质量、安全信号）
- JWT 认证

### 第 17-20 周：闭环 6 — AI 模块
- RAG 协议智能助手
- 异常检测 + Claude 解释
- NL-to-SQL 查询

### 第 21-24 周：集成 + 部署 + 文档
- 完整系统集成
- CI/CD 管道（GitHub Actions）
- Azure 云部署
- 项目文档与演示

## 常用命令

```bash
make help        # 查看所有命令
make lint        # 代码检查（ruff）
make format      # 代码格式化
make test        # 运行测试
make test-cov    # 运行测试并生成覆盖率报告
make clean       # 清理临时文件
```

## 贡献指南

1. 从 `main` 分支创建新分支：`git checkout -b feature/your-feature`
2. 提交代码前运行：`make lint && make test`
3. 推送分支并创建 Pull Request
4. 等待 CI/CD 检查通过

## 参考资源

### 官方文档
- [Pydantic](https://docs.pydantic.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Apache Spark](https://spark.apache.org/docs/latest/)
- [Delta Lake](https://docs.delta.io/)
- [Claude API](https://docs.anthropic.com/)

### 临床试验标准
- [CDISC 标准](https://www.cdisc.org/)
- [21 CFR Part 11](https://www.fda.gov/regulatory-information/fda-regulations/title-21-code-federal-regulations-part-11-electronic-records-electronic-signatures)
- [FHIR R4](https://www.hl7.org/fhir/)

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 联系方式

👤 **Mingchao**
- GitHub: [@mingchao](https://github.com/mingchao)

---

**最后更新**: 2026-04-11
