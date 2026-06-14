# 更新日志

本项目的重要变更都会记录在本文件中。

本文档结构参考 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)。

## [未发布]

### 新增

- 新增一套带有 `Open Bugs` 章节的更新日志维护机制，便于后续持续维护。

### 修复

- 修复 `assets/reference.docx` 中 `Heading 1 / Heading 2 / Heading 3` 继承 Office 默认主题蓝色的问题。
- 更新 `scripts/build_reference_doc.py`，为标题与正文样式显式写入黑色字体，并清除 `w:themeColor / w:themeTint / w:themeShade` 继承，避免 Word 继续显示蓝色标题。
- 重新生成 `assets/reference.docx`，确认转换后的标题样式保持黑体（SimHei）且颜色为黑色，正文保持宋体（SimSun）。

### Open Bugs

后续 AI 助手维护规则：

1. 如果发现了可复现 Bug，先在这里追加一条问题记录。
2. 每条 Bug 记录至少包含：
   - 日期
   - 现象
   - 触发条件
   - 影响文件或模块
   - 当前状态
3. Bug 修复完成后：
   - 更新或移除 `Open Bugs` 中对应的问题项
   - 将修复结果同步写入 `未发布` 或具体发布日期下的 `修复` 章节

## [2026-06-14]

### 新增

- 首次建立更新日志。
