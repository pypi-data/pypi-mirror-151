from lesscli import add_subcommand
from arms.utils.grammar import is_column_sql, parse_column_sql, guess_mockjs
from arms.utils.templates import render_sql_line, render_create_sql_frame, render_json5, render_yapi_query
from arms.utils.wordstyle import word_to_style, WordStyle
from InquirerPy import inquirer
import pyperclip
import re
from rich.console import Console
from rich.syntax import Syntax


console = Console()


def blank_func():
    pass


def copy_board():
    """
    展示当前的粘贴板内容（不超过1000行和10KB），
    选择确认/放弃
    选确认则返回粘贴板内容
    """
    splitor_start = '─────────────────────────'
    splitor_end = '───────────────────────────'
    content = pyperclip.paste()
    if len(content.splitlines()) > 1000 or len(content) > 10240:
        content = '（粘贴板内容超过了1000行或10KB）'
    content = content.strip()
    answer = inquirer.select(
        message=splitor_start + '\n' + content + '\n' + splitor_end,
        choices=['确认使用粘贴板内容', '放弃'],
        default=None,
    ).execute()
    if answer == '放弃':
        exit(0)
    return content


def design_shimo_to_sql():
    """
    复制石墨表格，转换成建表SQL，保存到粘贴板
    石墨表格的格式：字段名(驼峰)、类型(SQL)、mockjs、注释
    """
    shimo_content = copy_board()
    camel_stype = inquirer.select(
        message="请选择数据库字段风格",
        choices=['蛇形', '驼峰'],
        default=None,
    ).execute() == '驼峰'
    table_name = inquirer.text(message="请输入数据库表名:").execute()
    table_comment = inquirer.text(message="请输入表的中文注释:").execute()
    sql_lines = []
    primary_key = ''
    for pos, row in enumerate(shimo_content.splitlines()):
        seg_size = len(segs := row.split('\t'))
        assert seg_size == 4, f'第{pos+1}行包含{seg_size}列，应该包含4列'
        name, sql_type, mockjs, comment = segs
        if not camel_stype:
            col_name = word_to_style(name, WordStyle.lower_snake)
        else:
            col_name = name
        if pos == 0:
            primary_key = col_name
        sql_lines.append(render_sql_line(col_name, sql_type, comment, mockjs, pos == 0))
    sql_content = render_create_sql_frame(table_name, table_comment, primary_key, sql_lines)
    print('创建数据库的SQL如下：')
    console.print(Syntax(sql_content, 'sql'))
    pyperclip.copy(sql_content)
    print('已复制到粘贴板！')


def design_sql_to_shimo():
    """
    复制建表SQL，转换成石墨表格，保存到粘贴板
    石墨表格的格式：字段名(驼峰)、类型(SQL)、mockjs、注释
    """
    sql_content = copy_board()
    seed = re.compile(r'CREATE TABLE *`?(\w+)`? *\((.*)\)', flags=re.I|re.DOTALL)
    match_size = len(find_ret := seed.findall(sql_content))
    assert match_size == 1, '无法解析该建表SQL'
    table_name, sql_body = find_ret[0]
    shimo_lines = []
    for sql_line in sql_body.splitlines():
        if sql_line and is_column_sql(sql_line):
            col_name, sql_type, comment = parse_column_sql(sql_line)
            name = word_to_style(col_name, WordStyle.lower_camel)
            mockjs = guess_mockjs(sql_type, name, comment)
            shimo_line = '\t'.join([name, sql_type, mockjs, comment])
            shimo_lines.append(shimo_line)
    shimo_content = '\n'.join(shimo_lines)
    print('定义实体的石墨文本如下：')
    console.print(Syntax(shimo_content, 'text'))
    pyperclip.copy(shimo_content)
    print('已复制到粘贴板！')


def design_shimo_to_json5():
    """
    复制石墨表格，转化为json5，保存到粘贴板
    石墨表格的格式：字段名(驼峰)、类型(SQL)、mockjs、注释
    """
    shimo_content = copy_board()
    shimo_rows = []
    for pos, row in enumerate(shimo_content.splitlines()):
        seg_size = len(segs := row.split('\t'))
        assert seg_size == 4, f'第{pos + 1}行包含{seg_size}列，应该包含4列'
        shimo_rows.append(segs)
    json5_content = render_json5(shimo_rows)
    print('json5内容如下：')
    console.print(Syntax(json5_content, 'json'))
    pyperclip.copy(json5_content)
    print('已复制到粘贴板！')


def design_shimo_to_query():
    """
    复制石墨表格，转化为YAPIQuery文本，保存到粘贴板
    石墨表格的格式：字段名(驼峰)、类型(SQL)、mockjs、注释
    YAPIQuery文本的格式：name:example（只能把注释放到example的位置）
    """
    shimo_content = copy_board()
    shimo_rows = []
    for pos, row in enumerate(shimo_content.splitlines()):
        seg_size = len(segs := row.split('\t'))
        assert seg_size == 4, f'第{pos + 1}行包含{seg_size}列，应该包含4列'
        shimo_rows.append(segs)
    answer = inquirer.select(
        message='请选择分页请求参数：',
        choices=['pageNum & numPerPage', '不需分页'],
        default=None,
    ).execute()
    if answer == 'pageNum & numPerPage':
        yapi_query_content = 'pageNum:当前页码，从1开始\nnumPerPage:分页大小\n'
    else:
        yapi_query_content = ''
    yapi_query_content += render_yapi_query(shimo_rows)
    print('YAPIQuery文本如下：')
    console.print(Syntax(yapi_query_content, 'text'))
    pyperclip.copy(yapi_query_content)
    print('已复制到粘贴板！')


@add_subcommand('shimo-to-sql', design_shimo_to_sql)
@add_subcommand('sql-to-shimo', design_sql_to_shimo)
@add_subcommand('shimo-to-json5', design_shimo_to_json5)
@add_subcommand('shimo-to-query', design_shimo_to_query)
def run_design():
    """生成文本并复制"""
    pass


@add_subcommand('controller', blank_func)  #新建或修改
@add_subcommand('dto', blank_func)  #仅新建
@add_subcommand('vo', blank_func)  #仅新建
@add_subcommand('entity', blank_func)  #仅新建
@add_subcommand('service', blank_func)  #仅新建
def run_codegen():
    """
    生成文件或修改文件
    自动识别编程语言
    """
    pass
