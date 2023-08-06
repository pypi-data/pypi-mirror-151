import pandas as pd


def remove_additional_comma(fn, exp=10):
    exp_no_cols = exp
    with open(fn, 'r') as f:
        old_lines = f.readlines()
        new_lines = []
        count = 0
        for line in old_lines:
            act_no_col = line.count(',') + 1
            no_comma_rmv = act_no_col - exp_no_cols
            if no_comma_rmv > 0:
                new_lines.append(line.split('\n')[0].rstrip(',') + '\n')
            else:
                new_lines.append(line)
            count += 1

    with open(fn, 'w') as f:
        for line in new_lines:
            f.write(line)


def count_lines_and_records(file_name, sep):
    """Count number of lines in a given file"""
    line_cnt = 0
    cont_cnt = 0
    sep_pos = []
    with open(file_name, 'r') as f:

        for i, line in enumerate(f):
            line_cnt += 1
            if line == sep:
                cont_cnt += 1
                sep_pos.append(i)
    print(f'Number of Lines: {line_cnt}\nNumber of Records: {cont_cnt}')
    return line_cnt, cont_cnt, sep_pos


def normalise_db_export(file_name_data, file_name_req_col, sep_pos):

    # Load required data fields
    req_col = []
    with open(file_name_req_col, 'r') as f:
        for line in f:
            req_col.append(line.replace('\n', ''))

    # Initialise variables for loop
    data_dict = dict()
    lines = ''
    stt_pos = 0

    # Read data export and extract key data
    with open(file_name_data, 'r') as f:

        # Convert text to list
        lines = f.readlines()
        for i, pos in enumerate(sep_pos):

            # Get contract block
            text_block = lines[stt_pos:pos]

            # Parse contract block
            for j, line in enumerate(text_block):
                if ':' in line:
                    loc = line.find(':')
                    k = line[:loc].replace(',', '|').replace("'", '')
                    v = line[loc + 1:].replace("'", '').replace(
                        '\n', '').replace(',', '|').replace('\x00', '|').strip()
                    if k in req_col:
                        data_dict[(i, j)] = (k, v)
                        # print(k,v)

            # Reset start position for next block
            stt_pos = pos + 1

    # Create an empty dateframe to store dict data
    df = pd.DataFrame({'record_index': pd.Series([], dtype='int'),
                       'line_index': pd.Series([], dtype='int'),
                       'column_name': pd.Series([], dtype='str'),
                       'value': pd.Series([], dtype='str')})
    for (k_cont, k_rec), (k_col, v) in data_dict.items():
        df.loc[df.shape[0]] = (k_cont, k_rec, k_col, v)
    df = df.drop(columns=['line_index'])
    return df
