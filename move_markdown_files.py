import os
import shutil

# 需要移动的文件映射
files_to_move = {
    "data/tobepicked/新加坡国立大学人工智能与创新理学硕士.md": "项目社交媒体信息/新加坡国立大学-人工智能与创新理学硕士.md",
    "data/tobepicked/新加坡国立大学工程设计与创新理学硕士.md": "项目社交媒体信息/新加坡国立大学-工程设计与创新理学硕士.md",
    "data/tobepicked/香港科技大学数据驱动建模理学硕士.md": "项目社交媒体信息/香港科技大学-数据驱动建模理学硕士.md",
    "data/tobepicked/南洋理工大学企业人工智能理学硕士.md": "项目社交媒体信息/南洋理工大学-企业人工智能理学硕士.md"
}

for source, dest in files_to_move.items():
    if os.path.exists(source):
        # 确保目标目录存在
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        # 复制文件
        shutil.copy2(source, dest)
        print(f"Copied: {source} -> {dest}")
        # 删除源文件
        os.remove(source)
        print(f"Removed: {source}")
    else:
        print(f"File not found: {source}")

print("Done!")

