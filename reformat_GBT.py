import re

def generate_bib(citations, output_file="output.bib"):
    """
    将 GB/T 7714-2015 格式的引文列表转换为 BibTeX 格式并写入 .bib 文件。
    
    参数:
        citations (list): GB/T 7714-2015 格式的引文字符串列表
        output_file (str): 输出 .bib 文件的路径，默认为 "output.bib"
    """
    bib_entries = []
    
    for i, citation in enumerate(citations, start=1):
        if "[J]" in citation:
            # 解析期刊文章 [J]
            pattern = r"^(?:(.*?)\.\s*)?(.*?)\s*\[J\]\.\s*(.*?),\s*(\d{4}),\s*(?:(\d+)\s*)?\((\d+)\):\s*(\d+-\d+)\.\s*(DOI:.*?)?$"
            match = re.match(pattern, citation)
            if match:
                author = match.group(1)  # 作者，可选
                title = match.group(2)   # 标题
                journal = match.group(3) # 期刊名
                year = match.group(4)    # 年份
                volume = match.group(5)  # 卷，可选
                number = match.group(6)  # 期
                pages = match.group(7)   # 页码
                doi = match.group(8)     # DOI，可选
                
                # 生成 BibTeX 条目
                entry = f"@article{{citation{i},\n"
                if author:
                    entry += f"  author = {{{author}}},\n"
                entry += f"  title = {{{title}}},\n"
                entry += f"  journal = {{{journal}}},\n"
                entry += f"  year = {{{year}}},\n"
                if volume:
                    entry += f"  volume = {{{volume}}},\n"
                entry += f"  number = {{{number}}},\n"
                entry += f"  pages = {{{pages}}},\n"
                if doi:
                    entry += f"  doi = {{{doi[5:]}}},\n"  # 移除 "DOI:" 前缀
                entry += "}"
                bib_entries.append(entry)
            else:
                print(f"解析期刊文章失败: {citation}")
                
        elif "[D]" in citation:
            # 解析学位论文 [D]，支持可选的 DOI 和更灵活的格式
            pattern = r"^(.*?)\.\s*(.*?)\s*\[D\]\.\s*(.*?),\s*(\d{4})\s*\.?\s*(DOI:.*)?$"
            match = re.match(pattern, citation)
            if match:
                author = match.group(1).strip()  # 作者
                title = match.group(2).strip()   # 标题
                school = match.group(3).strip()  # 学校
                year = match.group(4).strip()    # 年份
                doi = match.group(5).strip() if match.group(5) else None  # DOI，可选
                
                # 生成 BibTeX 条目
                entry = f"@phdthesis{{citation{i},\n"
                entry += f"  author = {{{author}}},\n"
                entry += f"  title = {{{title}}},\n"
                entry += f"  school = {{{school}}},\n"
                entry += f"  year = {{{year}}},\n"
                if doi:
                    entry += f"  doi = {{{doi[5:]}}},\n"  # 移除 "DOI:" 前缀
                entry += "}"
                bib_entries.append(entry)
            else:
                print(f"解析带 [D] 的学位论文失败: {citation}")
                
        else:
            # 解析无类型标识的引文（假定为学位论文）
            pattern = r"^(.*?),\s*(.*?)\.\s*(.*?),\s*(.*?),\s*(\d{4})-\d{2}-\d{2}\.$"
            match = re.match(pattern, citation)
            if match:
                author = match.group(1)    # 作者
                title = match.group(2)     # 标题
                location = match.group(3)  # 地点
                school = match.group(4)    # 学校
                year = match.group(5)      # 年份（从日期中提取）
                
                # 合并学校和地点
                school_full = f"{school}, {location}"
                
                # 生成 BibTeX 条目
                entry = f"@phdthesis{{citation{i},\n"
                entry += f"  author = {{{author}}},\n"
                entry += f"  title = {{{title}}},\n"
                entry += f"  school = {{{school_full}}},\n"
                entry += f"  year = {{{year}}},\n"
                entry += "}"
                bib_entries.append(entry)
            else:
                print(f"解析无类型标识的引文失败: {citation}")
    
    # 将条目写入 .bib 文件
    with open(output_file, "w", encoding="utf-8") as f:
        for entry in bib_entries:
            f.write(entry + "\n\n")

# 测试样本
citations = [
    "仝玉印.乡村振兴战略背景下成都市运动休闲特色乡村发展研究[D].成都体育学院,2022.DOI:10.26987/d.cnki.gcdtc.2022.000327.",
    "韩书麟.与A4蛋白前体相关的精子膜蛋白YWK-Ⅱ抗原cDNA的克隆表达及其功能研究[D].中国协和医科大学,2000.",
    "王正公.论肺痨的证治[J].上海中医药杂志,1960,(03):14-16.DOI:10.16305/j.1007-1334.1960.03.003.",
    "梅磊,徐培潭.循環記憶法的生理機制研究[J].生理学报,1954,(01):143-154.",
    "格日力, 高原低氧适应与损伤机制研究. 青海省, 青海大学, 1993-01-16.",
    "马根山, 缺氧预适应心脏祖细胞在心肌梗死后心室重构中的作用及机制研究. 江苏省, 东南大学附属中大医院, 2009-04-30.",
    "白云锋. 行政黑名单制度的法律属性及其可诉性——基于规范结构的实证分析 [J]. 重庆大学学报(社会科学版), 2025, 31 (01): 259-271.",
    "郭欢.有氧运动介导CUMS大鼠海马神经炎症的研究[D].成都体育学院,2020.DOI:10.26987/d.cnki.gcdtc.2020.000263."
]

# 调用函数生成 .bib 文件
generate_bib(citations, "citations.bib")
