# 数学建模竞赛一键工作流 / Mathematical Modeling Contest Workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Open Source](https://img.shields.io/badge/status-open--source-brightgreen.svg)](#开源状态--open-source-status)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-black.svg)](SKILL.md)

> 面向 CUMCM、MCM/ICM 等数学建模竞赛，从审题、数据处理、建模、验证到论文交付的端到端 Skill。
>
> An end-to-end skill for CUMCM, MCM/ICM, and similar contests, covering problem framing, data work, modeling, validation, and paper delivery.

## 中文介绍

### 能力范围

- 建立问题、数据与假设台账
- 选择可解释的基线并实施有限的有效改进
- 执行敏感性、稳健性与误差分析
- 生成论文结构、图表与公式交付物
- 按竞赛规则、AI 合规和评审视角做最终检查

### 适用场景

需要把一道数学建模赛题推进到可复现、可审校的完整论文时。

### 设计方式

`SKILL.md` 是唯一入口，先完成场景分诊，再按需读取 `references/` 中的专题资料。这样既保留关键约束，又避免把所有领域知识一次性装入上下文。脚本仅用于可重复、可验证的机械操作。

### 安装

```powershell
git clone https://github.com/GongGongPlus/skill-cumcm-one-click.git "$env:USERPROFILE\.codex\skills\cumcm-one-click"
```

安装后重新打开 Codex 会话，让 Skill 目录重新被发现。也可以直接在任务中点名 `$cumcm-one-click`。

### 使用示例

```text
请使用 $cumcm-one-click 处理这个任务，并把已验证事实、工程推论和待验证项分开报告。
```

### 证据与边界

不编造数据、结果、引用或官方规则；当届要求必须以赛事官网为准，模拟结果必须明确标注。

本仓库提供工作流与判断框架，不替代官方规则、专业认证、生产环境审批或真实设备验证。执行涉及资金、硬件熔丝、生产部署、外部提交等高风险操作前，必须取得明确授权。

## English

### Scope

- Maintain problem, data, and assumption ledgers
- Choose interpretable baselines and make limited justified improvements
- Run sensitivity, robustness, and error analysis
- Produce paper structures, figures, and formula-ready deliverables
- Check contest rules, AI compliance, and judge-facing quality gates

### Best fit

When a modeling problem must become a reproducible, reviewable, complete paper.

### Design

`SKILL.md` is the single entry point. It triages the request first and loads only the relevant files under `references/`. This preserves important constraints without loading the entire knowledge base into context. Scripts are reserved for repeatable, verifiable mechanical work.

### Installation

```bash
git clone https://github.com/GongGongPlus/skill-cumcm-one-click.git "$HOME/.codex/skills/cumcm-one-click"
```

Start a fresh Codex session after installation so the skill directory is rediscovered. You can also invoke it explicitly as `$cumcm-one-click`.

### Example prompt

```text
Use $cumcm-one-click for this task. Separate verified facts, engineering inferences, and items that still need validation.
```

### Evidence boundary

Never fabricate data, results, citations, or official rules; current competition requirements must be checked against official sources, and simulated results must be labeled.

This repository provides workflows and decision support. It does not replace official rules, professional certification, production approval, or real-device validation. Explicit authorization is required before high-risk actions involving funds, hardware fuses, production deployment, or external submission.

## Repository structure / 仓库结构

```text
skill-cumcm-one-click/
|-- agents/
|   |-- openai.yaml
|-- assets/
|   |-- ai-tool-usage-details.md
|   |-- paper-skeleton.md
|-- references/
|   |-- ai-compliance.md
|   |-- checklist.md
|   |-- contest-insights.md
|   |-- data-preprocessing-visualization.md
|   |-- judging-and-strategy.md
|   |-- model-construction.md
|   |-- model-cookbook.md
|   |-- model-innovation.md
|   |-- model-validation.md
|   |-- paper-depth-visual-density.md
|   |-- paper-requirements.md
|   |-- paper-writing.md
|   |-- problem-reading.md
|   |-- result-visualization.md
|   |-- sample-paper-style.md
|   |-- typography-and-python-figures.md
|   |-- word-latex-formulas.md
|-- scripts/
|   |-- audit_data.py
|   |-- sensitivity.py
|   |-- verify_docx_figures.py
|   |-- verify_docx_math.py
|   |-- verify_docx_typography.py
|-- static/
|-- manifest.yaml
|-- README.md
|-- SKILL.md
```

Reference topics / 专题资料：

- `references/ai-compliance.md`
- `references/checklist.md`
- `references/contest-insights.md`
- `references/data-preprocessing-visualization.md`
- `references/judging-and-strategy.md`
- `references/model-construction.md`
- `references/model-cookbook.md`
- `references/model-innovation.md`
- `references/model-validation.md`
- `references/paper-depth-visual-density.md`
- `references/paper-requirements.md`
- `references/paper-writing.md`
- `references/problem-reading.md`
- `references/result-visualization.md`
- `references/sample-paper-style.md`
- `references/typography-and-python-figures.md`
- `references/word-latex-formulas.md`

## Author / 作者

- Author and maintainer / 作者与维护者：**中北大学机器人协会续晋全**
- GitHub: [@GongGongPlus](https://github.com/GongGongPlus)
- Collection index / 总索引：[GongGongPlus/agent-skills-index](https://github.com/GongGongPlus/agent-skills-index)

The author statement identifies the maintainer and original integrator of this repository. Referenced third-party projects retain their own authorship and rights.

作者信息表示本仓库的维护者与原创整合者；被引用的第三方项目仍保留其原作者身份与相关权利。

## 开源状态 / Open-source status

- Visibility / 可见性：**Public / 公开**
- Status / 状态：**Open source / 开源**
- License / 许可证：[MIT](LICENSE)
- Warranty / 担保：按“原样”提供，不承诺适用于特定目的 / Provided as-is, without warranty
- Third-party boundary / 第三方边界：见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)

欢迎在遵守许可证与证据边界的前提下使用、修改和分发。Issues 与 Pull Requests 可用于报告可复现问题或提交改进。

Use, modification, and redistribution are welcome under the license and evidence boundaries. Issues and pull requests may be used for reproducible bug reports and improvements.
