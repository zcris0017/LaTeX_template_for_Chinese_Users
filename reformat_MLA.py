import re

def mla_to_bibtex(mla_citation, output_file="references.bib"):
    """
    将 MLA 格式的引文转换为 BibTeX 格式，支持页数和 DOI URL 识别，并写入 .bib 文件。
    
    参数：
        mla_citation (str): MLA 格式的引文字符串。
        output_file (str): 输出 .bib 文件的路径，默认为 "references.bib"。
    
    返回：
        str: 生成的 BibTeX 条目字符串。
    """
    # 初始化 BibTeX 条目
    bibtex_entry = ""
    
    # 识别引文类型：学位论文
    if "thesis" in mla_citation or "dissertation" in mla_citation:
        entry_type = "phdthesis" if "PhD" in mla_citation else "mastersthesis"
        pattern = r"(.+?)\.\s*(.+?)\.\s*(\d{4})\.\s*(.+?),\s*(MA thesis|PhD dissertation)\."
        match = re.match(pattern, mla_citation)
        if match:
            authors, title, year, school, thesis_type = match.groups()
            # 处理作者名
            if ',and ' in authors:
                authors = authors.replace(',and ', ' and ')
            else:
                authors = authors.replace(',', ' and ')
            # 生成唯一的条目键
            entry_key = f"{authors.split(' ')[0].lower()}{year}"
            bibtex_entry = f"@{entry_type}{{{entry_key},\n"
            bibtex_entry += f"  author = {{{authors}}},\n"
            bibtex_entry += f"  title = {{{title}}},\n"
            bibtex_entry += f"  school = {{{school}}},\n"
            bibtex_entry += f"  year = {{{year}}},\n"
            bibtex_entry += f"  type = {{{thesis_type}}}\n"
            bibtex_entry += "}"
        else:
            return "无法解析的学位论文格式"
    
    # 识别引文类型：期刊文章（带 DOI）
    else:
        entry_type = "article"
        # 更新正则表达式，使期号可选
        pattern_with_doi = r"(.+?)\.\s*\"(.+?)\"\.\s*(.+?)\s+(\d+)(?:\.\s*(\w+))?\s+\((\d{4})\):\s*(\d+-\d+)\.\s*(doi:.+?)\."
        match = re.match(pattern_with_doi, mla_citation)
        if match:
            authors, title, journal, volume, issue, year, pages, doi = match.groups()
            # 处理作者名
            if ',and ' in authors:
                authors = authors.replace(',and ', ' and ')
            else:
                authors = authors.replace(',', ' and ')
            # 生成唯一的条目键
            entry_key = f"{authors.split(' ')[0].lower()}{year}"
            bibtex_entry = f"@{entry_type}{{{entry_key},\n"
            bibtex_entry += f"  author = {{{authors}}},\n"
            bibtex_entry += f"  title = {{{title}}},\n"
            bibtex_entry += f"  journal = {{{journal}}},\n"
            bibtex_entry += f"  volume = {{{volume}}},\n"
            if issue is not None:
                bibtex_entry += f"  number = {{{issue}}},\n"
            bibtex_entry += f"  pages = {{{pages}}},\n"
            bibtex_entry += f"  year = {{{year}}},\n"
            # 清理 DOI，去除 "doi:" 前缀和末尾句号
            doi = doi.split(':')[1].strip().rstrip('.')
            bibtex_entry += f"  doi = {{{doi}}},\n"
            bibtex_entry += "}"
        else:
            # 期刊文章（不带 DOI）
            pattern_no_doi = r"(.+?)\.\s*\"(.+?)\"\.\s*(.+?)\s+(\d+)(?:\.\s*(\w+))?\s+\((\d{4})\):\s*(\d+-\d+)\."
            match = re.match(pattern_no_doi, mla_citation)
            if match:
                authors, title, journal, volume, issue, year, pages = match.groups()
                # 处理作者名
                if ',and ' in authors:
                    authors = authors.replace(',and ', ' and ')
                else:
                    authors = authors.replace(',', ' and ')
                # 生成唯一的条目键
                entry_key = f"{authors.split(' ')[0].lower()}{year}"
                bibtex_entry = f"@{entry_type}{{{entry_key},\n"
                bibtex_entry += f"  author = {{{authors}}},\n"
                bibtex_entry += f"  title = {{{title}}},\n"
                bibtex_entry += f"  journal = {{{journal}}},\n"
                bibtex_entry += f"  volume = {{{volume}}},\n"
                if issue is not None:
                    bibtex_entry += f"  number = {{{issue}}},\n"
                bibtex_entry += f"  pages = {{{pages}}},\n"
                bibtex_entry += f"  year = {{{year}}},\n"
                bibtex_entry += "}"
            else:
                return "无法解析的期刊文章格式"
    
    # 将 BibTeX 条目写入文件
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(bibtex_entry + "\n\n")
    
    return bibtex_entry

# 测试函数
citations = [
    '刘克明,and 赵香兰. "细菌细胞壁成分与药物抗菌作用机制问题." 广东医学 2. S1 (1964): 34-36. doi:10.13820/j.cnki.gdyx.1964.s1.017.',
    '王妙月,杨懋源,胡毓良,李自强,陈运泰,金严,冯锐. "新丰江水库地震的震源机制及其成因初步探讨." 地球物理学报 01 (1976): 1-17.',
    'J.Genest. "Ⅰ.高血压病发病机制研究概况." 中国循环杂志 01 (1988): 35-36.',
    '梅磊,and 徐培潭. "循環記憶法的生理機制研究." 生理学报 01 (1954): 143-154.',
    '张存明. 企业经营团队三维管理模型研究. 2008. 河北工业大学, MA thesis.',
    '饶犇. 粘质沙雷氏菌产2,3-丁二醇的调控机制及代谢工程研究. 2017. 华东理工大学, PhD dissertation.',
    '王振波,and 吴湘玲. "数字时代深度伪造技术研究——机理特征、功能异化及其优化理路." 北京航空航天大学学报(社会科学版) 38. 02 (2025): 47-55. doi:10.13766/j.bhsk.1008-2204.2022.0148.'
]

# 清空文件并写入测试结果
with open("references.bib", "w", encoding="utf-8") as f:
    f.write("")

for citation in citations:
    result = mla_to_bibtex(citation)
    print(result)
    print("\n")
