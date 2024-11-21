import pandas as pd

def compare_csv_with_substring_check(file1_path, file2_path, id_col, compare_col):
    # Load files with ISO-8859-1 encoding to handle special characters
    file1_df = pd.read_csv(file1_path, encoding='ISO-8859-1')
    file2_df = pd.read_csv(file2_path, encoding='ISO-8859-1')

    # Rename columns for consistency
    file1_df.rename(columns={id_col: 'ID', compare_col: 'End use'}, inplace=True)
    file2_df.rename(columns={id_col: 'ID', compare_col: 'End use'}, inplace=True)

    # Merge dataframes on 'ID' column
    merged_df = pd.merge(file1_df[['ID', 'End use']], file2_df[['ID', 'End use']], on='ID', suffixes=('_file1', '_file2'), how='outer')

    # Check if 'End use' in File 1 is a substring of 'End use' in File 2
    merged_df['file1_in_file2'] = merged_df.apply(
        lambda row: row['End use_file1'] in row['End use_file2'] if pd.notnull(row['End use_file1']) and pd.notnull(row['End use_file2']) else False,
        axis=1
    )

    # Summary statistics
    total_rows_file1 = file1_df.shape[0]
    total_rows_file2 = file2_df.shape[0]
    total_common_ids = merged_df['ID'].nunique()
    substring_match_count = merged_df['file1_in_file2'].sum()

    # Retrieve rows where File 1's 'End use' is contained within File 2's 'End use'
    contained_rows = merged_df[merged_df['file1_in_file2'] == True]

    # Summary of results
    summary = {
        "Total rows in File 1": total_rows_file1,
        "Total rows in File 2": total_rows_file2,
        "Total common IDs": total_common_ids,
        "Substring match count": substring_match_count,
    }

    return summary, contained_rows

# Example usage
file1_path = 'final_extracted_uses_111124.csv'
file2_path = 'EndUseExtract (Complete) - Copy.csv'
summary, substring_matches = compare_csv_with_substring_check(file1_path, file2_path, 'Assessment ID', 'Extracted use')

# Display the summary and the matching rows
print(summary)
print(substring_matches)