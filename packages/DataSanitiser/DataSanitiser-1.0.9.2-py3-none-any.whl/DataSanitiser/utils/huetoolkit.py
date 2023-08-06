import os
import numpy as np
import pandas as pd


def check_reserved_field_name(cols):
    cols = set(cols)
    res = {'file_name', 'load_dt'}
    ident = res.intersection(cols)
    if len(ident) > 0:
        print('Reserved Column Name Exists', ident)
    else:
        print('No Issue')


def check_dup_columns(cols):
    cols_lower = np.array([c.lower() for c in cols])
    unq, cnt = np.unique(cols_lower, return_counts=True)
    dup = unq[cnt > 1]
    dup = [c for c in cols if c.lower() in dup]
    print(f'Duplicated Columns: {dup}')


def generate_hue_dict(fp: list, ins: list = None):
    """
    Args:
        fp (list): [description]
        ins (dict, optional): [description]. Defaults to None.
        dict_file_name (str, optional): [description].
            Defaults to 'prod_audit_header_info.dic'.
    """
    def generate_hue_dict_item(fp: str, ins: dict = None):
        fc = os.path.basename(fp).split('.')
        fn = fc[0]
        fe = fc[1]
        if fe.lower() != 'csv':
            raise IOError(f'File {fp} is not a csv file')
        try:
            df = pd.read_csv(fp, nrows=1)
        except:
            raise IOError(f'Error when reading file {fp}')
        if ins is None:
            col_def = ','.join(
                ['"' + col + ' string' + '"' for col in df.columns])
        else:
            col_def = ','.join(['"' + col + f' {ins[col]}' + '"'
                                if col in ins.keys()
                                else '"' + col + ' string' + '"'
                                for col in df.columns])

        dict_rec = '"' + fn + '":[' + col_def + ']'
        return dict_rec
    dict_items = []
    for p, i in zip(fp, ins):
        dict_items.append(generate_hue_dict_item(p, i))
    dict_items = ',\n'.join(dict_items)
    dict_export = '{\n' + dict_items + '\n}'
    return dict_export


def generate_hue_csv(file_dir: list, file_name: list, table_name: list):
    cols = ['flow_type', 'lob', 'subject_area', 'ingestion_type', 'load_type',
            'is_control_file', 'destination_type', 'source_db', 'source_table',
            'target_table', 'target_db', 'lake_db', 'select_columns',
            'lake_partitions', 'partition_deriving_columns', 'lake_partition_logic',
            'bucket_columns', 'no_of_buckets', 'storage_type', 'lake_storage_type',
            'no_of_mappers', 'file_format', 'header_avail', 'part_file',
            'delimiter', 'mask_columns', 'timestamp_format', 'split_column']
    df = pd.DataFrame(columns=cols)

    def _add_row(df, file_dir, file_name, table_name):
        new_row = np.array(
            ['fs_hv', 'audit', 'audit', 'file-based', 'full', 'N', 'hive-table',
             file_dir,
             file_name,
             table_name,
             'p_audit_users_db',
             np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
             'parquetfile', 'parquet', 8, 'CSV', True, False, ',', np.nan,
             '%Y%m%d%H%M%S', np.nan], dtype=object)
        df.loc[df.shape[0], :] = new_row
        return df
    for i in range(len(file_dir)):
        df = _add_row(df, file_dir[i], file_name[i], table_name[i])
    return df


def prepare_hue_files(path_file_in: list, file_dir: list,
                      table_name: list, ins: list):
    dir_file_out = os.path.dirname(path_file_in[0])
    file_name = [os.path.basename(fn).split('.')[0] for fn in path_file_in]

    try:
        dict_file_path = os.path.join(
            dir_file_out, 'prod_audit_header_info.dic')
        dict_export = generate_hue_dict(path_file_in, ins)
        with open(dict_file_path, 'w') as f:
            f.write(dict_export)
        print(f'HUE DICT was generated: {dict_file_path}')
    except:
        print('Error - HUE DICT')
    try:
        csv_file_path = os.path.join(dir_file_out, 'prod_audit_full.csv')
        df_csv = generate_hue_csv(file_dir, file_name, table_name)
        df_csv.to_csv(csv_file_path, index=False)
        print(f'HUE CSV  was generated: {csv_file_path}')
    except:
        print('Error - HUE CSV')
