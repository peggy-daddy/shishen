---
name: fix
description: 修正命盘 — 直接调整某个十神的力量值，不用手动编辑 JSON
---

# 修正命盘

让用户方便地修正十神力量值，无需手动编辑 profile.json。

## 流程

1. 读取 `.shishen/profile.json`。如果不存在，回复：「你还没排盘呢。先 /shishen:setup」

2. 先展示当前的十神分布：

```
当前十神格局：
比肩(0·缺) 劫财(0·缺) 食神(1·弱) 伤官(2·中) 偏财(0·缺)
正财(3·旺) 七杀(1·弱) 正官(0·缺) 偏印(0·缺) 正印(1·弱)
```

3. 直接用文字问用户（不要用 AskUserQuestion 工具）：

「请告诉我要修正哪个十神的力量值。

格式：十神名=数值
例如：七杀=3  或  正印=0  或  食神=2

可以一次修正多个，用空格隔开：
例如：七杀=3 正印=0 食神=2」

等用户回复后继续。

4. 根据用户输入，更新 profile.json 中对应十神的 count 和 level：
   - 0 = 缺
   - 1 = 弱
   - 2 = 中
   - 3+ = 旺

5. 展示修正后的分布，并确认保存。

## 十神名称映射

支持中文名和拼音名：
| 中文 | 拼音 | JSON key |
|------|------|----------|
| 比肩 | bijian | bijian |
| 劫财 | jiecai | jiecai |
| 食神 | shishen | shishen |
| 伤官 | shangguan | shangguan |
| 偏财 | piancai | piancai |
| 正财 | zhengcai | zhengcai |
| 七杀 | qisha | qisha |
| 正官 | zhengguan | zhengguan |
| 偏印 | pianyin | pianyin |
| 正印 | zhengyin | zhengyin |

## 确认格式

```
✅ 已修正：
  七杀：弱(1) → 旺(3)
  正印：弱(1) → 缺(0)

你的内心声音阵容已更新。七杀要变强了，做好准备。
```
