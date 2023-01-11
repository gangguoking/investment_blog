import pandas as pd


def csv_to_excel(csv_filename, excel_filename):
    """

    :param csv_filename:
    :param excel_filename:
    :return:
    """
    df = pd.read_csv(csv_filename)
    print(df.columns.to_list())
    df.set_index("authors", inplace=True)
    df.to_excel(excel_filename)


if __name__ == '__main__':
    csv_to_excel(csv_filename="../spiders/Bloomberg_query.csv",
                 excel_filename="../spiders/Bloomberg_query.xlsx")
