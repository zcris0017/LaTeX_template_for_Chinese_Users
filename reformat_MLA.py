import re

def _parse_citation(mla_citation):
    """
    解析单个 MLA 格式引文并生成 BibTeX 条目。
    
    参数：
        mla_citation (str): MLA 格式的引文字符串。
    
    返回：
        str: 生成的 BibTeX 条目，或错误信息。
    """
    bibtex_entry = ""

    # 检查是否为学位论文
    if "thesis" in mla_citation.lower() or "dissertation" in mla_citation.lower():
        entry_type = "phdthesis" if "phd" in mla_citation.lower() else "mastersthesis"
        pattern = r"(.+?)\.\s*(.+?)\.\s*(\d{4})\.\s*(.+?),\s*(MA thesis|PhD dissertation)\."
        match = re.match(pattern, mla_citation)
        if match:
            authors, title, year, school, thesis_type = match.groups()
            if ',and ' in authors:
                authors = authors.replace(',and ', ' and ')
            else:
                authors = authors.replace(',', ' and ')
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
    else:
        # 处理期刊文章（带 DOI）
        pattern_with_doi = r"(.+?)\.\s*\"(.+?)\"\s*(.+?)\s+(\d+)(?:\.\s*(\w+))?\s+\((\d{4})\):\s*(\d+-\d+)\.\s*(doi:.+)"
        match = re.match(pattern_with_doi, mla_citation)
        if match:
            authors, title, journal, volume, issue, year, pages, doi_raw = match.groups()
            if ',and ' in authors:
                authors = authors.replace(',and ', ' and ')
            else:
                authors = authors.replace(',', ' and ')
            entry_key = f"{authors.split(' ')[0].lower()}{year}"
            bibtex_entry = f"@article{{{entry_key},\n"
            bibtex_entry += f"  author = {{{authors}}},\n"
            bibtex_entry += f"  title = {{{title}}},\n"
            bibtex_entry += f"  journal = {{{journal}}},\n"
            bibtex_entry += f"  volume = {{{volume}}},\n"
            if issue:
                bibtex_entry += f"  number = {{{issue}}},\n"
            bibtex_entry += f"  pages = {{{pages}}},\n"
            bibtex_entry += f"  year = {{{year}}},\n"
            doi = doi_raw[4:].rstrip('.').strip()
            bibtex_entry += f"  doi = {{{doi}}},\n"
            bibtex_entry += "}"
        else:
            # 处理期刊文章（不带 DOI）
            pattern_no_doi = r"(.+?)\.\s*\"(.+?)\"\s*(.+?)\s+(\d+)(?:\.\s*(\w+))?\s+\((\d{4})\):\s*(\d+-\d+)\."
            match = re.match(pattern_no_doi, mla_citation)
            if match:
                authors, title, journal, volume, issue, year, pages = match.groups()
                if ',and ' in authors:
                    authors = authors.replace(',and ', ' and ')
                else:
                    authors = authors.replace(',', ' and ')
                entry_key = f"{authors.split(' ')[0].lower()}{year}"
                bibtex_entry = f"@article{{{entry_key},\n"
                bibtex_entry += f"  author = {{{authors}}},\n"
                bibtex_entry += f"  title = {{{title}}},\n"
                bibtex_entry += f"  journal = {{{journal}}},\n"
                bibtex_entry += f"  volume = {{{volume}}},\n"
                if issue:
                    bibtex_entry += f"  number = {{{issue}}},\n"
                bibtex_entry += f"  pages = {{{pages}}},\n"
                bibtex_entry += f"  year = {{{year}}},\n"
                bibtex_entry += "}"
            else:
                return "无法解析的期刊文章格式"

    return bibtex_entry if bibtex_entry else "无法解析的引文格式"

def mla_to_bibtex(mla_citations, output_file="references.bib"):
    """
    将 MLA 格式引文列表转换为 BibTeX 格式，并在处理完所有引文后写入 .bib 文件。
    
    参数：
        mla_citations (list): MLA 格式的引文字符串列表。
        output_file (str): 输出 .bib 文件的路径，默认为 "references.bib"。
    
    返回：
        list: 生成的 BibTeX 条目列表。
    """
    if not isinstance(mla_citations, list):
        raise ValueError("mla_citations 必须是一个字符串列表")

    bibtex_entries = []
    for citation in mla_citations:
        result = _parse_citation(citation)
        if result.startswith("@"):  # 成功的 BibTeX 条目以 @ 开头
            bibtex_entries.append(result)
        else:
            print(f"解析失败: {result}，引文内容：{citation}")

    # 在处理完所有引文后一次性写入文件
    if bibtex_entries:
        try:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write("\n\n".join(bibtex_entries) + "\n\n")
            print(f"成功将 {len(bibtex_entries)} 个 BibTeX 条目写入 {output_file}")
        except Exception as e:
            print(f"写入文件时出错: {e}")
            return bibtex_entries  # 返回条目，即使写入失败也能查看结果
    else:
        print("没有生成任何 BibTeX 条目，未写入文件")

    return bibtex_entries

# 测试代码
citations = [
    '刘克明,and 赵香兰. "细菌细胞壁成分与药物抗菌作用机制问题." 广东医学 2. S1 (1964): 34-36. doi:10.13820/j.cnki.gdyx.1964.s1.017.',
    '张存明. 企业经营团队三维管理模型研究. 2008. 河北工业大学, MA thesis.'
]

output_file = "citation_MLA.bib"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("")  # 清空文件

results = mla_to_bibtex(citations, output_file)
print("生成的 BibTeX 条目：")
for result in results:
    print(result)
    print()
