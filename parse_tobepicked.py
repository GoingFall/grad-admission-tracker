#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析待选择项目的Markdown文件并生成CSV
"""

import csv
import re
from pathlib import Path

def parse_markdown_file(md_file_path):
    """解析单个Markdown文件，提取项目信息"""
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 从文件名提取项目名称作为备选
    filename = Path(md_file_path).stem
    filename_parts = filename.split('-', 1)
    filename_project_name = filename_parts[1] if len(filename_parts) > 1 else None
    
    # 提取大学名称（第一行，去掉QS排名）
    university_match = re.search(r'^(.+?)\s*\(QS:', content, re.MULTILINE)
    if not university_match:
        # 如果没有QS排名，直接取第一行
        first_line = content.split('\n')[0].strip()
        university = first_line
    else:
        university = university_match.group(1).strip()
    
    # 从文件名提取大学名称作为备选（更可靠）
    if filename_parts and len(filename_parts) > 0:
        filename_university = filename_parts[0]
        # 如果文件名中的大学名称更简洁，使用它
        if len(filename_university) < len(university) and filename_university in university:
            university = filename_university
    
    # 提取项目名称和英文名称
    # 优先从文件名提取项目名称
    project_name = filename_project_name if filename_project_name else "待查询"
    english_name = "待查询"
    
    # 尝试从内容中提取英文名称
    # 先尝试格式：项目名称 - 英文名称（香港科技大学格式）
    dash_match = re.search(r'^(.+?)\s*-\s*(.+?)$', content, re.MULTILINE)
    if dash_match:
        potential_name = dash_match.group(1).strip()
        potential_english = dash_match.group(2).strip()
        # 检查是否是合理的项目名称（不包含URL、学院等）
        if not any(x in potential_name for x in ['http', 'www', '学院', 'QS', '.edu', '.sg', '.hk']) and len(potential_name) > 3:
            project_name = potential_name
        if not any(x in potential_english for x in ['http', 'www', '.edu', '.sg', '.hk']) and len(potential_english) > 3:
            english_name = potential_english
    
    # 尝试格式：项目名称 | 英文名称
    if english_name == "待查询" or project_name == "待查询":
        pipe_match = re.search(r'^(.+?)\s*\|\s*(.+?)$', content, re.MULTILINE)
        if pipe_match:
            potential_name = pipe_match.group(1).strip()
            potential_english = pipe_match.group(2).strip()
            # 检查是否是合理的项目名称
            if project_name == "待查询" and not any(x in potential_name for x in ['http', 'www', '学院', 'QS', '.edu', '.sg', '.hk']) and len(potential_name) > 3:
                project_name = potential_name
            if english_name == "待查询" and not any(x in potential_english for x in ['http', 'www', '.edu', '.sg', '.hk']) and len(potential_english) > 3:
                english_name = potential_english
    
    # 提取URL
    url_match = re.search(r'https?://[^\s\n]+', content)
    url = url_match.group(0) if url_match else "待查询"
    
    # 提取学费
    tuition_match = re.search(r'学费\s*\n\s*\n\s*([^\n]+)', content)
    if tuition_match:
        tuition = tuition_match.group(1).strip()
        # 清理学费，移除IELTS信息
        tuition = re.sub(r'雅思.*?$', '', tuition, flags=re.MULTILINE).strip()
        if not tuition or len(tuition) < 3:
            tuition = "待查询"
    else:
        tuition = "待查询"
    
    # 提取IELTS要求
    ielts_match = re.search(r'雅思\s*\n\s*\n\s*([^\n]+)', content)
    if ielts_match:
        ielts_raw = ielts_match.group(1).strip()
        # 清理IELTS值，只保留数字部分
        ielts_clean = re.search(r'(\d+(?:\.\d+)?(?:/\d+)?)', ielts_raw)
        if ielts_clean:
            ielts = f"雅思: {ielts_clean.group(1)}"
        elif ielts_raw and ielts_raw != '雅思' and not any(x in ielts_raw for x in ['$', 'HK$', 'S$', '学制', '学费']):
            ielts = f"雅思: {ielts_raw}"
        else:
            ielts = ""
    else:
        ielts = ""
    
    # 提取申请截止日期
    deadline_patterns = [
        r'申请截止[：:]\s*([^\n]+)',
        r'申请时间\s*\n\s*\n\s*([^\n]+)',
        r'申请截止[：:]\s*Round\s*1[：:]\s*([^\n]+)',
    ]
    deadline = "待查询"
    for pattern in deadline_patterns:
        match = re.search(pattern, content)
        if match:
            deadline = match.group(1).strip()
            break
    
    # 提取申请要求
    requirements_match = re.search(r'申请要求\s*\n(.*?)(?=\n课程设置|\n$)', content, re.DOTALL)
    if requirements_match:
        requirements = requirements_match.group(1).strip()
        # 清理多余的空行和格式
        requirements = re.sub(r'\n+', ' ', requirements)
        requirements = re.sub(r'\s+', ' ', requirements)
    else:
        requirements = "待查询"
    
    # 提取项目时长
    duration_match = re.search(r'学制[：:]\s*([^\n]+)', content)
    if duration_match:
        duration = duration_match.group(1).strip()
    else:
        # 尝试从学费行提取
        if '学制' in tuition:
            duration_match = re.search(r'学制[：:]\s*([^\n]+)', tuition)
            if duration_match:
                duration = duration_match.group(1).strip()
            else:
                duration = "待查询"
        else:
            duration = "待查询"
    
    # 提取专业介绍作为详细描述
    description_match = re.search(r'专业介绍\s*\n(.*?)(?=\n申请要求|\n$)', content, re.DOTALL)
    if description_match:
        description = description_match.group(1).strip()
        description = re.sub(r'\n+', ' ', description)
        description = re.sub(r'\s+', ' ', description)
    else:
        description = "待查询"
    
    return {
        'university': university,
        'project_name': project_name,
        'english_name': english_name,
        'admission_rate': '待查询',
        'important_date': '待查询',
        'description': description,
        'url': url,
        'ielts': ielts,
        'deadline': deadline,
        'requirements': requirements,
        'tuition': tuition,
        'duration': duration
    }

def main():
    """主函数"""
    tobepicked_dir = Path('data/tobepicked')
    output_csv = '待选择项目信息.csv'
    
    # CSV表头
    headers = [
        '大学名称', '项目名称', '项目英文名称', '录取概率', '重要日期', 
        '详细描述', '项目URL', 'IELTS要求', '申请截止日期', 
        '申请要求', '学费信息', '项目时长'
    ]
    
    projects = []
    
    # 遍历所有Markdown文件
    md_files = sorted(tobepicked_dir.glob('*.md'))
    print(f"找到 {len(md_files)} 个Markdown文件")
    
    for md_file in md_files:
        print(f"正在解析: {md_file.name}")
        try:
            project_data = parse_markdown_file(md_file)
            projects.append(project_data)
            print(f"  成功: {project_data['university']} - {project_data['project_name']}")
        except Exception as e:
            print(f"  解析失败: {e}")
    
    # 写入CSV文件
    with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for project in projects:
            writer.writerow({
                '大学名称': project['university'],
                '项目名称': project['project_name'],
                '项目英文名称': project['english_name'],
                '录取概率': project['admission_rate'],
                '重要日期': project['important_date'],
                '详细描述': project['description'],
                '项目URL': project['url'],
                'IELTS要求': project['ielts'],
                '申请截止日期': project['deadline'],
                '申请要求': project['requirements'],
                '学费信息': project['tuition'],
                '项目时长': project['duration']
            })
    
    print(f"\n已生成CSV文件: {output_csv}")
    print(f"共 {len(projects)} 个项目")

if __name__ == '__main__':
    main()

