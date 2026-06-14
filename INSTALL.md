# Markdown 转 Word 技能安装说明

本技能是纯本地技能，不依赖远程 API，也不需要任何账号凭证。

## 一、前置要求

| 工具 | 版本建议 | 用途 |
| --- | --- | --- |
| Python | 3.8+ | 运行 `scripts/*.py` |
| Pandoc | 2.19+ | 执行 Markdown 转 DOCX |

本机检查命令：

```bash
python --version
pandoc --version
```

## 二、获取技能

GitHub 仓库地址：

```text
https://github.com/JasonCai2024/skill-markdown-to-word
```

克隆命令：

```bash
git clone https://github.com/JasonCai2024/skill-markdown-to-word.git
```

## 三、安装技能

### 方案 A：Claude Code 与 OpenCode 共用

把整个 `skill-markdown-to-word/` 文件夹复制到以下任一位置：

- 项目级：`<你的项目>/.claude/skills/skill-markdown-to-word/`
- 全局：`~/.claude/skills/skill-markdown-to-word/`

### 方案 B：仅给 OpenCode 使用

也可以复制到：

- `<你的项目>/.opencode/skills/skill-markdown-to-word/`
- `~/.config/opencode/skills/skill-markdown-to-word/`

但仍建议优先使用方案 A，因为 OpenCode 本身也会读取 `.claude/skills/`。

### 方案 C：可选的 Claude Code 兼容命令

如果希望更稳定地在 Claude Code 的 `/` 命令补全里看到本技能，可额外放一个命令文件到：

```text
~/.claude/commands/skill-markdown-to-word.md
```

最小内容可写为：

```markdown
---
description: 将 Markdown 文件转换为 Word .docx，并处理图片路径与表格样式。
argument-hint: [markdown-file]
---

优先使用：

`~/.claude/skills/skill-markdown-to-word/scripts/convert_markdown_to_word.py <input.md> [output.docx]`
```

## 四、安装后验证

- Claude Code：重启或新开会话，输入 `/`，检查是否能看到 `skill-markdown-to-word`
- OpenCode：重启或新开会话，检查技能列表中是否出现该技能

## 五、卸载

删除你在第三步中复制过去的技能目录即可；如果额外安装了命令文件，也一并删除：

```text
~/.claude/commands/skill-markdown-to-word.md
```
