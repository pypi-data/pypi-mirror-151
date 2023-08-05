import ast
import json
import re


def render_create_sql_frame(table_name: str, table_comment: str, primary_key: str, sql_lines: list):
    sql_body = '\n'.join(sql_lines)
    return f"""CREATE TABLE `{table_name}` (
{sql_body}
    PRIMARY KEY (`{primary_key}`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='{table_comment}';"""


def render_sql_line(col_name: str, sql_type: str, comment: str, mockjs: str, is_primary: bool):
    if mockjs.startswith('@natural'):
        sql_type = 'bigint(20) unsigned'
    elif sql_type.lower() == 'int':
        sql_type += '(11)'
    elif sql_type.lower() == 'bigint':
        sql_type += '(20)'
    elif sql_type.lower() == 'tinyint':
        sql_type += '(4)'
    elif sql_type.lower() == 'varchar':
        sql_type += '(200)'
    if col_name.lower().replace('_','') == 'nickname':
        sql_type += ' COLLATE utf8mb4_unicode_ci'
    comment = comment.replace("'", '"')
    default_part = ' DEFAULT NULL'
    if is_primary:
        default_part = ' NOT NULL'
    elif sql_type.lower() in ['text', 'blob']:
        default_part = ''
    elif col_name.lower().replace('_','') in ['createdat', 'updatedat', 'createtime', 'updatetime']:
        default_part = ' DEFAULT CURRENT_TIMESTAMP'
    extra_part = ''
    if col_name.lower().replace('_','') in ['updatedat', 'updatetime']:
        extra_part = ' ON UPDATE CURRENT_TIMESTAMP'
    elif is_primary and 'int' in sql_type.lower():
        extra_part = ' AUTO_INCREMENT'
    return f"""    `{col_name}` {sql_type}{default_part}{extra_part} COMMENT '{comment}',"""


def quote_mockjs(mockjs: str):
    if re.match('^[0-9.]+$', mockjs) or mockjs in ['true', 'false']:
        return str(mockjs)
    if mockjs.startswith(('"', "'")) and mockjs.endswith(('"', "'")):
        mockjs = ast.literal_eval(mockjs)
    return json.dumps(mockjs, ensure_ascii=False)


def render_json5(shimo_rows):
    body_lines = []
    for name, sql_type, mockjs, comment in shimo_rows:
        mockjs = quote_mockjs(mockjs)
        comment = comment.replace('//', ' ').replace('\n', ' ')
        line = f'''    "{name}": {mockjs}, //{comment}'''
        body_lines.append(line)
    return '{\n' + '\n'.join(body_lines) + '\n}'


def render_yapi_query(shimo_rows):
    body_lines = []
    for name, sql_type, mockjs, comment in shimo_rows:
        comment = comment.replace(':', '=').replace('\n', ';')
        line = f'''{name}:{comment}'''
        body_lines.append(line)
    return '\n'.join(body_lines)
