# MDL Blog

基于 Material Design Lite 的轻量级博客框架。无需数据库，Markdown 写作，一键部署 GitHub Pages。

## 特性

- **Material Design 1** — 严格遵循 MD1 规范，11 套配色主题
- **暗色模式** — 博客前端 + 管理后台全面支持，可跟随系统设置
- **Markdown 写作** — GFM 语法 + 代码高亮（17 种语言）
- **可视化管理** — 浏览器后台，实时预览 + 草稿保存
- **响应式布局** — 桌面 / 平板 / 手机三级适配
- **零数据库** — JSON 文件存储，Git 友好
- **一键部署** — GitHub Actions 自动发布到 Pages
- **轻量可扩展** — 核心仅 2 文件（`blog-admin.py` + `blog-admin.html`）

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装与启动

```bash
git clone https://github.com/BJY-STUDIO/bjy-studio.github.io.git
cd bjy-studio.github.io
pip install flask markdown
python blog-admin.py
```

启动后终端显示：

```
==================================================
  博客管理后台已启动
  管理界面: http://localhost:5001/admin
  博客首页: http://localhost:5001/
==================================================
```

| 页面 | 地址 |
|------|------|
| 博客首页 | http://localhost:5001/ |
| 管理后台 | http://localhost:5001/admin |

### 写第一篇文章

1. 打开 http://localhost:5001/admin
2. 点击右侧「+ 新建文章」
3. 填写标题、日期、摘要
4. 在 Markdown 编辑器中编写正文
5. 点击「预览」确认效果
6. 点击「保存并发布」

## 项目结构

```
├── blog-admin.py          # Flask 后端（文章管理 + 页面生成）
├── blog-admin.html        # 管理后台（MD1 规范 UI）
├── blog-data.json         # 博客数据（文章 + 配置 + 草稿）
├── 404.html               # 自定义错误页
├── index.html             # 首页（自动生成）
├── images/                # 站点图片
├── blog/
│   ├── covers/            # 封面图（管理员上传）
│   ├── backgrounds/       # 背景图
│   └── posts/             # 文章 HTML（自动生成）
├── lib/mdl/               # MDL 框架（11 套主题 CSS + JS）
├── file/
│   ├── css/               # 主题 CSS + Prism 高亮 + 页面样式
│   └── javascript/        # 代码复制 + 暗色模式切换
└── .github/workflows/     # GitHub Pages 自动部署
```

## 主题与暗色模式

### 11 套配色主题

管理后台 → 设置 → 主题色板，点击即切换：

| 主题 | 配色 |
|------|------|
| Grey-Orange（默认） | 灰底橙强调 |
| Blue-Grey-Red | 蓝灰底红强调 |
| Teal-Green | 青绿底绿强调 |
| Indigo-Pink | 靛蓝底粉强调 |
| Deep-Orange-Pink | 深橙底粉强调 |
| Cyan-Orange | 青底橙强调 |
| Purple-Orange | 紫底橙强调 |
| Light-Blue-Orange | 浅蓝底橙强调 |
| Blue-Light-Blue | 蓝底浅蓝强调 |
| Amber-Orange | 琥珀底橙强调 |
| Brown-Orange | 棕底橙强调 |

### 暗色模式

三种模式可选：明亮 / 黑暗 / 跟随系统。博客首页和文章页底部均有 Switch 可实时切换，设置自动持久化。

## Markdown 支持

支持 GFM 全语法：

- 标题、段落、粗体 / 斜体
- 代码块（```语言 包裹，17 种语言 Prism 高亮 + 点击复制）
- 行内代码（`code`）
- 表格、引用块、有序 / 无序列表
- 图片、链接、水平线

同时也支持直接在编辑器中写 HTML 输出。

## 部署到 GitHub Pages

1. 推送代码到 `main` 分支
2. 仓库 Settings → Pages → Source 选择 "GitHub Actions"
3. 每次推送自动部署

## 自定义

### 站点配置

管理后台 → 设置，或直接编辑 `blog-data.json` 的 `site` 对象：

```json
{
  "site": {
    "author": "Your Name",
    "title": "My Blog",
    "subtitle": "Hello World",
    "theme": "indigo-pink",
    "darkMode": "light",
    "backgroundImage": ""
  }
}
```

### 页面布局

- 首页：`blog-admin.py` → `generate_index()`
- 文章页：`blog-admin.py` → `generate_post_page()`
- 全局样式：`file/css/styles.css`
- 管理后台样式：`file/css/blog-admin.css`

## 依赖

| 包 | 用途 | 安装 |
|----|------|------|
| Flask | 本地管理后台 | `pip install flask` |
| Markdown | Markdown 转 HTML | `pip install markdown` |

前端依赖（MDL、Prism.js）已本地化，无需 npm。

## 许可证

Apache License 2.0
