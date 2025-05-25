def endnote_to_bibtex(citation_list, output_file='output.bib'):
    """
    将 EndNote 格式的引文列表转换为 BibTeX 格式，处理行首不规范空格，并根据 %0 和 %9 判断文献类型。
    先打印生成的 BibTeX 条目到控制台，再保存到指定的 .bib 文件。

    参数:
    - citation_list (list): 包含多个 EndNote 格式引文字符串的列表。
    - output_file (str): 输出 .bib 文件的名称或路径，默认为 'output.bib'。
    """
    # EndNote 标签到 BibTeX 字段的映射
    tag_mapping = {
        '%A': 'author',
        '%T': 'title',
        '%J': 'journal',  # 默认映射，Thesis 中会调整为 school
        '%D': 'year',
        '%V': 'volume',
        '%N': 'number',
        '%P': 'pages',
        '%R': 'doi',
        '%U': 'url',
        '%X': 'abstract'
    }

    # 打开文件以写入所有条目
    with open(output_file, 'w', encoding='utf-8') as f:
        for idx, endnote_citation in enumerate(citation_list):
            # 用于存储解析后的字段
            fields = {}
            authors = []
            affiliations = []
            ref_type = 'article'  # 默认类型
            thesis_type = None

            # 将引文按行分割
            lines = endnote_citation.strip().split('\n')

            # 解析每一行
            for line in lines:
                # 去除行首的空白字符
                line = line.lstrip()
                if line.startswith('%'):
                    parts = line.split(None, 1)
                    if len(parts) == 2:
                        tag, value = parts
                        if tag == '%A':
                            cleaned_authors = [author.strip() for author in value.split(',') if author.strip()]
                            authors.extend(cleaned_authors)
                        elif tag == '%+':
                            cleaned_affiliations = [aff.strip() for aff in value.split(',') if aff.strip()]
                            affiliations.extend(cleaned_affiliations)
                        elif tag == '%0':
                            value = value.strip().lower()
                            if 'journal article' in value:
                                ref_type = 'article'
                            elif 'thesis' in value:
                                ref_type = 'thesis'
                            elif 'book' in value:
                                ref_type = 'book'
                            elif 'conference paper' in value:
                                ref_type = 'inproceedings'
                        elif tag == '%9':
                            value = value.strip().lower()
                            if '硕士' in value:
                                thesis_type = 'mastersthesis'
                            elif '博士' in value:
                                thesis_type = 'phdthesis'
                        elif tag in tag_mapping:
                            fields[tag_mapping[tag]] = value.strip()

            # 设置 author 字段
            if authors:
                fields['author'] = ' and '.join(authors)
            else:
                fields['author'] = 'Unknown'

            # 设置 affiliation 字段
            if affiliations:
                fields['affiliation'] = ', '.join(affiliations)

            # 确定最终文献类型
            if ref_type == 'thesis' and thesis_type:
                ref_type = thesis_type
            elif ref_type == 'thesis':
                ref_type = 'mastersthesis'  # 默认硕士论文

            # 对于 Thesis，将 %J 映射为 school
            if ref_type in ['mastersthesis', 'phdthesis'] and 'journal' in fields:
                fields['school'] = fields.pop('journal')

            # 生成 BibTeX 键
            first_author = fields['author'].split(' and ')[0].split()[0].lower()
            bibtex_key = f"{first_author}{fields.get('year', '0000')}_{idx}"  # 添加索引以避免键冲突

            # 构造 BibTeX 条目
            bibtex_entry = f"@{ref_type}{{{bibtex_key},\n"
            for key, value in fields.items():
                bibtex_entry += f"  {key} = {{{value}}},\n"
            bibtex_entry += "}"

            # 打印 BibTeX 条目到控制台
            print(f"生成的 BibTeX 条目 {idx + 1}：")
            print(bibtex_entry)
            print()

            # 写入文件
            f.write(bibtex_entry + '\n\n')

    print(f"所有 BibTeX 条目已写入 {output_file}")

# 测试用例
citation_list = [
    """%0 Journal Article
     %A 陈秀山
%+ 中国人民大学经济学系
%T 芝加哥学派竞争理论评析
%J 经济学动态
%D 1995
     %N 01
%X  芝加哥学派在过去是货币主义的同义语,...
%P 56-60
%U https://kns.cnki.net/kcms2/article/abstract?...""",
    """%0 Thesis
     %A 张存明
   %T 企业经营团队三维管理模型研究
   %J 河北工业大学
%9 硕士
   %D 2008
   %X 企业经营团队管理的研究是一个关系到企业长远发展的具有战略意义的课题,...
%U https://kns.cnki.net/kcms2/article/abstract?..."""
]

# 调用函数
endnote_to_bibtex(citation_list, 'citation_EndNote.bib')
