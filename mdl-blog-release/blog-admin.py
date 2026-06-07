#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
博客管理后端服务
启动方式: python blog-admin.py
管理界面: http://localhost:5001/admin
"""

import json
import os
import re
import uuid
import shutil
import markdown
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory, send_file

# ============================================================
# 配置
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'blog-data.json')
BLOG_DIR = os.path.join(BASE_DIR, 'blog')
POSTS_DIR = os.path.join(BLOG_DIR, 'posts')
COVERS_DIR = os.path.join(BLOG_DIR, 'covers')
BACKGROUNDS_DIR = os.path.join(BLOG_DIR, 'backgrounds')
AVATARS_DIR = os.path.join(BLOG_DIR, 'avatars')
FAVICONS_DIR = os.path.join(BLOG_DIR, 'favicons')
PORT = 5001

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(COVERS_DIR, exist_ok=True)
os.makedirs(BACKGROUNDS_DIR, exist_ok=True)
os.makedirs(AVATARS_DIR, exist_ok=True)
os.makedirs(FAVICONS_DIR, exist_ok=True)

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')

# ============================================================
# 数据读写
# ============================================================
def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============================================================
# API: 文章 CRUD
# ============================================================
@app.route('/api/posts', methods=['GET'])
def api_list_posts():
    """获取所有文章列表，按日期倒序"""
    data = load_data()
    posts = sorted(data['posts'], key=lambda p: p['date'], reverse=True)
    pinned_id = data.get('pinnedPostId', '')
    return jsonify({'posts': posts, 'pinnedPostId': pinned_id, 'site': data['site']})

@app.route('/api/posts', methods=['POST'])
def api_create_post():
    """新建文章"""
    data = load_data()
    body = request.json

    post_id = body.get('id') or body.get('title', '').lower().strip()
    post_id = re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '-', post_id).strip('-')
    if not post_id:
        post_id = str(uuid.uuid4())[:8]
    existing_ids = [p['id'] for p in data['posts']]
    if post_id in existing_ids:
        post_id = f"{post_id}-{str(uuid.uuid4())[:4]}"

    post = {
        'id': post_id,
        'title': body.get('title', '无标题'),
        'date': body.get('date', datetime.now().strftime('%Y-%m-%d')),
        'summary': body.get('summary', ''),
        'content': body.get('content', ''),
        'cardFormat': body.get('cardFormat', 'standard'),
        'coverImage': body.get('coverImage', ''),
    }
    data['posts'].append(post)
    save_data(data)
    generate_all()
    return jsonify({'ok': True, 'post': post})

@app.route('/api/posts/<post_id>', methods=['PUT'])
def api_update_post(post_id):
    """更新文章"""
    data = load_data()
    body = request.json
    for post in data['posts']:
        if post['id'] == post_id:
            post['title'] = body.get('title', post['title'])
            post['date'] = body.get('date', post['date'])
            post['summary'] = body.get('summary', post['summary'])
            post['content'] = body.get('content', post['content'])
            post['cardFormat'] = body.get('cardFormat', post.get('cardFormat', 'standard'))
            post['coverImage'] = body.get('coverImage', post.get('coverImage', ''))
            save_data(data)
            generate_all()
            return jsonify({'ok': True, 'post': post})
    return jsonify({'ok': False, 'error': '文章未找到'}), 404

@app.route('/api/posts/<post_id>', methods=['DELETE'])
def api_delete_post(post_id):
    """删除文章"""
    data = load_data()
    data['posts'] = [p for p in data['posts'] if p['id'] != post_id]
    if data.get('pinnedPostId') == post_id:
        data['pinnedPostId'] = ''
    save_data(data)
    # 删除对应的文章页面文件
    post_file = os.path.join(POSTS_DIR, f"{post_id}.html")
    if os.path.exists(post_file):
        os.remove(post_file)
    generate_all()
    return jsonify({'ok': True})

@app.route('/api/posts/<post_id>/pin', methods=['PUT'])
def api_pin_post(post_id):
    """设置/取消置顶文章"""
    data = load_data()
    if data.get('pinnedPostId') == post_id:
        data['pinnedPostId'] = ''
    else:
        data['pinnedPostId'] = post_id
    save_data(data)
    generate_all()
    return jsonify({'ok': True, 'pinnedPostId': data['pinnedPostId']})

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """手动触发生成"""
    generate_all()
    return jsonify({'ok': True})

# ============================================================
# API: 封面图片上传
# ============================================================
@app.route('/api/upload-cover', methods=['POST'])
def api_upload_cover():
    """上传封面图片，保存到 blog/covers/ 目录"""
    if 'file' not in request.files:
        return jsonify({'ok': False, 'error': '未找到文件'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'ok': False, 'error': '未选择文件'}), 400

    # 生成安全文件名
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
        return jsonify({'ok': False, 'error': '不支持的图片格式'}), 400

    filename = f"{uuid.uuid4().hex[:12]}{ext}"
    save_path = os.path.join(COVERS_DIR, filename)
    f.save(save_path)

    # 返回相对于 MDL 根目录的路径
    rel_path = f"blog/covers/{filename}"
    return jsonify({'ok': True, 'path': rel_path})

# ============================================================
# API: 背景图片上传
# ============================================================
@app.route('/api/upload-background', methods=['POST'])
def api_upload_background():
    """上传背景图片，保存到 blog/backgrounds/ 目录"""
    if 'file' not in request.files:
        return jsonify({'ok': False, 'error': '未找到文件'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'ok': False, 'error': '未选择文件'}), 400

    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.webp'):
        return jsonify({'ok': False, 'error': '不支持的图片格式'}), 400

    filename = f"{uuid.uuid4().hex[:12]}{ext}"
    save_path = os.path.join(BACKGROUNDS_DIR, filename)
    f.save(save_path)

    rel_path = f"blog/backgrounds/{filename}"

    # 更新 blog-data.json 中的 backgroundImage
    data = load_data()
    old_bg = data['site'].get('backgroundImage', '')
    data['site']['backgroundImage'] = rel_path
    save_data(data)
    generate_all()

    # 删除旧背景图文件
    if old_bg:
        old_path = os.path.join(BASE_DIR, old_bg)
        if os.path.exists(old_path) and old_path != os.path.join(BASE_DIR, rel_path):
            os.remove(old_path)

    return jsonify({'ok': True, 'path': rel_path})

@app.route('/api/background', methods=['DELETE'])
def api_delete_background():
    """删除背景图片"""
    data = load_data()
    old_bg = data['site'].get('backgroundImage', '')
    if old_bg:
        old_path = os.path.join(BASE_DIR, old_bg)
        if os.path.exists(old_path):
            os.remove(old_path)
    data['site']['backgroundImage'] = ''
    save_data(data)
    generate_all()
    return jsonify({'ok': True})

# ============================================================
# API: 头像上传
# ============================================================
@app.route('/api/upload-avatar', methods=['POST'])
def api_upload_avatar():
    """上传头像图片，保存到 blog/avatars/ 目录"""
    if 'file' not in request.files:
        return jsonify({'ok': False, 'error': '未找到文件'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'ok': False, 'error': '未选择文件'}), 400

    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.ico', '.svg'):
        return jsonify({'ok': False, 'error': '不支持的图片格式'}), 400

    filename = f"{uuid.uuid4().hex[:12]}{ext}"
    save_path = os.path.join(AVATARS_DIR, filename)
    f.save(save_path)

    rel_path = f"blog/avatars/{filename}"

    # 更新 blog-data.json 中的 avatar
    data = load_data()
    old_avatar = data['site'].get('avatar', '')
    data['site']['avatar'] = rel_path
    save_data(data)
    generate_all()

    # 删除旧头像文件
    if old_avatar:
        old_path = os.path.join(BASE_DIR, old_avatar)
        if os.path.exists(old_path) and old_path != os.path.join(BASE_DIR, rel_path):
            os.remove(old_path)

    return jsonify({'ok': True, 'path': rel_path})

@app.route('/api/avatar', methods=['DELETE'])
def api_delete_avatar():
    """删除头像图片，恢复默认"""
    data = load_data()
    old_avatar = data['site'].get('avatar', '')
    if old_avatar:
        old_path = os.path.join(BASE_DIR, old_avatar)
        if os.path.exists(old_path):
            os.remove(old_path)
    data['site']['avatar'] = ''
    save_data(data)
    generate_all()
    return jsonify({'ok': True})

# ============================================================
# API: Favicon 上传
# ============================================================
@app.route('/api/upload-favicon', methods=['POST'])
def api_upload_favicon():
    """上传 favicon 图片，保存到 blog/favicons/ 目录"""
    if 'file' not in request.files:
        return jsonify({'ok': False, 'error': '未找到文件'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'ok': False, 'error': '未选择文件'}), 400

    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ('.png', '.ico', '.jpg', '.jpeg', '.gif', '.webp', '.svg'):
        return jsonify({'ok': False, 'error': '不支持的图标格式'}), 400

    filename = f"{uuid.uuid4().hex[:12]}{ext}"
    save_path = os.path.join(FAVICONS_DIR, filename)
    f.save(save_path)

    rel_path = f"blog/favicons/{filename}"

    # 更新 blog-data.json 中的 favicon
    data = load_data()
    old_favicon = data['site'].get('favicon', '')
    data['site']['favicon'] = rel_path
    save_data(data)
    generate_all()

    # 删除旧 favicon 文件
    if old_favicon:
        old_path = os.path.join(BASE_DIR, old_favicon)
        if os.path.exists(old_path) and old_path != os.path.join(BASE_DIR, rel_path):
            os.remove(old_path)

    return jsonify({'ok': True, 'path': rel_path})

@app.route('/api/favicon', methods=['DELETE'])
def api_delete_favicon():
    """删除自定义 favicon，恢复默认"""
    data = load_data()
    old_favicon = data['site'].get('favicon', '')
    if old_favicon:
        old_path = os.path.join(BASE_DIR, old_favicon)
        if os.path.exists(old_path):
            os.remove(old_path)
    data['site']['favicon'] = ''
    save_data(data)
    generate_all()
    return jsonify({'ok': True})

# ============================================================
# API: 站点设置
# ============================================================
@app.route('/api/settings', methods=['PUT'])
def api_update_settings():
    """更新站点设置（author, title, subtitle）"""
    data = load_data()
    body = request.json
    if 'author' in body:
        data['site']['author'] = body['author'].strip()
    if 'title' in body:
        data['site']['title'] = body['title'].strip()
    if 'subtitle' in body:
        data['site']['subtitle'] = body['subtitle'].strip()
    save_data(data)
    generate_all()
    return jsonify({'ok': True, 'site': data['site']})

# ============================================================
# API: 菜单项管理
# ============================================================
@app.route('/api/menu-items', methods=['GET'])
def api_list_menu_items():
    """获取所有菜单项"""
    data = load_data()
    items = data.get('site', {}).get('menuItems', [])
    return jsonify({'menuItems': items})

@app.route('/api/menu-items', methods=['POST'])
def api_create_menu_item():
    """新增菜单项"""
    data = load_data()
    body = request.json
    if 'menuItems' not in data['site']:
        data['site']['menuItems'] = []
    item = {
        'id': str(uuid.uuid4())[:8],
        'name': body.get('name', '新菜单项').strip(),
        'url': body.get('url', '').strip(),
        'enabled': True,
    }
    data['site']['menuItems'].append(item)
    save_data(data)
    generate_all()
    return jsonify({'ok': True, 'item': item})

@app.route('/api/menu-items/<item_id>', methods=['PUT'])
def api_update_menu_item(item_id):
    """更新菜单项（名称、URL、启用状态、排序）"""
    data = load_data()
    items = data.get('site', {}).get('menuItems', [])
    for item in items:
        if item['id'] == item_id:
            body = request.json
            if 'name' in body:
                item['name'] = body['name'].strip()
            if 'url' in body:
                item['url'] = body['url'].strip()
            if 'enabled' in body:
                item['enabled'] = bool(body['enabled'])
            if 'order' in body:
                # order 是目标索引，执行移动
                old_idx = items.index(item)
                new_idx = int(body['order'])
                if 0 <= new_idx < len(items):
                    items.pop(old_idx)
                    items.insert(new_idx, item)
            save_data(data)
            generate_all()
            return jsonify({'ok': True, 'item': item})
    return jsonify({'ok': False, 'error': '菜单项不存在'}), 404

@app.route('/api/menu-items/<item_id>', methods=['DELETE'])
def api_delete_menu_item(item_id):
    """删除菜单项"""
    data = load_data()
    items = data.get('site', {}).get('menuItems', [])
    new_items = [i for i in items if i['id'] != item_id]
    if len(new_items) == len(items):
        return jsonify({'ok': False, 'error': '菜单项不存在'}), 404
    data['site']['menuItems'] = new_items
    save_data(data)
    generate_all()
    return jsonify({'ok': True})

# ============================================================
# API: 草稿管理
# ============================================================
@app.route('/api/drafts', methods=['GET'])
def api_list_drafts():
    """获取所有草稿"""
    data = load_data()
    drafts = data.get('drafts', [])
    return jsonify({'drafts': drafts})

@app.route('/api/drafts', methods=['POST'])
def api_save_draft():
    """保存草稿"""
    data = load_data()
    body = request.json
    if 'drafts' not in data:
        data['drafts'] = []

    draft = {
        'id': body.get('id') or str(uuid.uuid4())[:8],
        'title': body.get('title', ''),
        'date': body.get('date', datetime.now().strftime('%Y-%m-%d')),
        'summary': body.get('summary', ''),
        'content': body.get('content', ''),
        'cardFormat': body.get('cardFormat', 'standard'),
        'coverImage': body.get('coverImage', ''),
        'savedAt': datetime.now().isoformat(),
    }
    data['drafts'].append(draft)
    save_data(data)
    return jsonify({'ok': True, 'draft': draft})

@app.route('/api/drafts/<draft_id>', methods=['DELETE'])
def api_delete_draft(draft_id):
    """删除草稿"""
    data = load_data()
    data['drafts'] = [d for d in data.get('drafts', []) if d['id'] != draft_id]
    save_data(data)
    return jsonify({'ok': True})

# ============================================================
# API: 预览文章（服务端渲染，1:1 匹配实际发布页面）
# ============================================================
@app.route('/api/preview', methods=['POST'])
def api_preview():
    """服务端渲染文章预览，与实际发布页面完全一致"""
    # 支持 JSON 和 form-data 两种方式
    if request.is_json:
        body = request.json
    else:
        body = request.form.to_dict()
    
    preview_post = {
        'id': 'preview',
        'title': body.get('title', '无标题'),
        'date': body.get('date', datetime.now().strftime('%Y-%m-%d')),
        'summary': body.get('summary', ''),
        'content': body.get('content', ''),
        'cardFormat': body.get('cardFormat', 'standard'),
        'coverImage': body.get('coverImage', ''),
    }
    data = load_data()
    site = data['site']
    bg_image = site.get('backgroundImage', '')

    # 使用与 generate_post_page 相同的模板（不需要导航）
    content = preview_post['content']
    content = process_code_blocks(content)
    content = markdown_to_html(content)

    media_style = ''
    cover_img = preview_post.get('coverImage', '')
    if cover_img:
        # 预览页面 URL 为 /api/preview，使用绝对路径确保资源正确加载
        cover_img_abs = f'/{cover_img}' if not cover_img.startswith('/') else cover_img
        media_style = f' style="background-image: url(\'{cover_img_abs}\')"'

    post_bg_override = ''
    if bg_image:
        # 使用绝对路径
        bg_abs = f'/{bg_image}' if not bg_image.startswith('/') else bg_image
        post_bg_override = f"""body::before {{ background-image: url('{bg_abs}') !important; }}"""

    # 动态头像和 favicon
    avatar_src = site.get('avatar') or '/images/logo.png'
    preview_minilogo_style = f" style=\"background-image: url('{avatar_src}')\"" if site.get('avatar') else ''
    favicon_href = site.get('favicon') or '/images/favicon.png'
    if not favicon_href.startswith('/'):
        favicon_href = f'/{favicon_href}'

    html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="预览">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
    <title>预览 - {preview_post['title']}</title>
    <meta name="mobile-web-app-capable" content="yes">
    <link rel="icon" sizes="192x192" href="{favicon_href}">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="Material Design Lite">
    <link rel="apple-touch-icon-precomposed" href="{favicon_href}">
    <link rel="shortcut icon" href="{favicon_href}">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:regular,bold,italic,thin,light,bolditalic,black,medium&amp;lang=en">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link rel="stylesheet" href="/lib/mdl/material-themes-grey-orange.css">
    <link rel="stylesheet" href="/styles.css">
    <link rel="stylesheet" href="/file/css/prism-default.css">
    <link rel="stylesheet" href="/file/css/mdl-main.css">
    <style>
    #view-source {{
      position: fixed;
      display: block;
      right: 0;
      bottom: 0;
      margin-right: 40px;
      margin-bottom: 40px;
      z-index: 900;
    }}
    {post_bg_override}
    </style>
  </head>
  <body class="started">
    <div class="blog blog--article mdl-layout mdl-js-layout has-drawer is-upgraded">
      <main class="mdl-layout__content">
        <div class="back-btn">
          <a class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon mdl-color-text--white" href="javascript:history.back()" title="go back" role="button">
            <i class="material-icons" role="presentation">arrow_back</i>
          </a>
        </div>
        <div class="blog__posts mdl-grid">
          <div class="mdl-card mdl-shadow--4dp mdl-cell mdl-cell--12-col">
            <div class="mdl-card__media mdl-color-text--grey-50"{media_style}>
              <h3>{preview_post['title']}</h3>
            </div>
            <div class="mdl-color-text--grey-700 mdl-card__supporting-text meta">
              <div class="minilogo"{preview_minilogo_style}></div>
              <div>
                <strong>{site['author']}</strong>
                <span>{preview_post['date']}</span>
              </div>
              <div class="section-spacer"></div>
              <div>
                <i class="material-icons" role="presentation">bookmark</i>
                <span class="visuallyhidden">bookmark</span>
              </div>
              <div>
                <i class="material-icons" role="presentation">share</i>
                <span class="visuallyhidden">share</span>
              </div>
            </div>
            <div class="mdl-color-text--grey-700 mdl-card__supporting-text docs-layout">
              {content}
            </div>
          </div>
        </div>
        <footer class="mdl-mini-footer">
          <div class="mdl-mini-footer--left-section">
            <button class="mdl-mini-footer--social-btn social-btn social-btn__twitter">
              <span class="visuallyhidden">Twitter</span>
            </button>
            <button class="mdl-mini-footer--social-btn social-btn social-btn__blogger">
              <span class="visuallyhidden">Facebook</span>
            </button>
            <button class="mdl-mini-footer--social-btn social-btn social-btn__gplus">
              <span class="visuallyhidden">Google Plus</span>
            </button>
          </div>
          <div class="mdl-mini-footer--right-section">
            <button class="mdl-mini-footer--social-btn social-btn__share">
              <i class="material-icons" role="presentation">share</i>
              <span class="visuallyhidden">share</span>
            </button>
          </div>
        </footer>
      </main>
      <div class="mdl-layout__obfuscator"></div>
    </div>
    <script src="/lib/mdl/material.min.js"></script>
    <script src="/file/javascript/snippets.js"></script>
    <!-- Prism 代码高亮（含17种语言） -->
    <script src="/file/javascript/prism-bundle.min.js"></script>
  </body>
</html>'''
    return html


# ============================================================
# HTML 生成
# ============================================================
def generate_all():
    """生成 index.html 和所有文章详情页"""
    data = load_data()
    posts = sorted(data['posts'], key=lambda p: p['date'], reverse=True)
    pinned_id = data.get('pinnedPostId', '')
    site = data['site']
    bg_image = site.get('backgroundImage', '')

    # 迁移旧 posts/ 目录下的文件到 blog/posts/
    migrate_old_posts()

    generate_index(posts, pinned_id, site, bg_image)
    # 只为 standard 格式文章生成详情页，quote 格式不需要单独页面
    nav_posts = [p for p in posts if p.get('cardFormat', 'standard') != 'quote']
    for i, post in enumerate(nav_posts):
        if post.get('cardFormat', 'standard') != 'quote':
            generate_post_page(post, site, nav_posts, i, bg_image)
    # 清理已删除或 quote 格式文章的遗留文件
    existing_ids = {p['id'] for p in posts if p.get('cardFormat', 'standard') != 'quote'}
    for fname in os.listdir(POSTS_DIR):
        if fname.endswith('.html'):
            post_id = fname[:-5]
            if post_id not in existing_ids:
                os.remove(os.path.join(POSTS_DIR, fname))
    print(f"[生成完成] 首页 + {len(nav_posts)} 篇文章页面")

def migrate_old_posts():
    """将旧的 posts/ 目录下的文件迁移到 blog/posts/"""
    old_dir = os.path.join(BASE_DIR, 'posts')
    if os.path.exists(old_dir):
        for fname in os.listdir(old_dir):
            src = os.path.join(old_dir, fname)
            dst = os.path.join(POSTS_DIR, fname)
            if os.path.isfile(src) and not os.path.exists(dst):
                shutil.move(src, dst)
        # 旧目录如果为空则删除
        if not os.listdir(old_dir):
            os.rmdir(old_dir)

def build_card_media_style(post):
    """构建封面卡片的 inline style
    - 有封面图: background-image（会覆盖 primary-dark 背景色）
    - 无封面图: 仅返回空字符串，依赖模板中的 mdl-color--primary-dark 类
    """
    cover_img = post.get('coverImage', '')
    if cover_img:
        return f' style="background-image: url(\'{cover_img}\')"'
    return ''

def build_post_media_style(post):
    """文章详情页封面 inline style
    - 有封面图: background-image（路径多一级 ../，会覆盖 primary-dark 背景色）
    - 无封面图: 仅返回空字符串，依赖模板中的 mdl-color--primary-dark 类
    """
    cover_img = post.get('coverImage', '')
    if cover_img:
        img_path = f"../../{cover_img}"
        return f' style="background-image: url(\'{img_path}\')"'
    return ''

def generate_index(posts, pinned_id, site, bg_image=''):
    """生成首页 index.html"""
    # --- 构建动态背景图 CSS ---
    bg_override = ''
    if bg_image:
        bg_override = f"""body::before {{ background-image: url('{bg_image}') !important; }}"""

    pinned_post = None
    other_posts = []
    for p in posts:
        if p['id'] == pinned_id:
            pinned_post = p
        else:
            other_posts.append(p)

    # --- 动态头像和 favicon ---
    avatar_src = site.get('avatar') or 'images/logo.png'
    minilogo_style = f" style=\"background-image: url('{avatar_src}')\"" if site.get('avatar') else ''
    favicon_href = site.get('favicon') or 'images/favicon.png'
    touch_icon_href = favicon_href  # favicon 同时用作 touch icon

    # --- 构建置顶卡片 ---
    pinned_card = ''
    if pinned_post:
        media_style = build_card_media_style(pinned_post)
        pinned_card = f'''          <div class="mdl-card card-article mdl-cell mdl-cell--8-col">
            <div class="mdl-card__media mdl-color-text--grey-50"{media_style}>
              <h3><a href="blog/posts/{pinned_post['id']}.html">{pinned_post['title']}</a></h3>
            </div>
            <div class="mdl-card__supporting-text meta mdl-color-text--grey-600">
              <div class="minilogo"{minilogo_style}></div>
              <div>
                <strong>{site['author']}</strong>
                <span>{pinned_post['date']}</span>
              </div>
            </div>
          </div>'''

    # --- 构建侧栏个人信息卡片 ---
    # --- 构建动态菜单 ---
    menu_items = site.get('menuItems', [])
    menu_li_html = ''
    for mi in menu_items:
        if not mi.get('enabled', True):
            continue
        name = mi.get('name', '')
        url = mi.get('url', '').strip()
        if url:
            menu_li_html += f'<li><a href="{url}" class="mdl-menu__item">{name}</a></li>\n'
        else:
            menu_li_html += f'<li class="mdl-menu__item">{name}</li>\n'
    # 无启用的菜单项时隐藏菜单按钮
    menu_btn_html = ''
    if menu_li_html.strip():
        menu_btn_html = f'''<button id="menubtn" class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon">
                <i class="material-icons" role="presentation">more_vert</i>
                <span class="visuallyhidden">show menu</span>
              </button>'''

    sidebar_card = f'''          <div class="mdl-card sidebar-card mdl-cell mdl-cell--8-col mdl-cell--4-col-desktop">
            <a href="./file/clippy.html">
            <button class="mdl-button mdl-js-ripple-effect mdl-js-button mdl-button--fab mdl-color--accent">
                <i class="material-icons mdl-color-text--white" role="presentation">add</i>
              <span class="visuallyhidden">add</span>
            </button>
            </a>
            <div class="mdl-card__media mdl-color--white mdl-color-text--grey-600">
              <img src="{avatar_src}">
              {site['subtitle']}
            </div>
            <div class="mdl-card__supporting-text meta meta--fill mdl-color-text--grey-600">
              <div>
                <strong>{site['author']}</strong>
              </div>
              <ul class="mdl-menu mdl-js-menu mdl-menu--bottom-right mdl-js-ripple-effect" for="menubtn">
                {menu_li_html}
              </ul>
              {menu_btn_html}
            </div>
          </div>'''

    # --- 构建文章卡片列表 ---
    article_cards = ''
    for post in other_posts:
        card_format = post.get('cardFormat', 'standard')

        if card_format == 'quote':
            # quote 卡片使用 card-quote + mdl-card__title + h3.quote（无链接，不需要详情页）
            article_cards += f'''          <div class="mdl-card card-quote mdl-cell mdl-cell--12-col">
            <div class="mdl-card__title mdl-color-text--grey-50">
              <h3 class="quote">{post['title']}</h3>
            </div>
            <div class="mdl-card__supporting-text mdl-color-text--grey-600">
              {post['summary']}
            </div>
            <div class="mdl-card__supporting-text meta mdl-color-text--grey-600">
              <div class="minilogo"{minilogo_style}></div>
              <div>
                <strong>{site['author']}</strong>
                <span>{post['date']}</span>
              </div>
            </div>
          </div>
'''
        else:
            # standard 卡片使用 card-article + mdl-card__media
            media_style = build_card_media_style(post)
            article_cards += f'''          <div class="mdl-card card-article mdl-cell mdl-cell--12-col">
            <div class="mdl-card__media mdl-color-text--grey-50"{media_style}>
              <h3><a href="blog/posts/{post['id']}.html">{post['title']}</a></h3>
            </div>
            <div class="mdl-color-text--grey-600 mdl-card__supporting-text">
              {post['summary']}
            </div>
            <div class="mdl-card__supporting-text meta mdl-color-text--grey-600">
              <div class="minilogo"{minilogo_style}></div>
              <div>
                <strong>{site['author']}</strong>
                <span>{post['date']}</span>
              </div>
            </div>
          </div>
'''

    # --- 组装完整 index.html ---
    html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="A front-end template that helps you build fast, modern mobile web apps.">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
    <title>{site['title']} - 使用 Material Design Lite 搭建</title>
    <meta name="mobile-web-app-capable" content="yes">
    <link rel="icon" sizes="192x192" href="{touch_icon_href}">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="Material Design Lite">
    <link rel="apple-touch-icon-precomposed" href="{touch_icon_href}">
    <meta name="msapplication-TileImage" content="{touch_icon_href}">
    <meta name="msapplication-TileColor" content="#3372DF">
    <link rel="shortcut icon" href="{favicon_href}">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:regular,bold,italic,thin,light,bolditalic,black,medium&amp;lang=en">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="lib/mdl/material-themes-grey-orange.css">
    <link rel="stylesheet" href="styles.css">
    <style>
    #view-source {{
      position: fixed;
      display: block;
      right: 0;
      bottom: 0;
      margin-right: 40px;
      margin-bottom: 40px;
      z-index: 900;
    }}
    .mdl-menu__item a {{
      display: block;
      width: 100%;
      height: 100%;
      text-decoration: none;
    }}
    .mdl-menu__item a:hover {{
      background-color: #f0f0f0;
    }}
    .mdl-menu__item a[disabled] {{
      color: #aaa;
      pointer-events: none;
    }}
    {bg_override}
    </style>
    <script>
      document.addEventListener('DOMContentLoaded', function() {{
        var menuTheme1 = document.getElementById('menu-theme-1');
        var menuTheme2 = document.getElementById('menu-theme-2');
        var menuTheme3 = document.getElementById('menu-theme-3');
        menuTheme1.addEventListener('click', function() {{
          setThemeColor('lib/mdl/material-themes-grey-orange.css');
        }});
        menuTheme2.addEventListener('click', function() {{
          setThemeColor('lib/mdl/material-themes-blue-grey-red.css');
        }});
        menuTheme3.addEventListener('click', function() {{
          setThemeColor('lib/mdl/material-themes-teal-green.css');
        }});
      }});
      function setThemeColor(themeUrl) {{
        var themeLink = document.querySelector('link[href^="lib/mdl/material-themes"]');
        if (themeLink) {{
          themeLink.href = themeUrl;
        }}
      }}
    </script>
  </head>
  <body>
    <div class="blog mdl-layout mdl-js-layout has-drawer is-upgraded">
      <main class="mdl-layout__content">
        <div class="theme">
          <button id="menu-button" class="mdl-button mdl-js-button mdl-button--icon">
            <i class="material-icons" role="presentation">palette</i>
          </button>
          <ul class="mdl-menu mdl-menu--bottom-left mdl-js-menu mdl-js-ripple-effect" for="menu-button">
            <li id="menu-theme-1" class="mdl-menu__item">Grey - Orange</li>
            <li id="menu-theme-2" class="mdl-menu__item">Blue Grey - Red</li>
            <li id="menu-theme-3" class="mdl-menu__item">Teal - Green</li>
          </ul>
          <div class="mdl-tooltip mdl-tooltip--right" for="menu-button">
            更改主题配色
          </div>
        </div>
        <div id="theme-snackbar-container" class="mdl-js-snackbar mdl-snackbar">
          <div class="mdl-snackbar__text"></div>
          <button class="mdl-snackbar__action" type="button"></button>
        </div>
        <script>
          (function() {{
            'use strict';
            var snackbarContainer = document.querySelector('#theme-snackbar-container');
            var menuItems = document.querySelectorAll('.mdl-menu__item');
            menuItems.forEach(function(menuItem) {{
              menuItem.addEventListener('click', function() {{
                var theme = this.innerText;
                var data = {{
                  message: '选择了 ' + theme + ' 主题',
                  timeout: 2000,
                }};
                snackbarContainer.MaterialSnackbar.showSnackbar(data);
              }});
            }});
          }})();
        </script>
        <div class="blog__posts mdl-grid">
{pinned_card}
{sidebar_card}
{article_cards}          <nav class="article-nav mdl-cell mdl-cell--12-col">
            <div class="section-spacer"></div>
          </nav>
        </div>
        <footer class="mdl-mini-footer">
          <div class="mdl-mini-footer--left-section">
            <button class="mdl-mini-footer--social-btn social-btn social-btn__twitter">
              <span class="visuallyhidden">Twitter</span>
            </button>
            <button class="mdl-mini-footer--social-btn social-btn social-btn__blogger">
              <span class="visuallyhidden">Facebook</span>
            </button>
            <button class="mdl-mini-footer--social-btn social-btn social-btn__gplus">
              <span class="visuallyhidden">Google</span>
            </button>
          </div>
          <div class="mdl-mini-footer--right-section">
            <button class="mdl-mini-footer--social-btn social-btn__share">
              <i class="material-icons" role="presentation">share</i>
              <span class="visuallyhidden">share</span>
            </button>
          </div>
        </footer>
      </main>
      <div class="mdl-layout__obfuscator"></div>
    </div>
    <script src="lib/mdl/material.min.js"></script>
  </body>
  <script>
    Array.prototype.forEach.call(document.querySelectorAll('.mdl-card__media'), function(el) {{
      var link = el.querySelector('a');
      if(!link) {{
        return;
      }}
      var target = link.getAttribute('href');
      if(!target) {{
        return;
      }}
      el.addEventListener('click', function() {{
        location.href = target;
      }});
    }});
  </script>
</html>'''

    index_path = os.path.join(BASE_DIR, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)


def generate_post_page(post, site, all_posts, post_index, bg_image=''):
    """生成单篇文章详情页

    Args:
        post: 当前文章数据
        site: 站点配置
        all_posts: 按日期倒序排列的所有文章列表
        post_index: 当前文章在 all_posts 中的索引
        bg_image: 自定义背景图路径（可选）
    """
    # 处理内容中的代码块标记（向后兼容 [code:lang]...[/code]）
    content = post['content']
    content = process_code_blocks(content)
    # Markdown → HTML（支持 fenced code blocks, tables 等）
    content = markdown_to_html(content)

    # 获取封面 inline style（如果上传了自定义封面图）
    media_style = build_post_media_style(post)

    # --- 构建动态背景图 CSS ---
    post_bg_override = ''
    if bg_image:
        # 文章详情页在 blog/posts/ 下，路径多两级 ../
        post_bg = f"../../{bg_image}"
        post_bg_override = f"""body::before {{ background-image: url('{post_bg}') !important; }}"""

    # --- 动态头像和 favicon ---
    avatar_src = site.get('avatar') or '../../images/logo.png'
    post_minilogo_style = f" style=\"background-image: url('{avatar_src}')\"" if site.get('avatar') else ''
    post_favicon_href = site.get('favicon') or '../../images/favicon.png'
    if post_favicon_href and not post_favicon_href.startswith('http') and not post_favicon_href.startswith('../../'):
        post_favicon_href = f"../../{post_favicon_href}"
    post_touch_icon_href = post_favicon_href

    # --- 构建底部导航 ---
    # all_posts 按日期倒序: [newest, ..., current, ..., oldest]
    # ← (左/arrow_back) = 较新文章; → (右/arrow_forward) = 较旧文章
    # 最新文章(post_index==0): 左侧"返回首页"
    # 最旧文章(post_index==len-1): 右侧"返回首页"
    # hover tooltip 显示相邻文章标题 + 日期

    if post_index == 0:
        # 最新文章：左侧返回首页
        newer_link = '../../index.html'
        newer_text = '返回首页'
        newer_title = '返回博客首页'
    else:
        newer_post = all_posts[post_index - 1]
        newer_link = f"{newer_post['id']}.html"
        newer_text = '前一篇'
        newer_title = f"{newer_post['title']} ({newer_post['date']})"

    older_html = ''
    if post_index < len(all_posts) - 1:
        older_post = all_posts[post_index + 1]
        older_link = f"{older_post['id']}.html"
        older_title = f"{older_post['title']} ({older_post['date']})"
        older_html = f'''            <a href="{older_link}" class="article-nav__btn" title="{older_title}">
              后一篇
              <button class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon mdl-color--white mdl-color-text--grey-900" role="presentation">
                <i class="material-icons">arrow_forward</i>
              </button>
            </a>'''
    else:
        # 最旧文章：右侧返回首页
        older_html = f'''            <a href="../../index.html" class="article-nav__btn" title="返回博客首页">
              返回首页
              <button class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon mdl-color--white mdl-color-text--grey-900" role="presentation">
                <i class="material-icons">arrow_forward</i>
              </button>
            </a>'''

    nav_html = f'''          <nav class="article-nav mdl-color-text--grey-50 mdl-cell mdl-cell--12-col">
            <a href="{newer_link}" class="article-nav__btn" title="{newer_title}">
              <button class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon mdl-color--white mdl-color-text--grey-900" role="presentation">
                <i class="material-icons">arrow_back</i>
              </button>
              {newer_text}
            </a>
            <div class="section-spacer"></div>
{older_html}          </nav>'''

    html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="description" content="{post['title']}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0">
    <title>{site['title']} - {post['title']}</title>
    <meta name="mobile-web-app-capable" content="yes">
    <link rel="icon" sizes="192x192" href="{post_touch_icon_href}">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="Material Design Lite">
    <link rel="apple-touch-icon-precomposed" href="{post_touch_icon_href}">
    <link rel="shortcut icon" href="{post_favicon_href}">
    <link href='//fonts.googleapis.com/css?family=Roboto:regular,bold,italic,thin,light,bolditalic,black,medium&amp;lang=en' rel='stylesheet' type='text/css'>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link rel="stylesheet" href="../../lib/mdl/material-themes-grey-orange.css">
    <link rel="stylesheet" href="../../styles.css">
    <link rel="stylesheet" href="../../file/css/prism-default.css">
    <link rel="stylesheet" href="../../file/css/mdl-main.css">
    <style>
    #view-source {{
      position: fixed;
      display: block;
      right: 0;
      bottom: 0;
      margin-right: 40px;
      margin-bottom: 40px;
      z-index: 900;
    }}
    {post_bg_override}
    </style>
  </head>
  <body class="started">
    <div class="blog blog--article mdl-layout mdl-js-layout has-drawer is-upgraded">
      <main class="mdl-layout__content">
        <div class="back-btn">
          <a class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon mdl-color-text--white" href="javascript:history.back()" title="go back" role="button">
            <i class="material-icons" role="presentation">arrow_back</i>
          </a>
        </div>
        <div class="blog__posts mdl-grid">
          <div class="mdl-card mdl-shadow--4dp mdl-cell mdl-cell--12-col">
            <div class="mdl-card__media mdl-color-text--grey-50"{media_style}>
              <h3>{post['title']}</h3>
            </div>
            <div class="mdl-color-text--grey-700 mdl-card__supporting-text meta">
              <div class="minilogo"{post_minilogo_style}></div>
              <div>
                <strong>{site['author']}</strong>
                <span>{post['date']}</span>
              </div>
              <div class="section-spacer"></div>
              <div>
                <i class="material-icons" role="presentation">bookmark</i>
                <span class="visuallyhidden">bookmark</span>
              </div>
              <div>
                <i class="material-icons" role="presentation">share</i>
                <span class="visuallyhidden">share</span>
              </div>
            </div>
            <div class="mdl-color-text--grey-700 mdl-card__supporting-text docs-layout">
              {content}
            </div>
            <div class="mdl-color-text--primary-contrast mdl-card__supporting-text comments">
              <div class="comment mdl-color-text--grey-700"></div>
            </div>
          </div>
{nav_html}
        </div>
        <footer class="mdl-mini-footer">
          <div class="mdl-mini-footer--left-section">
            <button class="mdl-mini-footer--social-btn social-btn social-btn__twitter">
              <span class="visuallyhidden">Twitter</span>
            </button>
            <button class="mdl-mini-footer--social-btn social-btn social-btn__blogger">
              <span class="visuallyhidden">Facebook</span>
            </button>
            <button class="mdl-mini-footer--social-btn social-btn social-btn__gplus">
              <span class="visuallyhidden">Google Plus</span>
            </button>
          </div>
          <div class="mdl-mini-footer--right-section">
            <button class="mdl-mini-footer--social-btn social-btn__share">
              <i class="material-icons" role="presentation">share</i>
              <span class="visuallyhidden">share</span>
            </button>
          </div>
        </footer>
      </main>
      <div class="mdl-layout__obfuscator"></div>
    </div>
    <script src="../../lib/mdl/material.min.js"></script>
    <script src="../../file/javascript/snippets.js"></script>
    <!-- Prism 代码高亮（含17种语言） -->
    <script src="../../file/javascript/prism-bundle.min.js"></script>
  </body>
</html>'''

    post_path = os.path.join(POSTS_DIR, f"{post['id']}.html")
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(html)


def process_code_blocks(content):
    """
    将 [code:语言]...[/code] 或 [code:语言|备注]...[/code] 标记转换为
    code-with-text 格式的 HTML 代码块（灰色容器 + 语言标题 + Prism 高亮 + click-to-copy）
    注意：此函数保持向后兼容，新内容应使用 Markdown fenced code blocks
    """
    def replace_code_block(match):
        lang_spec = match.group(1)
        code = match.group(2)
        code_escaped = (code
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))
        # 解析 "语言|备注" 格式
        if '|' in lang_spec:
            lang, label = lang_spec.split('|', 1)
        else:
            lang = lang_spec
            label = lang_spec
        # 映射语言名到 Prism class
        lang_map = {
            'html': 'markup', 'xml': 'markup', 'svg': 'markup',
            'js': 'javascript', 'jsx': 'javascript',
            'py': 'python',
            'sh': 'bash', 'shell': 'bash',
            'yml': 'yaml',
            'md': 'markdown',
            'ts': 'typescript',
            'dockerfile': 'docker',
        }
        prism_lang = lang_map.get(lang.lower(), lang.lower())
        return f'''<div class="code-with-text">{label}
<pre class="language-{prism_lang}"><code class="language-{prism_lang}">{code_escaped}</code></pre>
</div>'''

    pattern = r'\[code:([a-zA-Z0-9+#|\u4e00-\u9fff\s]+)\]\s*([\s\S]*?)\s*\[/code\]'
    return re.sub(pattern, replace_code_block, content)


def markdown_to_html(content):
    """
    将 Markdown 内容转换为 HTML
    - 保留已有 HTML 标签（markdown 库默认行为）
    - 支持 fenced code blocks（```语言）
    - 支持 tables, nl2br 等扩展
    - fenced code blocks 输出 Prism 兼容的 code-with-text 格式
    """
    # 自定义 fenced code block 处理器，输出与 process_code_blocks 相同的 code-with-text 格式
    class CodeWithTextExtension(markdown.Extension):
        def extendMarkdown(self, md):
            # 替换默认的 fenced_code 扩展
            md.preprocessors.deregister('fenced_code_block')
            md.parser.blockprocessors.deregister('fenced_code_block')

    # 先用自定义扩展处理 fenced code blocks
    # 用正则预提取 fenced code blocks 并替换为 code-with-text HTML
    def replace_fenced_code(match):
        lang = match.group(1) or ''
        code = match.group(2)
        code_escaped = (code
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))
        lang_map = {
            'html': 'markup', 'xml': 'markup', 'svg': 'markup',
            'js': 'javascript', 'jsx': 'javascript',
            'py': 'python',
            'sh': 'bash', 'shell': 'bash',
            'yml': 'yaml',
            'md': 'markdown',
            'ts': 'typescript',
            'dockerfile': 'docker',
        }
        prism_lang = lang_map.get(lang.lower(), lang.lower()) if lang else 'markup'
        label = lang if lang else 'code'
        return f'''<div class="code-with-text">{label}
<pre class="language-{prism_lang}"><code class="language-{prism_lang}">{code_escaped}</code></pre>
</div>'''

    # 先处理 fenced code blocks（```lang\n...\n```），替换为 code-with-text HTML
    fenced_pattern = r'```(\w*)\r?\n([\s\S]*?)\r?\n```'
    content = re.sub(fenced_pattern, replace_fenced_code, content)

    # 用 markdown 库处理其余内容（标题、列表、链接、图片等）
    md = markdown.Markdown(extensions=['tables', 'nl2br'], output_format='html5')
    result = md.convert(content)
    return result


# ============================================================
# 管理后台页面路由
# ============================================================
@app.route('/admin')
@app.route('/admin/')
def admin_page():
    return send_file(os.path.join(BASE_DIR, 'blog-admin.html'))

# 静态文件服务（博客根目录）
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(BASE_DIR, filename)

@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')


# ============================================================
# 启动
# ============================================================
if __name__ == '__main__':
    generate_all()
    print(f"\n{'='*50}")
    print(f"  博客管理后台已启动")
    print(f"  管理界面: http://localhost:{PORT}/admin")
    print(f"  博客首页: http://localhost:{PORT}/")
    print(f"{'='*50}\n")
    app.run(host='0.0.0.0', port=PORT, debug=True)
