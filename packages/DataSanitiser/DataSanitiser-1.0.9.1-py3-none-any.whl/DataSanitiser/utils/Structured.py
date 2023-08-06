import os
import pandas as pd
import numpy as np
from datetime import datetime
from scipy import integrate
from scipy import stats
import csv
import time
import warnings
warnings.filterwarnings("ignore")


class Pipeline():
    def __init__(self, mode='batch', dir_in=None, dir_out=None, dir_ign=None,
                 dir_bckp=None, version=None):
        # info
        self.author = "Author: Colin Li"
        print("Disclaimer: This is a Minimal Viable Product (MVP)")
        print(self.author)

        # i/o
        self.df_in = None
        self.df_out = None
        self.date_format = "%Y-%m-%d"
        self.version = (
            version,
            datetime.now().strftime("%Y_%m_%d")
        )[version is None]

        # formatting
        self.file_format = 'csv'
        self.char_to_esc = [',', '"', "'"]
        self.cols_date = None
        self.cols_percentage = None
        self.cols_float = None
        self.cols_int = None
        self.precision_min = 9

        self.file_format_in = None
        self.header_in_range = 5
        self.footer_in_range = 5

        # workload
        self.dir_in = dir_in
        self.dir_out = dir_out
        self.dir_ign = dir_ign
        self.dir_bckp = dir_bckp
        self.files_xls = []
        self.files_xlsx = []
        self.files_csv = []

        # mapping
        self.df_mapping = None
        self.df_ts = None

        # schema
        self.schema = None

        if mode == 'batch':
            self.__calculate_workload()
        elif mode == 'single':
            pass
        else:
            raise KeyError("Mode should be either 'batch' or 'single'")

    def __calculate_workload(self):
        """
        recursively search relevant data files within a directory
        """
        for root, dirs, fns in os.walk(self.dir_in):
            for fn in fns:
                if root != self.dir_ign:
                    ext = fn.split('.')[-1]
                    if ext.lower() == 'xls':
                        self.files_xls.append(os.path.join(root, fn))
                    elif ext.lower() == 'xlsx':
                        self.files_xlsx.append(os.path.join(root, fn))
                    elif ext.lower() in ['enc', 'csv']:
                        self.files_csv.append(os.path.join(root, fn))

        print('\nWorkload:\n'
              f'Number of Excel File (*.xls ): {len(self.files_xls)}\n'
              f'Number of Excel File (*.xlsx): {len(self.files_xlsx)}\n'
              f'Number of CSV File   (*.csv ): {len(self.files_csv)}\n')

    def store_file_timestamps(self):
        files = self.files_csv + self.files_xlsx + self.files_xls
        file_ts = []
        for fp in files:
            fn = os.path.basename(fp)
            fmodt = datetime.strptime(time.ctime(os.path.getmtime(fp)), "%c")
            fcret = datetime.strptime(time.ctime(os.path.getctime(fp)), "%c")
            file_ts.append((fn, fcret, fmodt))
        self.df_ts = pd.DataFrame(
            file_ts, columns=['src_file_name', 'src_file_cre_dt', 'src_file_mod_dt'])
        self.df_ts.to_excel(os.path.join(
            self.dir_out, 'meta_data_' + str(self.version) + '.xlsx'), index=False)

    def parse_and_save_bad_csv(self, dir_file, result='df'):

        def bad_row_cleaner(row, num_cols, sep="|"):
            return row[:num_cols - 1] + [sep.join(str(i) for i in row[num_cols - 1:])]

        # determine number of columns
        try:
            with open(dir_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                num_rows = 0
                len_rec = []
                for row in csv_reader:
                    len_rec.append(len(row))
                    num_rows += 1
                num_cols = stats.mode(len_rec).mode[0]
                print(num_cols)

            # sanitise bad rows
            rows = []
            with open(dir_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for i, row in enumerate(csv_reader):
                    if (len(row) < num_cols):
                        continue
                    else:
                        row = bad_row_cleaner(row, num_cols)
                        rows.append(row)
            df = pd.DataFrame(rows)
            col_names = df.iloc[0]  # grab the first row for the header
            df = df[1:]  # take the data less the header row
            df.columns = col_names  # set the header row as the df header
            if result == 'df':
                return df
            else:
                df.to_csv(dir_file, index=False)
                print(
                    f' CSV  ⚠️: File was fixed and overwritten to {dir_file}')
        except:
            raise RuntimeError("Error occurred while parsing and saving CSV")

    def rewrite_old_excel_file(self, fp_old, df):
        fn_new = os.path.basename(fp_old).split('.')[0] + '.xlsx'
        fp_new = os.path.join(os.path.dirname(fp_old), fn_new)
        df.to_excel(fp_new, index=False)
        os.remove(fp_old)
        self.files_xls.remove(fp_old)
        self.files_xls.append(fp_new)
        print(f'Excel ⚠️: File was fixed and overwritten as {fp_new}')
        return fn_new

    def generate_mapping(self):
        """
        generate mapping file
        """
        file_meta = []
        files_excel = self.files_xlsx + self.files_xls
        files_csv = self.files_csv
        files = files_excel + files_csv

        for fdir in files:
            fn = os.path.basename(fdir)
            en = fn.split('.')[1]

            if fdir in files_excel:
                try:
                    ex = pd.ExcelFile(fdir)
                    for sht in ex.sheet_names:
                        df = ex.parse(sht, nrows=15)
                        if df.shape[0] != 0:
                            header_loc = self.detect_header_loc_v1(df)
                            # print(fdir, header_loc)
                            df = ex.parse(sht, nrows=15, header=header_loc)
                            for col in df.columns:
                                file_meta.append((fn, sht, col, header_loc))
                            print(f'Excel ✅: {fn}')
                        else:
                            continue
                except:
                    try:
                        df = pd.read_html(fdir)[0]
                        if df.shape[0] != 0:
                            fn_new = self.rewrite_old_excel_file(fdir, df)
                            for col in df.columns:
                                file_meta.append((fn_new, 'Sheet1', col, 0))
                            print(f"  ┖─Excel ✅: {fn} --> {fn_new}")
                    except:  # XMLSyntaxError
                        try:
                            df = pd.read_table(fdir, encoding='utf-16-be')
                            if df.shape[0] != 0:
                                fn_new = self.rewrite_old_excel_file(fdir, df)
                                for col in df.columns:
                                    file_meta.append(
                                        (fn_new, 'Sheet1', col, 0))
                                print(f"  ┖─Excel ✅: {fn} --> {fn_new}")
                        except:
                            print(f"Excel ❌: {fn} (Please check this file)")

            elif fdir in files_csv:
                try:
                    df = pd.read_csv(fdir, nrows=15)
                    header_loc = self.detect_header_loc_v1(df)
                    df = pd.read_csv(fdir, header=header_loc, nrows=15)
                    for col in df.columns:
                        file_meta.append((fn, np.nan, col, header_loc))
                    print(f" CSV  ✅: {fn}")
                except:
                    try:
                        self.parse_and_save_bad_csv(fdir, result='file')
                        print(f"  ┖─ CSV  ✅: {fn}")
                    except:
                        print(f" CSV  ❌: {fn} (Please check this file)")

        self.df_mapping = pd.DataFrame(
            file_meta, columns=['fileName', 'sheetName', 'columnName', 'skipTopN'])
        self.df_mapping['mapToColumnName'] = ''
        self.df_mapping['systemName'] = ''
        self.df_mapping['originalDateFormat'] = ''
        self.df_mapping['leftNChars'] = ''
        self.df_mapping['skipLastN'] = ''
        self.df_mapping['noHeader'] = ''
        mfn = os.path.join(self.dir_out,
                           'mapping_file_' + str(self.version) + '.xlsx')
        self.df_mapping.to_excel(mfn, index=False)
        print(f"Mapping file is saved: {mfn}")
        print("IMPORTANT: Please rename this file name"
              "(e.g. adding '_reviewed') after your review.")

    def create_output_df_schema(self, schema):
        self.schema = schema
        self.df_out = pd.DataFrame(self.schema, index=[])
        print("Table has been created!")
        pass

    def detect_header_loc_v1(self, df, nrows=10):
        nrows = min(df.shape[0], nrows)
        # determine non-null value in current header
        no_unnamed = sum(['Unnamed' in a for a in df.columns])
        no_notnull = df.columns.notnull().sum()
        a = np.array([no_notnull - no_unnamed])

        # check following rows
        for i in range(nrows):
            a = np.append(a, df.loc[i].notnull().sum())
        header_loc = np.argmax(a)
        return header_loc

    def parse_excel_worksheet(self, dir_file, sheet_name, sys_name, skip_top_n=0, skip_last_n=0, nrows=None, rename_dict=None, miss_header=False):
        bn = os.path.basename(dir_file)
        ext = bn.split('.')[-1]
        sheet_name = False if pd.isnull(sheet_name) else sheet_name
        ex = pd.ExcelFile(dir_file)
        df = ex.parse(sheet_name, header=skip_top_n,
                      skipfooter=skip_last_n, nrows=nrows)
        if miss_header:
            df = ex.parse(sheet_name, header=None,
                          skipfooter=skip_last_n, nrows=nrows)
        else:
            df = ex.parse(sheet_name, header=skip_top_n,
                          skipfooter=skip_last_n, nrows=nrows)

        # bug fix
        try:
            df.columns = [str(c).strip() for c in df.columns]
        except:
            print('N')

        # rename and only include columns in dict
        try:
            if rename_dict:

                # bug fix
                rename_dict = {str(k).strip(): str(v).strip()
                               for k, v in rename_dict.items()}
                df.rename(columns=rename_dict, inplace=True)
                df = df[rename_dict.values()]
        except:
            print(bn, rename_dict, df.columns)
            raise IOError

        df['extract_name'] = bn
        if 'sys_name' not in rename_dict.values():
            df['sys_name'] = sys_name

        return df

    def parse_csv_file(self, dir_file, sys_name, skip_top_n=0, skip_last_n=0, nrows=None, rename_dict=None, miss_header=False):
        bn = os.path.basename(dir_file)
        ext = bn.split('.')[-1]
        if miss_header:
            df = pd.read_csv(dir_file, header=None,
                             skipfooter=skip_last_n, nrows=nrows)
        else:
            df = pd.read_csv(dir_file, header=skip_top_n,
                             skipfooter=skip_last_n, nrows=nrows)
        if rename_dict:
            try:
                df.rename(columns=rename_dict, inplace=True)
                df = df[rename_dict.values()]
            except:
                print(df.columns)
                print(rename_dict)
                raise IOError
        df['extract_name'] = bn
        if 'sys_name' not in rename_dict.values():
            df['sys_name'] = sys_name
        return df

    def truncate_columns(self, df, cols_trunc, nchar):
        for i, col in enumerate(cols_trunc):
            df[col] = df[col].str[:nchar[i]]
        return df

    def validate_mapping_and_parse_data(self, dir_mapping: str, display_df=False):
        self.df_mapping = pd.read_excel(dir_mapping)
        files_excel = self.files_xlsx + self.files_xls
        files_csv = self.files_csv
        files = files_excel + files_csv

        # read mapping
        for fdir in files:
            fn = os.path.basename(fdir)
            sheet_names = self.df_mapping[self.df_mapping['fileName']
                                          == fn]['sheetName'].unique()
            for sheet_name in sheet_names:

                # get details from mapping and exclude unmapped columns
                try:
                    if pd.notnull(sheet_name):
                        t_df = self.df_mapping[
                            (self.df_mapping['fileName'] == fn) &
                            (self.df_mapping['sheetName'] == sheet_name) &
                            (self.df_mapping['mapToColumnName'].notnull())]
                    else:
                        t_df = self.df_mapping[
                            (self.df_mapping['fileName'] == fn) &
                            (self.df_mapping['mapToColumnName'].notnull())]

                    # get file level parsing requirement
                    t_skip_top = 0 if pd.isnull(
                        t_df['skipTopN'].max()) else int(t_df['skipTopN'].max())
                    t_skip_last = 0 if pd.isnull(
                        t_df['skipLastN'].max()) else int(t_df['skipLastN'].max())
                    t_sys = t_df['systemName'].max()
                    t_old_cols = t_df['columnName'].tolist()
                    t_new_cols = t_df['mapToColumnName'].tolist()
                    t_no_header = True if "Y" in t_df['noHeader'].tolist(
                    ) else False
                    date_idx = np.argwhere(~pd.isnull(
                        t_df['originalDateFormat'].to_numpy())).flatten()
                    t_date_cols = t_df['mapToColumnName'].to_numpy()[
                        date_idx].flatten()
                    t_date_format = t_df['originalDateFormat'].to_numpy()[
                        date_idx].flatten()
                    trunc_idx = np.argwhere(~pd.isnull(
                        t_df['leftNChars'].to_numpy())).flatten()
                    t_trunc_cols = t_df['mapToColumnName'].to_numpy()[
                        trunc_idx].flatten()
                    t_trunc_nchars = t_df['leftNChars'].to_numpy()[
                        trunc_idx].flatten().astype(int)
                except:
                    raise KeyError(f"❌Error occurs when parsing {fn}, "
                                   "Please check if fileName and sheetName are"
                                   " correct in the mapping file!")

                # parse data accordingly
                rename_dict = {k: v for (k, v) in zip(t_old_cols, t_new_cols)}
                if fdir in files_excel:
                    try:
                        df_single = self.parse_excel_worksheet(
                            fdir, sheet_name, t_sys, t_skip_top, t_skip_last, None, rename_dict, t_no_header)
                    except:
                        print(f"❌Error occurs when parsing {fn},"
                              "please check original data and your mapping.")
                elif fdir in files_csv:
                    try:
                        df_single = self.parse_csv_file(
                            fdir, t_sys, t_skip_top, t_skip_last, None, rename_dict, t_no_header)
                    except:
                        print(f"❌Error occurs when parsing {fn},"
                              "please check original data and your mapping.")

                # truncate columns
                try:
                    df_single = self.truncate_columns(
                        df_single, t_trunc_cols, t_trunc_nchars)

                    # convert date to string
                    df_single = self.convert_date_to_string(
                        df_single, t_date_cols, t_date_format)
                except:
                    print(f"❌Error occurs when parsing {fn},"
                          "please check your mapping file (truncate/datetime)")
                try:
                    self.df_out = self.df_out.append(
                        df_single, ignore_index=True)
                except:
                    print(
                        f"File {fn}: Please make sure: \n"
                        "a) There are no duplicated names in 'mapToColumnName' in mapping document"
                        "b) Schema has been imported")
                print(
                    f"File: {str(fn)[:18]+'..':<20} | Sheet: {str(sheet_name)[:10]+'..':<12} | #Rows: {df_single.shape[0]:9} | #Columns: {df_single.shape[1]:3}")

    def convert_date_to_string(self, df, cols_date, cols_date_format):
        """
        convert date to string as per Hadoop requirements
        """
        df = df.copy()
        for col, date_format in zip(cols_date, cols_date_format):
            try:
                df[col] = df[col].dt.strftime(date_format)
            except:
                try:
                    df[col] = pd.to_datetime(
                        df[col], infer_datetime_format=True)
                    df[col] = df[col].dt.strftime(date_format)
                except:
                    df[col] = np.nan
        return df

    def remove_sensitive_chars(self):
        for col in self.df_out.columns:
            if self.df_out[col].dtype == 'O':
                self.df_out[col].fillna('', inplace=True)
                self.df_out[col] = self.df_out[col].str.replace(
                    ',', '', regex=False)
                self.df_out[col] = self.df_out[col].str.replace(
                    '/', '', regex=False)
                self.df_out[col] = self.df_out[col].str.replace(
                    '\\', '', regex=False)
                self.df_out[col] = self.df_out[col].str.replace(
                    '"', '', regex=False)
                self.df_out[col] = self.df_out[col].str.replace(
                    "'", '', regex=False)

    def save(self):
        self.df_out.to_csv(
            os.path.join(
                self.dir_out,
                "user_access_listing_not_cleaned_" + str(self.version) + ".csv"),
            index=False)
