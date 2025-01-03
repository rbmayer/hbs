import configparser as cp
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from hbs.queries import get_treated_subclass_query, get_control_subclass_query

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def get_mysql_login(access='remote'):
    """
    Read config params for MySQL server.
    :param access: 'local' or 'remote
    :return: config params
    """
    remote_params_path = ''
    local_params_path = ''
    config = cp.ConfigParser()
    if access == 'remote':
        block = 'mysql.titan'
        config.read(remote_params_path)
    elif access == 'local':
        block = 'mysql.access'
        config.read(local_params_path)
    host = config[block]['host']
    port = config[block]['port']
    user = config[block]['user']
    pwd = config[block]['password']
    return host, port, user, pwd


def create_engine_to_hbs(access='remote'):
    """
    params: access = 'local' or 'remote
    """
    if access == 'remote':
        host, port, user, pwd = get_mysql_login('remote')
    elif access == 'local':
        host, port, user, pwd = get_mysql_login('local')
    dialect = 'mysql'
    driver = 'mysqlconnector'
    database = 'hbs'
    dbase_url = f"{dialect}+{driver}://{user}:{pwd}@{host}/{database}"
    return create_engine(dbase_url)


def get_mcnemar_test_inputs(year, category, engine, baseline=True, ):
    """Query the database to retrieve disease flags of matched pairs for McNemar analysis."""
    treated_subclass_query = get_treated_subclass_query(year=year, category=category, baseline=baseline)
    treated_subclass = pd.read_sql(treated_subclass_query, con=engine)
    control_subclass_query = get_control_subclass_query(year=year, category=category)
    control_subclass = pd.read_sql(control_subclass_query, con=engine)
    # combine matched controls to treated subjects.
    # exclude any subclasses with no treated or no control (inner join).
    pairs = pd.merge(left=treated_subclass, right=control_subclass, how='inner', on='subclass')
    return pairs


def get_mcnemar_contingency_table(df):
    """Return 2x2 array of counts for each combination of treated + matched control disease status. Rows of array represent control status ordered by status=1, status=0. Columns represent status of treated ordered by status=1, status=0. """
    # assign contingency table bucket group
    df['contingency_table_cell'] = df.apply(lambda row: str(row['dementia_flag_c']) + str(row['dementia_flag_t']), axis=1)
    contingency_table = np.array([(df.loc[df['contingency_table_cell'] == '11', 'subclass'].count(),
                               df.loc[df['contingency_table_cell'] == '10', 'subclass'].count()),
                              (df.loc[df['contingency_table_cell'] == '01', 'subclass'].count(),
                               df.loc[df['contingency_table_cell'] == '00', 'subclass'].count())])
    return contingency_table