from utils import nunique_per_cat
import pandas as pd

# a utility preprocessor class to preprocess different datasets
class PreprocessMIMIC:

    def __init__(self):
        pass

    def print_info(self, df):
        """
        Print out the information of the dataframe, such as:
        - shape
        - missing values
        - dtypes of objects
        """

        print("Information about the DataFrame")
        print('#' * 25)
        print(f'Shape of the df: {df.shape}')
        print()
        print(f'Missing Values:\n{df.isna().sum()}')
        print()
        print("The number of unique values per 'object' dtype")
        print(sorted(nunique_per_cat(df), key = lambda x: x[1]))
        print()
        df.info()
        print('#' * 25)

    def convert_to_datetime(self, df, cols):
        """
        Convert a list of valid columns into datetime objects
        """
        # convert each col to datetime 
        for col in cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])

    def compute_LOS(self, df, intime_col, outtime_col, prefix, format_length = 'hour'):
        """
        Compute the Length of Stay (hours default)
        """
        df[f'{prefix}_los_hours'] = (df[outtime_col] - df[intime_col]).dt.total_seconds() / 3600


    def map_to_group(self, df, col, mapping, fill_na):
        """
        Perform a mapping of values to new values
        """
        df[f'{col}_grouped'] = df[col].map(mapping).fillna(fill_na)


    def filter_outliers(self, df, col):
        """ 
        Using IQR filtering, constrain the bounds of the distribution of a continuous feature
        by capping values outside the range to the upper and lower bounds.
        """
        assert df[col].dtype in ['int64', 'float64']
        
        # find the Quantiles and compute the IQR
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
    
        # compute the bounds
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
    
        # cap values outside the bounds
        df[col] = df[col].apply(lambda x: lower_bound if x < lower_bound else (upper_bound if x > upper_bound else x))
    
        return df

        
