#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将待选择项目CSV文件转换为JSON格式
"""

import csv
import json
import os
from pathlib import Path

def generate_project_id(university, project_name):
    """生成项目ID"""
    return f"{university}-{project_name}"

def convert_csv_to_json(csv_path):
    """将CSV文件转换为JSON"""
    projects = []
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
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
                'duration': row['项目时长'],
                'status': 'tobepicked'  # 标记为待选择项目
            }
            projects.append(project)
    
    return projects

def main():
    """主函数"""
    csv_path = '待选择项目信息.csv'
    output_dir = 'data'
    web_output_dir = 'web/data'
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(web_output_dir, exist_ok=True)
    
    # 转换CSV
    print("正在转换CSV文件...")
    projects = convert_csv_to_json(csv_path)
    
    # 输出到data目录
    output_file = os.path.join(output_dir, 'tobepicked-projects.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)
    print(f"已生成: {output_file}")
    
    # 输出到web/data目录
    web_output_file = os.path.join(web_output_dir, 'tobepicked-projects.json')
    with open(web_output_file, 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)
    print(f"已生成: {web_output_file}")
    
    print(f"共 {len(projects)} 个项目")

if __name__ == '__main__':
    main()

