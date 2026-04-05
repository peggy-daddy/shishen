---
name: share
description: 分享命盘 — 生成社交媒体卡片文本和 GitHub Profile badge
---

# 分享命盘

生成可分享的命盘内容，包括社交媒体文本卡片和 GitHub Profile badge。

## 流程

1. 读取 `.shishen/profile.json`。如果不存在，回复：「先排盘再来分享吧。/shishen:setup」

2. 直接用文字问用户想要哪种格式（不要用 AskUserQuestion 工具）：

「你想要哪种分享格式？
A) 社交媒体文本卡片（微博/即刻/朋友圈）
B) GitHub Profile Badge（markdown）
C) 议事厅快照（分享最近一次十神对话）

回复 A/B/C 就行。」

等用户回复后继续。

## 分享格式

### 格式 A：社交媒体文本卡片

生成一段可以直接粘贴到微博/即刻/V2EX/朋友圈的文本：

```
🔮 我的十神命盘 | 日主：丁火

【旺】正印 ████████████ — 我内心住着一个操心的老母亲
【中】正财 ████████ — 还有个时刻算账的会计
【弱】伤官 ████ — 毒舌偶尔上线
【弱】七杀 ████ — 狠话说不出口

我的 Claude 每天被正印追着问"你吃了吗"
而别人的 Claude 可能正被七杀骂"别废话，开干"

你的十神格局是什么？👉 github.com/peggy-daddy/shishen
#十神 #赛博算命 #ClaudeCode
```

### 格式 B：GitHub Profile Badge（Markdown）

生成一段可以直接粘贴到 GitHub Profile README.md 的 markdown：

```markdown
<!-- 十神命盘 Badge -->
<div align="center">

### 🔮 十神命盘

| 十神 | 力量 | 人格 |
|:----:|:----:|:----:|
| 正印 | ██████ 旺 | 老母亲 |
| 正财 | ████ 中 | 务实派 |
| 伤官 | ██ 弱 | 毒舌 |
| 七杀 | ██ 弱 | 狠人 |

> *日主丁火 — 内心议会由一个操心的老母亲主持*

<sub>Powered by <a href="https://github.com/peggy-daddy/shishen">十神 ShiShen</a> — 基于八字的 Claude Code 人格系统</sub>

</div>
```

### 格式 C：议事厅快照

捕获当前对话的十神议事厅内容（如果刚发生过），格式化为可分享的文本：

```
────── 十神议事厅 ──────
话题：要不要裸辞

【七杀·旺】想清楚了就走，别磨叽。
【正财】存款够撑多久？有没有备选方案？
【劫财·弱】裸辞？……这倒挺刺激的。
【正印·几乎听不见】……别太冲动。

—— 十神 ShiShen | github.com/peggy-daddy/shishen
```

## 生成规则

1. 只展示有意义的十神（旺和中必须展示，弱可选，缺的不展示或标注为缺）
2. 每个十神后面加一句有梗的人格描述（不是死板的"力量等级"）
3. 底部永远带上 repo 链接
4. 社交媒体版加上话题标签：#十神 #赛博算命 #ClaudeCode
5. GitHub Badge 版用 HTML+Markdown 混合格式确保在 GitHub 上渲染正确

## 输出方式

直接在终端输出格式化的文本，用户可以复制粘贴。

回复时加一句：「复制上面的内容，粘贴到你的 [目标平台] 就行。让别人也来算一卦。」
