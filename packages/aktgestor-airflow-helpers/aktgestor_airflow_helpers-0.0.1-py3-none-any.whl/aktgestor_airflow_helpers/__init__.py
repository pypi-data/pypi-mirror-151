from jinjasql import JinjaSql
jinja = JinjaSql(param_style='pyformat')

def read_sql_file(file_path,params = None):
    with open(file_path, 'r') as f:
        sql = f.read()
        query, bind_params = jinja.prepare_query(sql, params)
        return {'sql' : query, 'parameters' : bind_params}