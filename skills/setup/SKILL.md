---
name: setup
description: 初始排盘 — 输入生辰信息，算出你的四柱八字和十神格局
---

# 十神排盘

帮用户排出四柱八字，推算十神格局。

## 流程

### 第一步：收集信息

直接用文字问用户（不要用 AskUserQuestion 工具）：

「请告诉我你的出生信息，用来排盘：
1. 阳历生日（如：1995年3月15日）
2. 出生时间（如：下午2点，不确定说大概即可）
3. 性别（男/女）
4. 出生城市

一次性告诉我就行，格式随意。」

等用户回复后继续。

### 第二步：计算八字

从用户回复中提取年、月、日、时（24小时制，0-23）。

用 Bash 工具找到脚本并运行排盘。执行以下命令（一条命令完成查找+运行）：

```bash
BAZI=$(find ~/.claude/plugins -name "bazi-calc.py" -path "*/shishen/*" 2>/dev/null | head -1); [ -z "$BAZI" ] && BAZI=$(find ~ -maxdepth 6 -name "bazi-calc.py" -path "*/shishen/bin/*" 2>/dev/null | head -1); [ -z "$BAZI" ] && BAZI=$(find / -maxdepth 8 -name "bazi-calc.py" -path "*/shishen/bin/*" 2>/dev/null | head -1); [ -n "$BAZI" ] && python3 "$BAZI" <年> <月> <日> <时> || echo "ERROR: 找不到 bazi-calc.py，请确认 shishen 插件已安装"
```

将 `<年> <月> <日> <时>` 替换为用户的实际数据。时间用 24 小时制（0-23）。

例如用户说"1995年3月15日下午2点"：
```bash
BAZI=$(find ~/.claude/plugins -name "bazi-calc.py" -path "*/shishen/*" 2>/dev/null | head -1); [ -z "$BAZI" ] && BAZI=$(find ~ -maxdepth 6 -name "bazi-calc.py" -path "*/shishen/bin/*" 2>/dev/null | head -1); [ -n "$BAZI" ] && python3 "$BAZI" 1995 3 15 14 || echo "ERROR: 找不到 bazi-calc.py"
```

脚本会输出 JSON 格式的结果。如果报 ERROR，提示用户检查安装：「请确认已执行 `claude plugin link <shishen目录路径>`」。

### 第三步：展示结果

解析 JSON 输出，用以下格式展示：

```
🔮 排盘完成！

┌──────────────────────────────────────┐
│  年柱：{year.stem}{year.branch}      │
│  月柱：{month.stem}{month.branch}    │
│  日柱：{day.stem}{day.branch}        │
│  时柱：{hour.stem}{hour.branch}      │
│  日主：{dayMaster}（{dayMasterPolarity}{dayMasterElement}）│
└──────────────────────────────────────┘

【十神格局】
```

对十神按 score 从高到低排序展示：
- score >= 4：`████████████ 旺` + 👑
- score >= 2：`████████ 中`
- score > 0：`████ 弱`
- score = 0：`░░░░ 缺`

每个十神后加一句有梗的短评（参考十神人格设定）。

最后用 2-3 句轻松的话概括用户的"十神人格画像"。

### 第四步：保存配置

用 Write 工具将完整 JSON 结果保存到 `.shishen/profile.json`，额外加上用户输入的原始信息：

```json
{
  "birthday": "YYYY-MM-DD",
  "birthTime": "HH:MM",
  "gender": "male/female",
  "birthCity": "城市名",
  "autoMode": false,
  "fourPillars": { ... },
  "dayMaster": "...",
  "dayMasterElement": "...",
  "dayMasterPolarity": "...",
  "tenGods": { ... }
}
```

保存完成后提示：「排盘完成！输入 /shishen:on 开启十神模式，让你的内心声音上线。🔮」
