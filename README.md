# Conduit API 接口测试与自动化回归

对开源博客系统 **Conduit** 的接口测试实践：从接口梳理、用例设计、手工执行，到 pytest 自动化回归的完整闭环。

> **说明**：被测项目是第三方开源项目。本仓库**仅包含我编写的测试代码与测试文档，不含被测项目的任何源码**。

## 被测对象

| 项目 | 说明 |
| --- | --- |
| 仓库 | [borys25ol/fastapi-realworld-backend](https://github.com/borys25ol/fastapi-realworld-backend) |
| 规范 | [RealWorld](https://github.com/gothinkster/realworld) API Spec |
| 技术栈 | FastAPI + SQLAlchemy + SQLite |
| 本地地址 | `http://127.0.0.1:8899`（由被测服务提供） |

## 仓库内容

| 文件 | 说明 |
| --- | --- |
| `接口清单.csv` | 梳理出的 20 个接口：模块、方法、路径、参数、鉴权要求 |
| `测试用例表.csv` | 15 条手工用例及执行结果 |
| `测试报告.md` | 测试范围、执行统计、验证到的校验规则、遗留风险 |
| `autotest/` | pytest 自动化用例 |
| `autotest/conftest.py` | fixture：自动注册独立用户、统一管理 JWT 鉴权头 |
| `autotest/report.html` | pytest-html 生成的测试报告 |
| `requirements.txt` | 依赖清单 |

## 测试覆盖面

- **接口规模**：20 个 REST 接口
- **用例设计维度**：正常流 / 参数校验 / 边界值 / 鉴权异常 / 业务冲突 / 数据一致性
- **手工用例**：15 条（鉴权 4、文章 9、用户 2），全部执行
- **自动化用例**：13 条（9 个测试函数经参数化展开），全量回归约 2 秒

### 已验证的关键行为

- JWT 为三段式结构；无 token、伪造 token、截断 token 均被拒绝，且错误信息可区分「格式错误」与「签名错误」两类失败
- `description`、`body` 字段最小长度 10 字符（以 9 / 10 字符对照验证）
- 文章列表 `limit` 参数：传 `0`、负数、非数字字符均返回 422
- 重复邮箱注册被拒绝，错误信息精确到 `email` 字段
- 未登录创建文章返回 403

### 已识别的遗留风险

**`limit` 参数无上限校验**：传入 `limit=99999` 仍返回 200 并全量返回数据。在大数据量场景下存在被恶意拉取全表的风险，建议服务端增加分页上限或强制分页。

## 运行方式

**前置条件**：被测服务已在本机 `127.0.0.1:8899` 启动（需另行部署，不在本仓库内）。

```bash
# 1. 创建虚拟环境
python -m venv .venv

# 2. 安装依赖
# Windows
.venv\Scripts\python.exe -m pip install -r requirements.txt
# macOS / Linux
.venv/bin/python -m pip install -r requirements.txt

# 3. 执行全部用例
# Windows
.venv\Scripts\python.exe -m pytest autotest -v
# macOS / Linux
.venv/bin/python -m pytest autotest -v

# 4. 生成 HTML 报告
.venv\Scripts\python.exe -m pytest autotest --html=autotest/report.html --self-contained-html
```

预期结果：`13 passed`。

## 环境要求

- Python 3.10+
- pytest / requests / pytest-html

## 技术要点

- **fixture 管理登录态**：每个用例执行前自动注册独立用户并注入 JWT 鉴权头，用例之间互不干扰
- **uuid 随机数据**：注册信息带随机后缀，保证用例可重复执行，不依赖数据库既有状态
- **parametrize 数据驱动**：边界值与异常值以参数化方式组织，一条函数覆盖多组数据
- **断言**：同时校验 HTTP 状态码与关键业务字段，而非只看状态码
