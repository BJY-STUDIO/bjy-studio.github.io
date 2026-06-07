---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: 'b3b3fb01-2e55-42e4-b909-ce85c50ec504'
  PropagateID: 'b3b3fb01-2e55-42e4-b909-ce85c50ec504'
  ReservedCode1: '8d00ccd2-1de6-4062-9e1a-97669f0bba65'
  ReservedCode2: '8d00ccd2-1de6-4062-9e1a-97669f0bba65'
---

# MDL Blog

基于 Material Design Lite 的轻量级博客框架。无需数据库，Markdown 写作，一键部署 GitHub Pages。

## 特性

- **Material Design** — 遵循 MD1 规范，5 套配色主题
- **Markdown 写作** — GFM 语法 + 代码高亮（17 种语言）
- **可视化管理** — 浏览器后台，实时预览 + 草稿保存
- **零数据库** — JSON 文件存储，Git 友好
- **一键部署** — GitHub Actions 自动发布到 Pages
- **轻量可扩展** — 核心仅 2 文件（`blog-admin.py` + `blog-admin.html`）

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装

```bash
git clone https://github.com/your-username/mdl-blog.git
cd mdl-blog
pip install -r requirements.txt
python blog-admin.py
```

启动后访问：

| 页面 | 地址 |
|------|------|
| 博客首页 | http://localhost:5001/ |
| 管理后台 | http://localhost:5001/admin |

### 写第一篇文章

1. 打开 http://localhost:5001/admin
2. 在右侧编辑器中填写标题、日期、摘要
3. 用 Markdown 编写正文
4. 点击"预览"确认效果
5. 点击"保存并发布"

## 项目结构

```
mdl-blog/
├── blog-admin.py          # Flask 后端（文章管理 + 页面生成）
├── blog-admin.html        # 管理后台（MD1 规范 UI）
├── blog-data.json         # 博客数据（文章 + 配置 + 草稿）
├── styles.css             # 博客全局样式
├── 404.html               # 自定义错误页
├── requirements.txt       # Python 依赖
├── images/                # favicon、logo
├── blog/
│   ├── covers/            # 封面图（自动上传）
│   ├── backgrounds/       # 背景图
│   └── posts/             # 文章 HTML（自动生成）
├── lib/mdl/               # MDL 框架（5 套主题）
├── file/
│   ├── css/               # Prism 主题 + 页面样式
│   ├── javascript/        # 代码高亮 + 工具脚本
│   ├── about.html         # 关于页
│   └── code.html          # 代码展示页
└── .github/workflows/     # GitHub Pages 自动部署
```

## 主题切换

内置 5 套主题，位于 `lib/mdl/`：

| 文件 | 风格 |
|------|------|
| `material-themes-grey-orange.css` | 灰橙（默认） |
| `material-themes-blue-grey-red.css` | 蓝灰红 |
| `material-themes-teal-green.css` | 青绿 |
| `material-themes-indigo-pink.css` | 靛粉 |
| `material-themes-deep-orange-pink.css` | 深橙粉 |

修改 `blog-admin.py` 中 `generate_index()` 和 `generate_post_page()` 的主题引用即可切换。

## Markdown 支持

支持 GFM 全语法，包括：

- 标题、段落、粗体/斜体
- 代码块（\`\`\`语言 包裹，17 种语言高亮）
- 表格、引用块、列表
- 图片、链接、水平线

## 部署到 GitHub Pages

1. 在 GitHub 创建新仓库
2. 推送代码到 `main` 分支
3. 仓库 Settings → Pages → Source 选择 "GitHub Actions"
4. 推送后自动部署

```bash
git remote add origin https://github.com/your-username/your-repo.git
git branch -M main
git push -u origin main
```

## 自定义

### 站点配置

编辑 `blog-data.json` 的 `site` 对象：

```json
{
  "site": {
    "author": "Your Name",
    "title": "My Blog",
    "subtitle": "Hello World",
    "backgroundImage": ""
  }
}
```

### 页面布局

- 首页：`blog-admin.py` → `generate_index()`
- 文章页：`blog-admin.py` → `generate_post_page()`
- 全局样式：`styles.css`
- 管理后台：`blog-admin.html` → `<style>` 块

## 依赖

| 包 | 用途 | 安装 |
|----|------|------|
| Flask | 本地管理后台 | `pip install flask` |
| Markdown | Markdown 转 HTML | `pip install markdown` |

前端依赖通过 CDN 或本地加载，无需 npm。

## 许可证

Apache License 2.0