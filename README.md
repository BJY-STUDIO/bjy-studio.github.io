---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '0ae27a1b-961a-46c6-b0e6-f4b7656a07b6'
  PropagateID: '0ae27a1b-961a-46c6-b0e6-f4b7656a07b6'
  ReservedCode1: '7fb65945-049a-4a37-93d9-0f8771b4bba2'
  ReservedCode2: '7fb65945-049a-4a37-93d9-0f8771b4bba2'
---

# MDL Blog

基于 Google Material Design Lite (MDL) 的轻量级个人博客框架。Flask 本地管理 + Markdown 写作 + 静态页面一键部署到 GitHub Pages，零数据库，全端响应式。

---

## 目录

- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [使用教程](#使用教程)
- [API 参考](#api-参考)
- [主题系统](#主题系统)
- [暗色模式](#暗色模式)
- [内容格式](#内容格式)
- [部署指南](#部署指南)
- [自定义与二次开发](#自定义与二次开发)
- [代码架构与优化](#代码架构与优化)
- [依赖清单](#依赖清单)
- [许可证](#许可证)

---

## 功能特性

### 博客前端

| 功能 | 说明 |
|------|------|
| MD1 规范 UI | 严格遵循 Google Material Design 1 设计语言 |
| 11 套配色主题 | 管理后台一键切换，CSS 变量全局联动 |
| 暗色模式 | 明亮 / 黑暗 / 跟随系统，首页和文章页 Switch 实时切换 |
| 响应式布局 | 桌面 / 平板 / 手机自动适配 |
| 代码高亮 | Prism.js 引擎，17 种语言语法着色 + 点击复制 |
| 文章导航 | 前一篇 / 后一篇，悬停显示 tooltip |
| 置顶文章 | 首页卡片置顶，管理后台控制 |
| 引用卡片 | 名言警句格式，不生成详情页，不参与导航 |
| 自定义背景图 | 管理后台上传 / 删除，CSS `body::before` 覆盖 |

### 管理后台

| 功能 | 说明 |
|------|------|
| 文章 CRUD | 新建、编辑、删除、发布，全部浏览器内完成 |
| Markdown 编辑器 | EasyMDE 集成，侧边实时预览，Material Icons 工具栏 |
| 服务端预览 | 1:1 匹配发布页面，所见即所得 |
| 草稿系统 | 保存未完成文章，随时恢复编辑 |
| 封面图上传 | 拖拽或点击，自动存储到 `blog/covers/` |
| 头像 / Favicon 上传 | 设置页统一管理 |
| 导航菜单管理 | 自定义侧边栏链接，支持排序、启用 / 禁用 |
| MD1 组件库 | Snackbar、Dialog、Datepicker、Switch、Tooltip 均严格遵循 MD1 规范 |

---

## 快速开始

### 环境要求

- Python 3.8+
- pip
- Git

### 安装

```bash
git clone https://github.com/BJY-STUDIO/bjy-studio.github.io.git
cd bjy-studio.github.io
pip install flask markdown
```

### 启动

```bash
python blog-admin.py
```

终端输出：

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

1. 浏览器打开 **http://localhost:5001/admin**
2. 点击右侧 **「+ 新建文章」**
3. 填写标题、日期、摘要
4. 在 Markdown 编辑器中编写正文
5. 点击 **「预览」** 确认渲染效果
6. 点击 **「保存并发布」**，文章自动生成到 `blog/posts/`

---

## 项目结构

```
├── blog-admin.py              # Flask 后端（API + 页面生成，~1280 行）
├── blog-admin.html            # 管理后台 SPA（~2225 行）
├── blog-data.json             # 全部数据：文章 / 配置 / 草稿 / 导航
├── index.html                 # 博客首页（自动生成，勿手动编辑）
├── 404.html                   # 自定义 404 页（15 秒倒计时自动跳转）
│
├── blog/
│   ├── covers/                # 文章封面图（管理后台上传）
│   ├── backgrounds/           # 博客背景图
│   ├── avatars/               # 作者头像
│   ├── favicons/              # 自定义 Favicon
│   └── posts/                 # 文章详情页 HTML（自动生成，勿手动编辑）
│
├── lib/mdl/
│   ├── material.min.js        # MDL v1.3.0 运行时
│   ├── material-themes.css    # 5 套基础主题合集
│   ├── material-themes-*.css  # 5 套基础主题入口
│   └── material.*.min.css     # 5 套 MDL 原始主题文件
│
├── file/
│   ├── css/
│   │   ├── styles.css                 # 博客前端全局样式（~1620 行）
│   │   ├── blog-admin.css             # 管理后台样式（~2900 行）
│   │   ├── mdl-main.css               # MDL docs-layout 样式
│   │   ├── prism-default.css          # Prism.js 默认亮色主题
│   │   ├── material-themes-*.css      # 11 套完整主题 CSS（博客端）
│   │   ├── material.min.css           # MDL v1.3.0 完整压缩 CSS
│   │   ├── material-design-lite.css   # MDL v1.3.0 完整未压缩 CSS
│   │   ├── clock-page.css             # CSS 时钟动画（404 页用）
│   │   └── clippy-page.css            # Clippy 助手页面
│   │
│   ├── javascript/
│   │   ├── snippets.js                # 代码块点击复制 + 暗色模式 Switch
│   │   ├── prism.js                   # Prism.js 核心
│   │   ├── prism-bundle.min.js        # 17 种语言 Prism 插件合集
│   │   ├── prism-python.min.js        # 单独语言插件（按需加载）
│   │   ├── ...                        # 其余 16 个单独语言插件
│   │   ├── material.min.js            # MDL v1.3.0 JS（副本）
│   │   ├── moment.min.js              # Moment.js v2.9.0
│   │   ├── moment-timezone-*.min.js   # Moment 时区数据
│   │   ├── clippy.min.js              # ClippyJS Agent 库
│   │   └── widgets.js                 # Twitter 嵌入组件
│   │
│   ├── agents/                # ClippyJS 角色精灵资源
│   ├── images/                # 编辑器工具栏图标等
│   ├── about.html             # 关于页
│   ├── code.html              # 代码展示页
│   ├── clock.html             # CSS 动画时钟
│   ├── clippy.html            # Clippy 桌面助手
│   └── wwdc15.html            # WWDC 2015 CSS 动画
│
├── images/                    # 站点素材（logo、截图等）
│
├── .github/workflows/
│   └── static.yml             # GitHub Pages 自动部署工作流
│
├── LICENSE                    # Apache License 2.0
└── README.md                  # 本文件
```

> `blog/posts/*.html` 和 `index.html` 由 `blog-admin.py` 自动生成，每次保存文章或修改设置时重新生成。**不要手动编辑这些文件**，改动会在下次生成时被覆盖。

---

## 使用教程

### 文章管理

| 操作 | 步骤 |
|------|------|
| **新建** | 右侧面板 → 填写标题 / 日期 / 正文 → 保存并发布 |
| **编辑** | 左侧列表点击文章 → 修改内容 → 保存并发布 |
| **删除** | 列表中点击删除图标 → MD1 Dialog 确认 → Snackbar 可撤销 |
| **置顶** | 列表中点击图钉图标 → 文章在首页始终显示在首位 |
| **预览** | 编辑时点击「预览」→ 服务端渲染，1:1 匹配发布效果 |

### 封面图

1. 编辑文章时点击「封面图」区域的上传按钮
2. 选择图片文件，自动上传到 `blog/covers/`
3. 上传进度条显示传输状态（MD1 确定进度条）
4. 首页卡片和文章详情页自动展示封面图
5. 未上传封面时，卡片显示 `#37474f`（blue-grey 800）实色背景

### 草稿系统

1. 编辑文章时点击「保存草稿」
2. 草稿存储在 `blog-data.json` 的 `drafts` 数组中
3. 下次打开管理后台，草稿列表显示在文章列表下方
4. 点击草稿可恢复到编辑器继续编辑

### 导航菜单

管理后台 → 导航管理：

| 操作 | 说明 |
|------|------|
| 新增 | 点击「+ 添加链接」，填写名称和 URL |
| 编辑 | 直接修改名称 / URL 文本框 |
| 排序 | 拖拽左侧拖动手柄上下调整顺序 |
| 禁用 | 取消勾选启用复选框，菜单项保留但不显示 |
| 删除 | 点击删除图标 → 确认删除 |

### 站点设置

管理后台 → 设置：

| 设置项 | 说明 |
|--------|------|
| 作者名称 | 显示在文章页作者区域和侧边栏 |
| 博客标题 | `<title>` 标签和侧边栏 |
| 副标题 | 侧边栏卡片底部 |
| 主题 | 11 套配色色板，点击即切换 |
| 暗色模式 | 明亮 / 黑暗 / 跟随系统 |
| 博客背景图 | 上传 / 删除自定义全屏背景 |
| 头像 | 上传 / 删除作者头像 |
| Favicon | 上传 / 删除自定义 Favicon |

---

## API 参考

`blog-admin.py` 提供 26 个 API 端点，管理后台通过这些接口完成所有操作：

### 文章

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/posts` | 获取所有文章（按日期倒序） |
| POST | `/api/posts` | 创建文章 |
| PUT | `/api/posts/<id>` | 更新文章 |
| DELETE | `/api/posts/<id>` | 删除文章及其 HTML 文件 |
| PUT | `/api/posts/<id>/pin` | 切换文章置顶状态 |

### 上传

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/upload-cover` | 上传封面图到 `blog/covers/` |
| POST | `/api/upload-background` | 上传背景图（替换旧的） |
| DELETE | `/api/background` | 删除背景图 |
| POST | `/api/upload-avatar` | 上传头像 |
| DELETE | `/api/avatar` | 删除头像 |
| POST | `/api/upload-favicon` | 上传 Favicon |
| DELETE | `/api/favicon` | 删除 Favicon |

### 站点与导航

| 方法 | 路径 | 说明 |
|------|------|------|
| PUT | `/api/settings` | 更新站点设置（标题、主题、暗色模式等） |
| GET | `/api/menu-items` | 获取导航菜单项 |
| POST | `/api/menu-items` | 新增菜单项 |
| PUT | `/api/menu-items/<id>` | 更新菜单项 |
| DELETE | `/api/menu-items/<id>` | 删除菜单项 |

### 草稿与其他

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/drafts` | 获取所有草稿 |
| POST | `/api/drafts` | 保存草稿 |
| DELETE | `/api/drafts/<id>` | 删除草稿 |
| POST | `/api/preview` | 服务端渲染预览页面 |
| POST | `/api/generate` | 手动触发全站重新生成 |

---

## 主题系统

### 11 套配色方案

管理后台 → 设置 → 主题色板，点击切换：

| 主题键 | 风格 | 主色 | 强调色 |
|--------|------|------|--------|
| `grey-orange` | 灰橙（默认） | #616161 | #ff9800 |
| `blue-grey-red` | 蓝灰红 | #455a64 | #f44336 |
| `teal-green` | 青绿 | #009688 | #4caf50 |
| `indigo-pink` | 靛粉 | #3f51b5 | #e91e63 |
| `deep-orange-pink` | 深橙粉 | #ff5722 | #e91e63 |
| `red-amber` | 红琥珀 | #f44336 | #ffc107 |
| `purple-pink` | 紫粉 | #9c27b0 | #e91e63 |
| `blue-amber` | 蓝琥珀 | #1976d2 | #ffc107 |
| `deep-purple-amber` | 深紫琥珀 | #512da8 | #ffc107 |
| `cyan-orange` | 青橙 | #00bcd4 | #ff9800 |
| `light-blue-deep-orange` | 浅蓝深橙 | #03a9f4 | #ff5722 |

### CSS 变量注入

主题切换时，Python 后端通过 `theme_vars_css()` 注入 CSS 自定义属性，替代所有硬编码颜色值：

```css
:root {
    --md-primary: #616161;
    --md-accent: #ff9800;
    --md-primary-dark: #424242;
    --md-accent-dark: #f57c00;
}
```

所有 CSS 文件中的按钮悬停色、Switch 轨道色、选中状态色等均引用这些变量，实现一键换色。

---

## 暗色模式

### 三种模式

| 模式 | 行为 |
|------|------|
| 明亮 | 始终使用亮色主题 |
| 黑暗 | 始终使用暗色主题 |
| 跟随系统 | 自动检测系统偏好，实时响应系统切换 |

### 实现机制

- 通过 `<html>` 标签的 `data-mode` 属性控制（`light` / `dark` / `auto`）
- 所有暗色样式通过 `html[data-mode="dark"]` CSS 选择器覆盖
- 页脚 Switch 切换时同步调用 `PUT /api/settings` 持久化
- 博客前端和管理后台各自独立处理暗色模式

### 覆盖范围

| 组件 | 暗色适配 |
|------|----------|
| 博客首页 | 背景、卡片、文字、侧边栏、页脚 |
| 文章详情页 | 全部文本、代码块、引用块、图片边框、导航按钮 |
| 管理后台 | App Bar、卡片、表单、按钮、Dialog、Snackbar、Datepicker、下拉菜单、进度条、上传区域 |

---

## 内容格式

支持两种内容编写方式，可在编辑器中混用：

### Markdown（推荐）

```markdown
## 标题

正文段落，**粗体**，*斜体*，`行内代码`。

```python
def hello():
    print("Hello, MDL Blog!")
```
````

### HTML 直接输出

```html
<h4>自定义标题</h4>
<p>直接写 HTML，<code>完全控制</code>输出格式。</p>
<img src="../../images/screenshot.png" alt="截图" style="max-width:100%;border-radius:4px;margin:12px auto;display:block;">
```

### 代码块语法

| 语法 | 说明 |
|------|------|
| `` ```python ... ``` `` | Markdown fenced code block，推荐 |
| `[code:python]...[/code]` | 旧格式，向后兼容 |
| `[code:python\|备注]...[/code]` | 旧格式 + 自定义标签文本 |

所有代码块输出统一的 `code-with-text` 格式：灰色容器 + 语言标签 + Prism 高亮 + 点击复制按钮。

### 支持的代码语言

Prism.js 支持 17 种语言高亮：markup (HTML/XML/SVG)、CSS、JavaScript、Java、Python、C、C++、Go、Rust、SQL、Bash、YAML、JSON、Markdown、TypeScript、Docker。

---

## 部署指南

### GitHub Pages 自动部署

项目内置 GitHub Actions 工作流：

```yaml
# .github/workflows/static.yml
on:
  push:
    branches: ["main"]
```

**步骤：**

1. Fork 或 clone 本仓库
2. 推送代码到 `main` 分支
3. 仓库 Settings → Pages → Source 选择 **"GitHub Actions"**
4. 每次推送自动部署，无需手动操作

工作流无构建步骤，整个仓库根目录直接部署为静态站点。

### 自定义域名

1. 在仓库根目录创建 `CNAME` 文件，内容为你的域名
2. DNS 服务商添加 CNAME 记录指向 `<username>.github.io`
3. GitHub 仓库 Settings → Pages → Custom domain 填入域名

---

## 自定义与二次开发

### 站点配置

直接编辑 `blog-data.json`：

```json
{
  "site": {
    "author": "Your Name",
    "title": "My Blog",
    "subtitle": "Hello World",
    "theme": "grey-orange",
    "darkMode": "light",
    "backgroundImage": "",
    "avatar": "",
    "favicon": ""
  }
}
```

### 页面模板

所有页面模板内嵌在 `blog-admin.py` 中：

| 页面 | 函数 | 说明 |
|------|------|------|
| 博客首页 | `generate_index()` | 卡片流 + 侧边栏 + 置顶 + 页脚 |
| 文章详情 | `generate_post_page()` | 正文 + 代码高亮 + 导航 + 页脚 |
| 预览页面 | `api_preview()` | 与发布页 1:1 一致，独立路由 |

### 样式文件

| 文件 | 作用 | 修改原则 |
|------|------|----------|
| `file/css/styles.css` | 博客前端样式 | 自定义样式追加到文件末尾，带注释说明 |
| `file/css/blog-admin.css` | 管理后台样式 | 同上 |
| `file/css/material*.css` | MDL 官方 CSS | **不要修改**，所有 MDL 文件保持原样 |
| `file/css/prism-default.css` | Prism 主题 | 可替换为其他 Prism 主题 |

### 添加新主题

1. 生成 MDL 主题 CSS 文件（使用 [MDL Theme Designer](https://getmdl.io/customize/index.html)）
2. 分别放入 `lib/mdl/` 和 `file/css/` 目录
3. 在 `blog-admin.py` 的 `_THEME_COLORS` 字典中添加主题键和颜色值
4. 在 `blog-admin.html` 的主题色板区域添加对应的色块
5. 重新启动服务即可

---

## 代码架构与优化

### 整体架构

```
┌──────────────┐       API        ┌──────────────┐
│  浏览器前端    │ ◄──────────────► │  Flask 后端   │
│              │                  │              │
│ blog-admin   │   RESTful JSON   │ blog-admin   │
│   .html      │                  │   .py        │
│              │                  │              │
│ index.html   │  静态文件服务     │  页面生成器    │
│ posts/*.html │ ◄─────────────── │  generate_*  │
└──────────────┘                  └──────────────┘
                                         │
                                         ▼
                                  ┌──────────────┐
                                  │ blog-data    │
                                  │   .json      │
                                  └──────────────┘
```

### 数据流

1. **写入**：管理后台 → API → `blog-data.json` + 文件上传 → `generate_all()` → 重新生成 HTML
2. **读取**：浏览器 → 静态文件服务 → `index.html` / `posts/*.html`
3. **预览**：编辑器 → `POST /api/preview` → 服务端渲染 → 新窗口展示

### 代码组织（blog-admin.py）

| 区域 | 行号 | 内容 |
|------|------|------|
| 导入与配置 | 1-36 | 常量、目录路径、Flask 初始化 |
| 数据读写 | 39-60 | `load_data()` / `save_data()` + 数据迁移 |
| API 路由 | 63-605 | 26 个 REST 端点（文章、上传、设置、草稿、导航） |
| 辅助函数 | 606-655 | `fmt_datetime()`、`dark_mode_attr()`、`theme_vars_css()` 等 |
| 页面生成 | 658-1199 | `generate_all()` → `generate_index()` → `generate_post_page()` |
| Markdown | 1162-1251 | `process_code_blocks()` + `markdown_to_html()` |
| 静态服务 | 1256-1270 | 首页、管理页面、静态文件路由 |
| 启动入口 | 1274-1282 | `generate_all()` + `app.run()` |

### 性能优化

| 优化点 | 实现 |
|--------|------|
| **CDN 本地化** | 所有 MDL / Prism 资源存放在 `lib/mdl/` 和 `file/`，无外部 CDN 依赖，国内访问无阻塞 |
| **Prism 插件打包** | 17 个语言插件合并为 `prism-bundle.min.js`（34 行），一次请求加载全部语言 |
| **MDL 主题按需加载** | 每个页面只引用当前主题的 CSS 文件（~8 行），不加载全部 11 套 |
| **静态生成** | 文章保存时生成 HTML，访问时直接返回静态文件，无运行时渲染开销 |
| **图片自动管理** | 上传新头像 / 背景图时自动删除旧文件，避免磁盘冗余 |
| **孤儿文件清理** | `generate_all()` 自动删除 `blog/posts/` 中已不存在的文章 HTML |

### MD1 规范化组件

管理后台的 6 个核心组件严格遵循 [m1.material.io](https://m1.material.io/) 规范：

| 组件 | 规格要点 |
|------|----------|
| **Snackbar** | 48dp 高，288-568dp 宽，2dp 圆角；移动端全宽贴底 |
| **Dialog** | 标题 20sp Medium，内容 14sp，24dp 阴影，操作区 52dp |
| **Text Field** | 浮动标签 12sp，底部线 1dp → 2dp focus，输入 16sp |
| **Datepicker** | 7 列日期网格，月份切换滑动动画，`:not()` 解决样式冲突 |
| **Switch** | Track 36×14dp，Thumb 20dp 无边框，行程 16dp，MDL Ripple |
| **Tooltip** | 10sp Medium，Grey 700 90%，22dp 高，150ms 动画 |

---

## 依赖清单

### Python 依赖

| 包 | 用途 | 安装 |
|----|------|------|
| Flask | 本地管理后台 HTTP 服务 | `pip install flask` |
| Markdown | Markdown → HTML 转换（GFM 扩展） | `pip install markdown` |

### 前端依赖（均已本地化，无需 npm）

| 库 | 版本 | 位置 | 用途 |
|----|------|------|------|
| Material Design Lite | v1.3.0 | `lib/mdl/` | MD1 框架 |
| Prism.js | v1.x | `file/javascript/` | 代码语法高亮 |
| EasyMDE | v2.18.0 | jsDelivr CDN | Markdown 编辑器（仅管理后台） |
| Marked.js | v12.0.0 | jsDelivr CDN | 编辑器客户端预览（仅管理后台） |
| Material Icons | - | Google Fonts CDN | 图标字体 |
| Moment.js | v2.9.0 | `file/javascript/` | CSS 时钟（404 页） |
| ClippyJS | - | `file/javascript/` | 桌面助手（彩蛋页） |

---

## 许可证

Apache License 2.0