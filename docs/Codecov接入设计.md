# Codecov 接入设计

本文描述为 `new-school-sdk` 接入 [Codecov](https://about.codecov.io/) 覆盖率追踪的设计方案与实施蓝图。本轮仅完成设计定稿，配置变更按本文第 6 节的步骤单独实施。

## 1. 目标与范围

**做什么**

- 为 `school_sdk/` 建立可见的测试覆盖率追踪
- 每次 push / PR 自动生成覆盖率报告，PR 中以 Codecov bot 评论展示变化
- README 展示覆盖率徽章
- 为后续"以覆盖率门控 PR"保留演进路径

**不做什么**

- 不改变现有 `tests.yml` 六档矩阵与文档构建 job 的行为
- 不引入阻塞性的覆盖率状态检查（见第 4 节决策）
- 不要求本地开发必须运行覆盖率采集

## 2. 现状分析

| 维度 | 现状 |
| --- | --- |
| CI 测试 | `tests.yml`：pytest 六档矩阵（py3.8–3.13）+ `mkdocs build --strict`，全程无覆盖率采集 |
| 测试资产 | 仅 `tests/test_offline_smoke.py` 10 个离线用例，覆盖课表、成绩、会话失效、Cookie 解析等路径 |
| 未覆盖区 | 登录编排（`ZFLogin`）、验证码识别（`check_code/`）、`PyRsa`、`Info` 的 HTML 解析 |
| 覆盖率工具链 | 未安装 `pytest-cov` / `coverage`，无 `codecov.yml` |

!!! note "初始覆盖率的诚实预期"
    当前用例集中在使用 mock 响应的业务解析路径，登录与验证码模块零覆盖，接入后的初始覆盖率预计在 **20%–35%** 区间（实测为 **52%**，高于预期，因业务解析路径被离线用例覆盖得比较扎实）。这是起点而非目标，不应成为推迟接入或提前自满的理由。

## 3. 关键设计决策

| 决策点 | 选择 | 理由 |
| --- | --- | --- |
| 报告使用方式 | **仅信息展示**：不设阻塞性状态检查 | 当前用例少、基线低，严格门控会阻塞正常开发；先建立可见性，待覆盖面稳定后再收紧（第 8 节 Phase 3） |
| 上传来源 | **单一专职 coverage job**（py3.12） | 矩阵六档全部上传会产生 6 份重复报告与合并噪音；离线测试与 Python 版本几乎无关，单点采集足够代表 |
| 上传 action | `codecov/codecov-action@v5` | 官方维护；**v4 起即使公开仓库也必须提供 token**（tokenless 上传已废弃） |
| Codecov 侧配置文件 | **不引入 `codecov.yml`**，按社区 quickstart 最小接入 | 默认行为已满足 Phase 1 需求；状态检查默认不参与合并门控（除非手动加入分支保护），与"仅信息展示"定位天然一致 |
| 覆盖率后端 | pytest-cov（coverage.py） | pytest 原生插件，`--cov` 单参数启用，无需改写测试 |
| flags 分组 | 不引入 | 单一数据源，无需按单元/集成拆分报告，保持配置最简 |

## 4. 方案设计

### 4.1 覆盖率采集

dev 依赖组新增 `pytest-cov`（`pyproject.toml` `[dependency-groups].dev`）：

```toml
[dependency-groups]
dev = [
    "autopep8==1.5.7",
    "pre-commit>=3",
    "pytest>=7",
    "pytest-cov>=5",
]
```

!!! note "版本约束说明"
    只设下界不设上界，与全项目依赖声明约定一致（运行时依赖同样仅设下界，参见 `pyproject.toml`）。pytest-cov 会随 uv 通用锁按 Python 版本自动分叉，coverage job 固定在 py3.12 运行，不存在 py3.8 的兼容边界问题。

coverage.py 的行为约束写入 `pyproject.toml`：

```toml
[tool.coverage.run]
source = ["school_sdk"]
omit = [
    "school_sdk/PyRsa/*",     # vendored jsbn 移植, 非本仓库维护的代码
    "tests/*",
    "examples/*",
]

[tool.coverage.report]
show_missing = true
```

`source = ["school_sdk"]` 保证未导入的模块（如 `check_code/predict.py`）也计入分母，避免覆盖率虚高。

!!! note "check_code/ 的覆盖预期"
    `check_code/` 的 CNN 分支依赖 optional extra `kaptcha`（torch/torchvision），CI 的 coverage job 不安装该 extra，这部分代码会长期显示为未覆盖。这是预期行为，待 Phase 2 引入带 kaptcha extra 的专用 fixture 后再补齐。

### 4.2 CI：新增专职 coverage job

在 `tests.yml` 中与现有矩阵 job **并列**新增，不改动任何既有 job：

```yaml
  coverage:
    name: coverage (py3.12)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
        with:
          python-version: "3.12"
      - run: uv sync
      - name: Run tests with coverage
        run: uv run pytest tests/ -v --cov=school_sdk --cov-report=xml --cov-report=term-missing
      - name: Upload coverage reports to Codecov
        uses: codecov/codecov-action@v5
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
```

要点：

- 上传步骤按社区 quickstart 的最简形式编写：action 会自动发现工作区的 `coverage.xml`，无需显式指定 `files`
- 不设 `fail_ci_if_error`，采用 action 默认行为；codecov-action 自身已内置重试
- 生成的 `coverage.xml` 需加入 `.gitignore`，防止本地运行后误提交

### 4.3 Codecov 侧配置：不引入 `codecov.yml`

按社区 quickstart 接入，仓库内不创建 `codecov.yml`。无配置文件时 Codecov 采用默认行为：自动识别上传的报告、在 PR 中发布评论与状态检查。其中状态检查默认不会阻塞合并——只有被手动加入 GitHub 分支保护的 required checks 才会产生门控效果，这与"仅信息展示"定位天然一致。

排除 `PyRsa/` 等 vendored 代码的职责由本地 `[tool.coverage.run]` 的 `omit` 承担：上传的 `coverage.xml` 中本来就不含这些文件，Codecov 端无需重复声明 ignore。

若 Phase 3 需要门控或自定义评论布局，再按需引入 `codecov.yml` 或在 Codecov 网页端配置。

### 4.4 README 徽章

`README.md` 的徽章区混合了 Markdown 与 HTML `<a>` 写法，在现有 `[![Downloads]...]` 一行之后追加即可（Markdown 徽章与 HTML 徽章可混排）：

```markdown
[![codecov](https://codecov.io/gh/FarmerChillax/new-school-sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/FarmerChillax/new-school-sdk)
```

## 5. 人工配置步骤（非代码，需仓库管理员操作）

1. 用 GitHub 账号登录 [codecov.io](https://about.codecov.io/)，在仓库列表中激活 `FarmerChillax/new-school-sdk`
2. 进入仓库 Settings，复制 **Repository Upload Token**
3. 在 GitHub 仓库 Settings → Secrets and variables → Actions 中新增 secret：名称 `CODECOV_TOKEN`，值为上一步的 token
4. （可选）确认分支保护的 required checks 中**未**包含 Codecov 的状态检查——只要不加进去，状态检查就始终不阻塞合并

!!! warning "Token 安全"
    token 只存放在 GitHub Actions secret 与 Codecov 后台，不写入任何仓库文件、文档或示例代码。workflow 中仅通过 `${{ secrets.CODECOV_TOKEN }}` 引用。

## 6. 实施清单

按以下顺序执行，全部为小步变更：

1. `pyproject.toml`：dev 组加 `pytest-cov>=5`，新增 `[tool.coverage.run]` / `[tool.coverage.report]`；随后 `uv lock`（新增包均为纯 Python，无 wheel 风险，但刷新 lock 时须遵守"定点升级而非整体降级"约定，避免陈旧 pin 复现 Pillow 8.3.1 式的 CI 失败，背景见[架构设计](架构设计.md)第 12 节）
2. `.gitignore`：追加 `coverage.xml`、`.coverage`
3. `tests.yml`：追加 coverage job（内容见 4.2）；不创建 `codecov.yml`（见 4.3）
4. `README.md`：追加徽章（内容见 4.4）
5. 完成第 5 节的人工配置（激活仓库 + 配置 secret）
6. 推送并在 PR 中验证

## 7. 验证方式

- **本地**：`uv run --with pytest-cov pytest tests/ --cov=school_sdk --cov-report=term` 应输出逐模块覆盖率表，退出码 0
- **CI**：coverage job 绿色；Codecov 页面出现首份报告；PR 评论区出现 Codecov bot 的 diff 摘要；README 徽章渲染出数字（首次可能有几分钟缓存延迟）

## 8. 分阶段演进

| 阶段 | 内容 | 触发条件 |
| --- | --- | --- |
| Phase 1（本次） | 信息展示 + 徽章 + PR 评论 | — |
| Phase 2 | 补登录流程（mock CSRF/公钥响应）、`Info` HTML 快照 fixture；可选增加带 `kaptcha` extra 的 coverage job 覆盖 `check_code/` | 本 PR 合并后 |
| Phase 3 | 转为门控：将 Codecov 状态检查加入分支保护的 required checks，并引入 `codecov.yml` 设定 project 基线目标值与 patch 新增代码阈值 | 覆盖率稳定且团队认可阈值 |

## 9. 风险与注意事项

- **初始数字低引起误读**：在 README 徽章旁无需额外说明，但 Phase 1 期间不宜在对外沟通中引用覆盖率数字作为质量论据
- **token 失效**：Codecov token 轮换后 CI 上传会静默失败（action 默认不因上传失败阻塞），需依赖 PR 评论消失这一信号察觉；建议纳入第 5 节第 4 步的检查习惯
- **pytest-cov 版本漂移**：未来 pytest 大版本升级若与 pytest-cov 不兼容，锁定策略与本文 4.1 节约定一致——定点处理，不动无关依赖
