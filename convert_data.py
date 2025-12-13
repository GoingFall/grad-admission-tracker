#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据转换脚本：将CSV和Markdown文件转换为JSON格式
"""

import csv
import json
import os
import re
from pathlib import Path

def parse_markdown(md_file_path):
    """解析Markdown文件，提取结构化数据"""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取项目基本信息
    basic_info = {}
    basic_match = re.search(r'## 项目基本信息\n(.*?)\n##', content, re.DOTALL)
    if basic_match:
        basic_text = basic_match.group(1)
        for line in basic_text.split('\n'):
            if line.strip() and line.startswith('-'):
                if '英文名称' in line:
                    basic_info['english_name'] = line.split('：')[-1].strip()
                elif '录取概率' in line:
                    basic_info['admission_rate'] = line.split('：')[-1].strip()
                elif '重要日期' in line:
                    basic_info['important_date'] = line.split('：')[-1].strip()
    
    # 提取小红书搜索结果
    xiaohongshu_posts = []
    xhs_section = re.search(r'## 小红书搜索结果\n(.*?)\n## 知乎搜索结果', content, re.DOTALL)
    if xhs_section:
        xhs_content = xhs_section.group(1)
        # 匹配帖子
        post_pattern = r'### 帖子(\d+)：(.*?)\n- 发布时间：(.*?)\n- 作者：(.*?)\n- 点赞数：(.*?)\n- 链接：(.*?)(?=\n\n###|$)'
        posts = re.findall(post_pattern, xhs_content, re.DOTALL)
        for post in posts:
            xiaohongshu_posts.append({
                'title': post[1].strip(),
                'publish_date': post[2].strip(),
                'author': post[3].strip(),
                'likes': post[4].strip(),
                'url': post[5].strip()
            })
    
    # 提取知乎搜索结果
    zhihu_posts = []
    zhihu_section = re.search(r'## 知乎搜索结果\n(.*?)\n## 关键信息总结', content, re.DOTALL)
    if zhihu_section:
        zhihu_content = zhihu_section.group(1)
        # 匹配帖子
        post_pattern = r'### 帖子(\d+)：(.*?)\n- 发布时间：(.*?)\n- 点赞数：(.*?)\n- 回答数：(.*?)\n- 链接：(.*?)\n- 内容摘要：(.*?)(?=\n\n###|$)'
        posts = re.findall(post_pattern, zhihu_content, re.DOTALL)
        for post in posts:
            zhihu_posts.append({
                'title': post[1].strip(),
                'publish_date': post[2].strip(),
                'likes': post[3].strip(),
                'answers': post[4].strip(),
                'url': post[5].strip(),
                'summary': post[6].strip()
            })
    
    # 提取关键信息总结
    summary_section = re.search(r'## 关键信息总结\n(.*?)$', content, re.DOTALL)
    summary = {}
    if summary_section:
        summary_text = summary_section.group(1)
        # 提取各个部分
        sections = re.findall(r'### (.*?)\n(.*?)(?=\n### |$)', summary_text, re.DOTALL)
        for section_title, section_content in sections:
            summary[section_title] = section_content.strip()
    
    return {
        'basic_info': basic_info,
        'xiaohongshu_posts': xiaohongshu_posts,
        'zhihu_posts': zhihu_posts,
        'summary': summary
    }

def generate_project_id(university, project_name):
    """生成项目ID"""
    # 使用大学名称和项目名称生成唯一ID
    return f"{university}-{project_name}"

def convert_csv_to_json(csv_path):
    """将CSV文件转换为JSON"""
    projects = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            project_id = generate_project_id(row['大学名称'], row['项目名称'])
            project = {
                'id': project_id,
                'university': row['大学名称'],
                'project_name': row['项目名称'],
                'english_name': row['项目英文名称'],
                'admission_rate': row['录取概率'],
                'important_date': row['重要日期'],
                'description': row['详细描述'],
                'url': row['项目URL'],
                'ielts_requirement': row['IELTS要求'],
                'deadline': row['申请截止日期'],
                'requirements': row['申请要求'],
                'tuition': row['学费信息'],
                'duration': row['项目时长']
            }
            projects.append(project)
    
    return projects

def convert_markdowns_to_json(md_dir):
    """将Markdown文件转换为JSON"""
    social_media_data = {}
    
    md_files = Path(md_dir).glob('*.md')
    for md_file in md_files:
        # 从文件名提取大学和项目名称
        filename = md_file.stem  # 去掉.md扩展名
        parts = filename.split('-', 1)
        if len(parts) == 2:
            university = parts[0]
            project_name = parts[1]
            project_id = generate_project_id(university, project_name)
            
            # 解析Markdown文件
            md_data = parse_markdown(md_file)
            social_media_data[project_id] = md_data
    
    return social_media_data

def main():
    """主函数"""
    # 文件路径
    csv_path = '申请项目信息.csv'
    md_dir = '项目社交媒体信息'
    output_dir = 'data'
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 转换CSV
    print("正在转换CSV文件...")
    projects = convert_csv_to_json(csv_path)
    with open(os.path.join(output_dir, 'projects.json'), 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)
    print(f"已生成 {len(projects)} 个项目数据")
    
    # 转换Markdown
    print("正在转换Markdown文件...")
    social_media = convert_markdowns_to_json(md_dir)
    with open(os.path.join(output_dir, 'social-media.json'), 'w', encoding='utf-8') as f:
        json.dump(social_media, f, ensure_ascii=False, indent=2)
    print(f"已生成 {len(social_media)} 个社交媒体数据")
    
    print("数据转换完成！")

if __name__ == '__main__':
    main()

