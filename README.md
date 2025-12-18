# 申请项目信息静态网页

这是一个用于展示研究生申请项目信息的静态网页系统，可以挂载到GitHub Pages上查看。

## 项目结构

```
项目根目录/
├── web/                    # 前端项目目录
│   ├── index.html          # 项目列表页（主页）
│   ├── detail.html         # 项目详情页
│   ├── data/
│   │   ├── projects.json   # 项目数据（从CSV转换）
│   │   └── social-media.json # 社交媒体信息（从Markdown提取）
│   ├── css/
│   │   └── style.css       # 样式文件
│   └── js/
│       ├── main.js         # 列表页逻辑（排序、筛选）
│       └── detail.js       # 详情页逻辑
├── 申请项目信息.csv        # 原始数据文件
├── 项目社交媒体信息/       # 原始Markdown文件
├── convert_data.py         # 数据转换脚本（可选）
└── README.md               # 项目说明文档
```

## 功能特性

- **项目列表页**：展示所有申请项目的卡片列表
- **项目详情页**：显示项目的完整信息和社交媒体信息
- **排序功能**：支持按录取概率、截止日期、大学名称排序
- **响应式设计**：适配桌面端和移动端
- **现代UI设计**：简洁美观的用户界面

## 数据来源

- `申请项目信息.csv`：包含项目的基本信息（大学、项目名称、录取概率、截止日期等）
- `项目社交媒体信息/*.md`：包含各项目的社交媒体信息（小红书、知乎帖子等）

## 使用方法

### 本地开发

1. 克隆或下载项目到本地
2. 进入 `web` 目录
3. 使用本地服务器打开项目（推荐使用Python的简单HTTP服务器）：

**Windows PowerShell:**
```powershell
cd web
python -m http.server 8000
```

**或者使用Node.js的http-server:**
```powershell
cd web
npx http-server -p 8000
```

4. 在浏览器中访问 `http://localhost:8000`


### 更新数据

如果需要更新项目数据：

1. 更新 `申请项目信息.csv` 文件
2. 更新 `项目社交媒体信息/` 目录下的Markdown文件
3. 运行数据转换脚本（可选）：

```bash
python convert_data.py
```

或者手动更新 `web/data/projects.json` 和 `web/data/social-media.json` 文件。

## GitHub Pages 部署

### 方法一：通过GitHub网页界面

1. 将项目上传到GitHub仓库
2. 进入仓库的 Settings 页面
3. 找到 Pages 设置
4. 选择 Source 为 "Deploy from a branch"
5. 选择分支为 "master"（或你的主分支）
6. 选择文件夹为 "/ (root)"（重要：必须选择根目录）
7. 点击 Save
8. 等待几分钟，GitHub会生成你的网站地址：`https://你的用户名.github.io/仓库名/`

### 方法二：使用Git命令行

1. 初始化Git仓库（如果还没有）：

```bash
git init
git add .
git commit -m "Initial commit"
```

2. 在GitHub上创建新仓库

3. 添加远程仓库并推送：

```bash
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main
```

4. 在GitHub仓库设置中启用Pages（参考方法一）

## 注意事项

- 确保所有文件路径使用相对路径
- JSON文件需要是有效的JSON格式
- 如果使用GitHub Pages，确保仓库是公开的（或你有GitHub Pro账户）
- 项目ID格式为：`大学名称-项目名称`（例如：`香港中文大学-科学人工智能`）

## 浏览器支持

- Chrome（推荐）
- Firefox
- Safari
- Edge

## 技术栈

- HTML5
- CSS3（使用CSS变量和Grid布局）
- JavaScript（ES6+，使用Fetch API）
- 无框架依赖，纯原生实现

## 许可证

本项目仅供个人使用。

## 更新日志

### v1.0.0 (2024-12)
- 初始版本
- 实现项目列表和详情页
- 支持排序功能
- 响应式设计

