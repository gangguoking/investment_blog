import pandas as pd


def csv_to_excel(csv_filename, excel_filename):
    """

    :param csv_filename:
    :param excel_filename:
    :return:
    """
    df = pd.read_csv(csv_filename)
    df.drop_duplicates("url", inplace=True)
    df = df.drop(df[df['authors'] == 'authors'].index)
    df.set_index(df.columns.to_list()[0], inplace=True)
    df.to_excel(excel_filename)
    df.to_csv(csv_filename)


if __name__ == '__main__':
    csv_to_excel(csv_filename="../download_file/Bloomberg_query.csv",
                 excel_filename="../download_file/Bloomberg_query.xlsx")
