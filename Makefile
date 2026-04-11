.PHONY: help venv install install-dev lint format test test-cov clean

# 默认目标
.DEFAULT_GOAL := help

help: ## 显示所有可用命令
	@echo "临床试验数据智能平台 - 常用命令"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# 虚拟环境
venv: ## 创建虚拟环境 (.venv)
	@echo "创建虚拟环境..."
	uv venv

# 依赖安装
install: ## 安装核心依赖
	@echo "安装核心依赖..."
	uv pip install -e "."

install-dev: ## 安装开发依赖（包括 ruff, pytest）
	@echo "安装开发依赖..."
	uv pip install -e ".[dev]"

# 代码质量
lint: ## 运行 ruff 检查代码风格
	@echo "运行代码检查..."
	@ruff check src tests || true

format: ## 用 ruff 格式化代码
	@echo "格式化代码..."
	@ruff format src tests

format-check: ## 检查代码是否已格式化
	@echo "检查代码格式..."
	@ruff format --check src tests

# 测试
test: ## 运行所有测试
	@echo "运行测试..."
	pytest

test-cov: ## 运行测试并生成覆盖率报告
	@echo "运行测试（含覆盖率）..."
	pytest --cov=src --cov-report=html --cov-report=term-missing
	@echo "覆盖率报告已生成：htmlcov/index.html"

test-unit: ## 仅运行单元测试
	@echo "运行单元测试..."
	pytest tests/unit -v

test-integration: ## 仅运行集成测试
	@echo "运行集成测试..."
	pytest tests/integration -v

# 清理
clean: ## 清理临时文件和缓存
	@echo "清理临时文件..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name .coverage -exec rm {} + 2>/dev/null || true
	@echo "清理完成！"

# 完整工作流
check: format lint test ## 格式化 + 检查 + 测试（提交前运行）

.PHONY: check
