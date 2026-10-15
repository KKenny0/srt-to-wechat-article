---
name: srt-to-wechat-article
description: "Transforms podcast or video SRT subtitle files and audio transcripts into a beautifully typeset, magazine-grade HTML reading article. Outputs 100% inline-styled HTML fully compatible with the WeChat Official Account editor (微信公众平台), complete with a one-click rich-text copy button for direct clipboard pasting. Use when the user wants to typeset SRT files, convert audio/video transcripts into WeChat articles, generate HTML articles with timestamps and quote callouts, or format podcast digests."
when_to_use: "srt to wechat, 字幕转公众号, srt排版, 播客转文章, 微信排版html, 字幕整理成文章, 类似截图排版, 微信公众平台排版"
---

# SRT to WeChat Article Typesetter (字幕转微信公众号精读文章)

将播客、访谈或视频的 `.srt` 字幕文件一键提炼并排版为现代杂志风格的精读 HTML 文章。
核心特性：
1. **SRT 自动清洗聚合**：解析时间戳，消除口语碎片、多余空行与语气词。
2. **结构化深度导读**：提炼 `/read` 风格的 `Summary` 与 `Useful Details`，按时间戳逻辑划分多级章节。
3. **100% 微信富文本兼容**：正文全部采用严格内联样式（Inline CSS），杜绝公众号编辑器吞样式、丢背景、丢边框的问题。
4. **一键复制到微信**：网页端内置专属工具条与现代剪贴板 `ClipboardItem` API，在浏览器中点击即可将高保真富文本复制到剪贴板，直接粘贴进微信后台。

---

## 核心设计规范与排版语言

参考模板文件位于：`assets/template.html`

### 1. 顶部眉栏与元数据（Header & Meta）
- **顶部分类栏**：大写无衬线，字号 11px，两端对齐，底边双实线 `border-bottom: 2px solid #1a1a1a;`。
  - 左侧：`ARTICLE —— FINAL`（或专栏分类）
  - 右侧：`野生肯尼 PAGE —— YYYY.MM.DD`
- **次级信息**：`AUTHOR 整理者 · DATE 日期 · READING 约 X 分钟`，字号 11px，浅灰字体 `#888`。
- **标签胶囊**：外框药丸设计 `border: 1px solid #dcdcdc; border-radius: 3px; padding: 2px 8px; font-size: 11px; color: #666; margin-right: 6px;`。

### 2. 标题体系（Typography）
- **主标题（H1）**：字号 28-32px，行高 1.35，字重 800，深黑 `#111111`，衬线或优质黑体。
- **副标题（Subtitle）**：字号 15-16px，行高 1.65，中灰 `#555555`，作为全文总结导读。
- **章节大标题（H2）**：中文字号带时间戳，如 `一、章节主题（00:00:24）`，字号 20-22px，字重 700，上外边距 36px，下外边距 14px。
- **章节序号上标（可选）**：如小字 `01` 置于大标题左上。

### 3. 特殊信息块（Callouts & Quotes）
- **来源元信息卡片（Source Box）**：
  - 容器：浅灰底色 `background-color: #ededed; border-radius: 4px; padding: 15px 18px; margin: 22px 0;`
  - 文字：字号 13px，行高 1.7，颜色 `#666666`。
- **金句引语卡片（Quote Callout）**：
  - 容器：`background-color: #ededed; border-left: 3px solid #b5b5b5; padding: 16px 20px; margin: 20px 0; border-radius: 0 4px 4px 0;`
  - 文字：字号 14px，行高 1.75，深灰 `#333333`。双语对照时，英文原句紧随其后附于括号中。
- **概念前置高亮（Lead Keywords）**：
  - 段落开头核心观点用加粗黑体收口，如：`<strong style="color: #111; font-weight: 700;">选择悖论。</strong>`

---

## 工作流与执行步骤

### 步骤 1：解析与聚合 SRT 输入
使用配套脚本（或内置正则逻辑）解析 `.srt` 文件：
```bash
python scripts/parse_srt.py <path_to_srt> --grouped 3
```
- 过滤音效标记（如 `[music]`、`[clears throat]`）。
- 聚合连续断句，按 2~4 分钟时间窗口分组，计算全文总时长与预估精读时间。

### 步骤 2：编辑提炼与架构化（Editorial Structuring）
1. **线索层**：提取 `/read` 核心摘要（`Summary` 3-5 点，`Useful Details` 核心概念与案例列表）。
2. **篇章层**：将全篇划分为 4-7 个具有悬念或叙事推进力的章节。
3. **语言层**：
   - 保留原声播客的核心观点与神态，转化为洗练流畅的书面语。
   - 提取主讲人与受访者的高光语录（Notable Quotes），标注原发时间点。
   - 核心洞察段落前置加粗关键词。

### 步骤 3：组装微信高兼容 HTML
读取 `assets/template.html`，将内容替换注入，确保正文区域所有标签包含**完整的内联样式**（不要依赖 class 或 `<style>` 标签在公众号中的解析）。

微信常用标签样式参考：
```html
<!-- 普通段落 -->
<p style="font-size: 15px; color: #2b2b2b; line-height: 1.85; margin: 14px 0; letter-spacing: 0.5px;">
  正文内容...
</p>

<!-- 加粗重点词 -->
<strong style="color: #111111; font-weight: 700;">关键词。</strong>

<!-- 金句引用框 -->
<blockquote style="background-color: #ededed; border-left: 3px solid #b5b5b5; padding: 16px 20px; margin: 20px 0; font-size: 14px; color: #333333; line-height: 1.75; border-radius: 0 4px 4px 0;">
  “引言内容”<br>
  <span style="color: #777; font-size: 13px;">(English quote if applicable)</span>
</blockquote>
```

### 步骤 4：保存与交互验证
1. 将产出的 HTML 文件保存至用户工作区（例如 `<project-root>/<slug>.html`）。
2. 在浏览器中打开即可看到完整版式，用户点击顶部的「一键复制到微信公众号」按钮，直接切换到微信公众号后台粘贴即可。
