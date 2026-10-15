# SRT to WeChat Article Typesetter

> 将播客、访谈或视频的 `.srt` 字幕/逐字稿文件一键提炼并排版为现代杂志风格的精读 HTML 文章，正文采用全内联样式，完美兼容微信公众平台富文本编辑器，并支持浏览器端一键复制到微信公众号。

---

## 🌟 核心特性

- **SRT 自动清洗聚合**：解析时间戳，去除口语停顿、噪声与语气词，按逻辑聚合长段落。
- **结构化深度导读**：提炼 Summary 核心线索与 Useful Details，按时间戳逻辑划分多级章节。
- **100% 微信富文本兼容**：正文全部使用高兼容内联样式（Inline CSS），杜绝公众号后台编辑器过滤 `<style>` 标签导致背景色和边框丢失的问题。
- **一键复制到微信公众号**：网页端内置专属工具栏与现代 `ClipboardItem({'text/html': ...})` 富文本剪贴板 API。点击后直接在微信公众号编辑器按 `Ctrl + V` 粘贴，样式 1:1 高保真还原。

---

## 📁 目录结构

```
srt-to-wechat-article/
├── SKILL.md                 # Antigravity / Claude Agent Skill 规则与主说明文档
├── README.md                # 项目主页与说明
├── assets/
│   └── template.html        # 微信高兼容内联 HTML 模版与剪贴板脚本
└── scripts/
    └── parse_srt.py         # SRT 解析与时间戳聚合 Python 脚本
```

---

## 🚀 快速上手

### 1. 命令行解析 SRT
```bash
python scripts/parse_srt.py <path_to_srt_file> --grouped 3
```

### 2. 作为 Agent Skill 使用
在支持 Agent Skills 的环境（如 Antigravity / Claude Code）中引入该 Skill 后，直接输入：
> “帮我把这个 SRT 排版成微信公众号文章” 或 “用 srt-to-wechat-article 排版这个字幕”

---

## 📝 微信排版视觉语言

- **顶部分类眉栏**：`ARTICLE —— FINAL` ｜ `野生肯尼 PAGE —— YYYY.MM.DD`
- **次级信息**：作者整理署名、发布日期、预估精读时长
- **标签胶囊**：外框药丸设计（Tags）
- **大标题与导语**：大字号衬线/无衬线高对比度标题，浅灰导语背景
- **章节时间戳标题**：带播放进度的分段小标（如 `一、……（00:00:24）`）
- **金句卡片**：浅灰底色（`#ededed`）+ 左侧细边框（`#b5b5b5`）+ 双语对照
- **观点加粗前置**：段首核心词黑体收口
