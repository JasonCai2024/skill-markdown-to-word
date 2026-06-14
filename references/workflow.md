# MD文档转WORD的方法

## 需求说明

将Markdown格式文档（.md）转换为WORD文档（.docx），保留原始文档中的文字、表格、图片等元素。图片来源于MD文件同目录下的`attachments`文件夹，需要嵌入到WORD文档中。

## 核心方法

### Pandoc 命令行 + 预处理脚本 + 参考样式文档 + DOCX后处理（推荐）

使用 Pandoc 将 Markdown 文档转换为 WORD 格式。当前主流程适配 `WORD -> MD` 主方案生成的 Markdown，即：图片使用 Obsidian wiki 链接，表格默认是可编辑的 `pipe table`。转换前使用 Python 脚本预处理 MD 文件，将图片路径转换为 Pandoc 能识别的相对路径；如输入文档中仍存在内嵌 HTML 表格，也会尽量展开为 Pandoc 可处理的 Markdown 表格。为尽量接近目标 WORD 样式，转换时应使用 `reference.docx` 作为参考样式文档。转换完成后，仅在文档中实际存在表格时，再使用 Python 脚本补齐 WORD 表格边框等样式。

#### 处理单个文档

**第一步：运行预处理脚本**

```bash
python fix_md_for_word.py "input.md" "./attachments" "input.for_word.md"
```

预处理脚本会生成一个临时的 `input.for_word.md`，并完成以下处理：
- 将 MD 文件中的 wiki 链接格式图片转换为相对路径格式
- 保留并直接使用现有的 Markdown `pipe table`
- 如存在内嵌 HTML 表格，则尝试将其转换为 Pandoc 更容易处理的 Markdown 表格

图片转换示例：
- `![[20250919183015_1.png]]` → `attachments/20250919183015_1.png`

**第二步：Pandoc 转换**

```bash
pandoc "input.for_word.md" -o "input.docx" --standalone --resource-path=. --reference-doc="./reference.docx"

# 3. WORD 后处理：仅在文档中存在表格时再执行
python postprocess_docx.py "input.docx"
```

| 参数 | 说明 |
|------|------|
| `-o input.docx` | 输出文件路径 |
| `--standalone` | 生成完整文档（包含页眉页脚等） |
| `--resource-path=.` | 指定资源文件搜索路径为当前目录 |
| `--reference-doc=./reference.docx` | 使用参考 WORD 文档中的样式定义 |

---

## 重要：处理多个文档

**多个 MD 文档位于同一文件夹时，必须逐个处理：**

1. 每次只处理一个MD文档
2. 预处理脚本输出的是临时 `*.for_word.md` 文件，不修改原始 MD
3. Pandoc 转换时指定资源路径指向当前目录

**正确示例：**
```bash
# 处理第一个文档
python fix_md_for_word.py "doc1.md" "./attachments" "doc1.for_word.md"
pandoc "doc1.for_word.md" -o "doc1.docx" --standalone --resource-path=. --reference-doc="./reference.docx"
python postprocess_docx.py "doc1.docx"  # 仅在文档中存在表格时再执行

# 然后再处理第二个文档
python fix_md_for_word.py "doc2.md" "./attachments" "doc2.for_word.md"
pandoc "doc2.for_word.md" -o "doc2.docx" --standalone --resource-path=. --reference-doc="./reference.docx"
python postprocess_docx.py "doc2.docx"  # 仅在文档中存在表格时再执行
```

---

## 预处理脚本功能说明

`fix_md_for_word.py` 脚本实现以下功能：

### 1. 转换Wiki链接为相对路径

**原始格式（Obsidian）：**
```markdown
![[20250919183015_1.png]]
![[20250919183015_2.jpeg]]
```

**转换后格式（Pandoc）：**
```markdown
![](./attachments/20250919183015_1.png)
![](./attachments/20250919183015_2.jpeg)
```

### 2. 处理带标题的图片引用

**原始格式：**
```markdown
![[image.png|标题]]
```

**转换后格式：**
```markdown
![标题](./attachments/image.png)
```

### 3. 处理嵌入文件引用

移除非图片类型的嵌入引用（如PDF、音频等），这些在WORD中无法显示：

**原始格式：**
```markdown
![[document.pdf]]
![[audio.mp3]]
```

**转换后格式：**
```markdown
[文件: document.pdf]
[文件: audio.mp3]
```

### 4. 处理内嵌 HTML 表格

将部分内嵌 HTML 表格转换为普通 Markdown 表格，优先让 Pandoc 生成真正的 WORD 表格。

说明：
- 支持清洗 `<blockquote>`、`<p>`、`<strong>` 等常见包裹标签
- 支持展开 `rowspan`、`colspan`
- 当前实现会将合并单元格“展开”为重复内容，以优先保证 WORD 中生成表格
- 该方案追求“尽量可转”，不是严格无损还原

说明：
- 如果输入 MD 已经是普通 `pipe table`，则无需额外转换，Pandoc 会直接生成 WORD 表格

### 5. WORD 表格后处理

`postprocess_docx.py` 脚本实现以下功能：

- 仅在文档实际包含表格时执行重写，并为 Pandoc 生成的 WORD 表格补齐外边框与内部边框
- 尝试将表格样式设置为 `Table Grid`
- 统一表格垂直居中

---

## 完整处理流程

```bash
# 假设要处理 doc1.md，附件在 attachments 文件夹中

# 1. 预处理：生成临时文件，处理图片与HTML表格
python fix_md_for_word.py "doc1.md" "./attachments" "doc1.for_word.md"

# 2. Pandoc 转换
pandoc "doc1.for_word.md" -o "doc1.docx" --standalone --resource-path=. --reference-doc="./reference.docx"

# 3. WORD 后处理：仅在文档中存在表格时再执行
python postprocess_docx.py "doc1.docx"

# 4. 清理临时文件
del "doc1.for_word.md"  # 可选
```

---

## 输出说明

### 文件结构

```
folder/
├── doc1.md              # MD文档
├── doc1.for_word.md     # 预处理后的临时MD文档
├── attachments/         # 图片文件夹
│   ├── 20250919183015_1.png
│   ├── 20250919183015_2.jpeg
│   └── ...
├── reference.docx       # 样式参考文档
├── doc1.docx           # 转换后的WORD文档
└── ...
```

### 图片嵌入说明

- 使用 `--resource-path=.` 参数后，Pandoc会自动将相对路径引用的图片嵌入到WORD文档中
- 生成的DOCX文件中的图片是嵌入式的，复制到其他位置也能正常显示

---

## 注意事项

1. **必须逐个处理**：同一目录下的多个MD文档，必须一个处理完再处理下一个
2. **预处理脚本不修改原文件**：会输出单独的 `*.for_word.md`
3. **资源路径**：确保 `--resource-path=.` 参数正确，以便Pandoc能找到图片
4. **临时文件**：转换完成后可删除 `*.for_word.md`
5. **参考样式文档**：建议提供 `reference.docx`，否则 Pandoc 会使用默认 WORD 样式
6. **主流程表格格式**：当前推荐输入是 Markdown `pipe table`，便于编辑且已验证可稳定转回 WORD 表格
7. **HTML 表格限制**：预处理脚本会尽量将 HTML 表格转换为普通 Markdown 表格，但复杂表格仍可能存在降级
8. **合并单元格策略**：当前对 `rowspan`、`colspan` 的处理是“展开内容优先”，不保证在 WORD 中保留视觉合并效果
9. **表格边框**：Pandoc 生成的表格可能默认无边框，建议仅在文档实际包含表格时运行 `postprocess_docx.py` 补齐；纯文本文档不要额外重写 DOCX
10. **样式保留**：即使使用 `reference.docx`，也主要控制标题、正文、表格样式等；复杂结构不保证完全还原
11. **编码**：确保MD文件使用UTF-8编码

---

## 依赖

- [Pandoc](https://pandoc.org/)：文档转换工具
- Python 3.x：运行预处理脚本

---

## 相关脚本

- `fix_md_for_word.py`：Markdown格式预处理脚本（必须使用）
- `reference.docx`：参考样式文档（建议使用）
- `build_reference_doc.py`：根据当前约定的正文、标题、引用块和表格样式重新生成 `reference.docx`
- `postprocess_docx.py`：为生成的 WORD 表格补齐边框和基础表格样式
