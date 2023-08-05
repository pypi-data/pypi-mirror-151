import ast


def is_column_sql(sql_line: str):
    """
    判断一个SQL行是否是合法的列定义SQL
    """
    return not sql_line.strip().upper().startswith(('PRIMARY ', 'KEY ', 'CONSTRAINT ', 'UNIQUE '))


def parse_column_sql(sql_line: str):
    """
    返回：col_name, sql_type, comment
    """
    sql_line = sql_line.strip().rstrip(',')
    if ' COMMENT ' in sql_line:
        sql_line, comment_part = sql_line.split(' COMMENT ', 1)
        comment = ast.literal_eval(comment_part)
    else:
        comment = ''
    col_name, sql_type = sql_line.split(None, 2)[:2]
    col_name = col_name.strip('`')
    return col_name, sql_type, comment


def guess_mockjs(sql_type, name, comment):
    if sql_type.startswith(('enum', 'ENUM')):
        return sql_type.replace('enum', '@pick').replace('ENUM', '@pick')
    sql_type = sql_type.lower()
    if sql_type == 'date':
        return '@date'
    elif sql_type == 'datetime':
        return '@datetime'
    elif sql_type.startswith('bigint'):
        return '@natural'
    elif sql_type.startswith('int'):
        return '@integer(0, 1000000)'
    elif sql_type.startswith('enum'):
        return sql_type.replace('enum', '@pick')
    elif '是否' in comment:
        return '@boolean'
    elif comment.endswith('姓名'):
        return '@cname'
    elif name.lower().endswith(('phone', 'mobile')):
        return '1@integer(3000000000, 9900000000)'
    elif name.lower().endswith('ipaddress') or comment.lower().endswith('ip地址'):
        return '@ip'
    elif name.lower().endswith('address') or comment.endswith('地址'):
        return '@county@cword(2)街@integer(1,100)号@cword(4)小区'
    else:
        return ''
