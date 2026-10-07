import tabula
import numpy as np
import pandas as pd


class BankParser:
    def __init__(self, bank_name):
        self.bank_name = bank_name

    def parse(self, pdf_path):
        raise NotImplementedError("This method should be implemented by subclasses.")


class TescoParser(BankParser):
    def __init__(self, pdf_path):
        super().__init__("Tesco", pdf_path)

    def _is_date_string(self, s):
        # Check if the string is in the format 'dd MMM'
        if isinstance(s, str) and len(s) == 6 and s[2] == ' ':
            day = s[:2]
            month = s[3:]
            return day.isdigit() and month.isalpha()
        return False

    def parse(self, pdf_path):
        # Implement Tesco-specific parsing logic here
        dfs = tabula.read_pdf(pdf_path, stream=True, pages='all', pandas_options={'header': None})

        formatted_dfs = []
        for i, df in enumerate(dfs):
            print(f"DataFrame {i}:")
            df = df.dropna(axis=0, thresh=4)
            df = df[(df.iloc[:, 0].apply(self._is_date_string) &
                    df.iloc[:, 1].apply(self._is_date_string))]
            df.iloc[:, 3] = df.iloc[:, 3:-1].replace(np.nan, '').astype('str').agg('-'.join, axis=1)
            df = df.iloc[:, [0, 1, 2, 3, -1]]

            
            df.columns = ['trans_date', 'post_date', 'id', 'description', 'amount']
            df['amount'] = df['amount'].str.replace('£', '').str.replace(',', '').astype(float)
            df = df.dropna(subset=['id'])
            df['id'] = df['id'].astype(int)

            formatted_dfs.append(df)

        return pd.concat(formatted_dfs, ignore_index=True)
