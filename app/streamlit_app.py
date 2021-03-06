from numpy import empty
import streamlit as st
import pandas as pd
from pandas.core.frame import DataFrame
import altair as alt
from datetime import datetime
# custom package
from src import Dataset, DateColumn, TextColumn, NumericColumn


def main():
    """
    Main function to run the whole program.

    Parameters
    ----------
    None

    Returns
    -------
    The main application contains 4 sections:
        1. Overall Information
        2. Numeric Columns Information
        3. Text Columns Information
        4. Datetime Columns Information
    """
    # Display title of the application
    st.title('Data Explorer Web App')

    # Upload CSV file and load data as Pandas dataframe
    dataset = file_upload()
    if dataset is not None:
        df = read_csv(dataset)

        # 1. Display Overall Information
        overall_info(df, dataset)

        # 2. Numeric Columns Information
        numeric_column(df)

        # 3. Text Columns Information
        text_column(df)

        # 4. Datetime Columns Information
        datetime_column(df)
    else:
        project_description()


def file_upload():
    """
    Display file uploader.
    """
    dataset = st.file_uploader("Choose a CSV file", type="csv")
    return dataset


def read_csv(dataset) -> pd.DataFrame:
    """
    Display read csv file.

    Parameters
    ----------
    dataset: streamlit.uploaded_file_manager.UploadedFile
    The dataset to be read.

    Returns
    -------
    pd.DataFrame
    """
    df = pd.read_csv(dataset)
    df.columns = df.columns.str.replace(' ','_') # replace the column has space with '_'
    return df


def project_description() -> None:
    """
    Display project description when first entering the application.

    Parameters
    ----------
    None

    Returns
    -------
    Description of the project.
    """
    st.markdown('### 🛠️ **Description**')
    st.info('In this project, our group will develop an interactive web application using Streamlit that will read a provided CSV file by the user and perform some exploratory data analysis on it. The web application needs to be containerised with Docker and will be running using python 3.8.2.')
    st.markdown('### 👤 **Authors**')
    st.markdown('* [Leah Nguyen](https://github.com/ndleah)')
    st.markdown('* [Cartier Zhi](https://github.com/cartierz)')
    st.markdown('* [Jia Ping Cai](https://github.com/caijiaping)')
    st.markdown('* [Laura Sofia Bayona](https://github.com/Laurabayonaf)')


def overall_info(df, dataset) -> None:
    """
    Display overall information about the dataset.

    Parameters
    ----------
    dataset: streamlit.uploaded_file_manager.UploadedFile
    The dataset to be read.

    df: pd.DataFrame
    The dataframe to be displayed.

    Returns
    -------
    Display contents for the overall information section.
    """
    # Display header called “Overall Information”
    st.header('1. Overall Information')

    # instantiate class object
    gen_info = Dataset(df, dataset.name)
    date_column_num = 0

    # Display filename
    df_name = gen_info.get_name()
    st.markdown(f'**Name of Table:** {df_name}')

    # Display number of rows 
    df_rows = gen_info.get_n_rows()
    st.markdown(f'**Number of Rows:** {df_rows}')

    # Display number of columns
    df_col = gen_info.get_n_cols() # get number of columns
    st.markdown(f'**Number of Columns:** {df_col}')
    
    # Display number of duplicated rows
    df_duplicate_rows = gen_info.get_n_duplicates()
    st.markdown(f'**Number of Duplicated Rows:** {df_duplicate_rows}')

    # Display number of rows with missing values
    df_missing_rows = gen_info.get_n_missing()
    st.markdown(f'**Number of Rows with Missing Values:** {df_missing_rows}')

    # Display list of columns and their data type (text, numeric, date)
    # Display list of columns
    df_col_list = str(gen_info.get_cols_list()).replace('[','').replace(']','').replace("'","")
    st.markdown(f'**List of Columns:**')
    st.write(df_col_list)

    # Display columns data type
    df_col_type = pd.DataFrame([gen_info.get_cols_dtype()]).transpose() # get columns data types
    st.markdown(f'**Type of Columns:**')
    st.dataframe(df_col_type)

    # Display slider for selecting the number of rows to be displayed 
    st.markdown(f'**Display slider for selecting the number of rows to be displayed**')
    df_slider = st.slider("Select the number of rows to be displayed",5,df_rows,5)

    # Display top N rows (default 5 rows) of dataset
    st.markdown('**Top Rows of Table**')
    st.dataframe(gen_info.get_head(df_slider))

    # Display bottom N rows (default 5 rows) of dataset
    st.markdown('**Bottom Rows of Table**')
    st.dataframe(gen_info.get_tail(df_slider))

    # Display N randomly sampled rows (default 5 rows) of dataset
    st.markdown('**Random Sample Rows of Table**')
    st.dataframe(gen_info.get_sample(df_slider))

    # Display a multi select box for choosing which text columns will be converted to datetime
    st.markdown('**Which columns do you want to convert to dates**')
    df_selectbox = st.multiselect("Please select columns:", gen_info.get_text_columns())
    df[df_selectbox] = df[df_selectbox].apply(lambda col: pd.to_datetime(col, errors='ignore'))
    if df_selectbox:
        df_datetime = df[df.columns.intersection(df_selectbox)]
        for datetime_column in df_datetime.columns:
            if df_datetime[datetime_column].dtypes != 'datetime64[ns]':
                st.markdown(f'**1.{date_column_num} Field Name: _{datetime_column.capitalize()}_**')
                st.error('Column is not under Datetime format or mixed with other data types.')
                date_column_num = date_column_num + 1
            else:
                st.markdown(f'**1.{date_column_num} Field Name: _{datetime_column.capitalize()}_**')
                st.success('The Column has successfully converted to Datetime format.')
                date_column_num = date_column_num + 1


def numeric_column(df) -> None:
    """
    Display numeric columns infomation of the dataset.

    Parameters
    ----------
    df: pd.DataFrame
    The dataframe to be displayed.

    Returns
    -------
    Display contents for the numeric column information section.
    """ 
    st.header('2. Information on numeric columns')

    # create dataframe with only numeric data only 
    df_numeric  = df.select_dtypes(include=['float64', 'int64'])

    # instantiate class object
    numeric = NumericColumn()
    column_num = 0

    if df_numeric.empty == True:
        st.warning('**No numeric columns found in the dataset.**')
    else: 
        for (columnName, columnData) in df_numeric.iteritems():
            numeric.get_data(columnName, columnData)
            column_name = numeric.get_name()

            # Display name of column as subtitle
            st.markdown(f'**2.{column_num} Field Name:** **_{column_name}_**')
            column_num = column_num + 1

            # Display number of unique values
            unique_values = numeric.get_unique()

            # Display number of missing values
            missing_values = numeric.get_missing()

            # Display number of occurrence of 0 value
            occurence_0 = numeric.get_zeros()

            # Display number of negative value
            negative_value = numeric.get_negatives()

            # Display the average value
            avg_value = numeric.get_mean()

            # Display the standard deviation value
            std_value = numeric.get_std()

            # Display the minimum value
            min_value = numeric.get_min()

            # Display the maximum value
            max_value = numeric.get_max()

            # Display the median value
            median_value = numeric.get_median()

            # Create a dataFrame for displaying in the Web App
            value = {'value':pd.Series([unique_values,missing_values,occurence_0,negative_value,avg_value,std_value,min_value,max_value,median_value], 
            index = ['Number of Unique Values:','Number of Missing Values:','Number of Rows with 0:','Number of Rows with Negative Values:',
            'Average Values:','Standard Deviation Values:','Minimum Value', 'Maximum Value','Median Value'])}
            
            df_value = pd.DataFrame(value)
            st.write(df_value)

            # Plot bar chat and display in Web App
            st.markdown('**Histogram**')
            st.altair_chart(numeric.get_histogram())

            # Create a frequent table and display in WebApp
            st.markdown('**Most Frequent Values**')
            frequent = numeric.get_frequent()
            st.write(frequent)


def text_column(df) -> None:
    """
    Display text columns infomation of the dataset.

    Parameters
    ----------
    df: pd.DataFrame
    The dataframe to be displayed.

    Returns
    -------
    Display contents for the text column information section.
    """
    st.header('3. Information on text columns')

    # create dataframe with only text data only 
    df_text  = df.select_dtypes(include=['object'])

    # instantiate class object
    text = TextColumn()
    column_num = 0

    if df_text.empty == True:
        st.warning('**No text columns found in the dataset.**')    
    else:
        for (columnName, columnData) in df_text.iteritems():
            text.get_data(columnName, columnData)
            column_name = text.get_name()

            # Display name of column as subtitle
            st.markdown(f'**3.{column_num} Field Name:** **_{column_name}_**')
            column_num = column_num + 1

            # Display number of unique value
            unique = text.get_unique()
                
            # Display number of missing values
            missing = text.get_missing()
                
            # Display number of rows with empty string
            empty = text.get_empty()
                
            # Display number of only whitespaces
            whitespaces = text.get_whitespace()
                    
            # Display number of only lower case characters
            lower = text.get_lowercase()
                
            # Display number of only upper case characters
            upper = text.get_uppercase()
                
            # Display number of only alphabet characters
            alp = text.get_alphabet()
                
            # Display number of only digital characters
            digital = text.get_digit()
                
            # Display the mode value
            mode_value = text.get_mode()
                
            # Create a dataFrame for displaying in the Web App
            value = {'value':pd.Series([unique,missing,empty, whitespaces, lower, upper, alp, digital,mode_value[0]], index = ['Number of Unique Values:', 'Number of Rows with Missing Values:',
                        'Number of Empty Rows:', 'Number of Rows with Only Whitespace:', 'Number of Rows with Only Lowercases:', 'Number of Rows with Only Uppercases:', 'Number of Rows with Only Alphabet:','Number of Rows with Only Digits:','Mode Value'])}
            df_value = pd.DataFrame(value)
            st.write(df_value)
                
            # Plot bar chat and display in Web App
            st.markdown('**Bar Chat**')
            st.altair_chart(text.get_barchart())

            # Create a frequent table and display in WebApp
            st.markdown('**Most Frequent Values**')
            frequent = text.get_frequent()
            st.write(frequent)


def datetime_column(df) -> None:
    """
    Display text columns infomation of the dataset.

    Parameters
    ----------
    df: pd.DataFrame
    The dataframe to be displayed.

    Returns
    -------
    Display contents for the datetime column information section.
    """
    st.header('4. Information on datetime columns')

    # instantiate class object
    datecol_object = DateColumn()
    date_column_num = 0
        
    # create dataframe with only datetime data
    datetime_col = df.select_dtypes(include = ["datetime64"])

    if datetime_col.empty == True:
        st.warning('**No datetime columns found in the dataset.**')    
    else:
        for (columnName, columnData) in datetime_col.iteritems(): 
            datecol_object.get_data(columnName, columnData)
            column_name = datecol_object.get_name()

            # Display name of column as subtitle
            st.markdown(f"**4.{date_column_num} Field Name: _{column_name}_**") 
            date_column_num = date_column_num + 1   

            # Applying methods
            uniquedate = datecol_object.get_unique()
            missingdate = datecol_object.get_missing()
            weekenddate = datecol_object.get_weekend()
            weekdaydate =datecol_object.get_weekday()
            futuredate = datecol_object.get_future()
            empty1900date = datecol_object.get_empty_1900()
            empty1970date = datecol_object.get_empty_1970()
            mindate = datecol_object.get_min()
            maxdate = datecol_object.get_max()

            datetime_sum = { "" : ["Number of Unique Values", 
                                "Number of Rows with Missing Values", 
                                "Number of Weekend Dates", 
                                "Number of Weekday Dates", 
                                "Number of Dates in Future", 
                                "Number of Rows with 1900-01-01", 
                                "Number of Rows with 1970-01-01", 
                                "Minimum Value", 
                                "Maximum Value"], 
                                "Value" : [uniquedate, 
                                missingdate, 
                                weekenddate, 
                                weekdaydate, 
                                futuredate, 
                                empty1900date, 
                                empty1970date, 
                                mindate, 
                                maxdate
                                ]
                                }
                        
            display_sumdate = pd.DataFrame(datetime_sum)
            st.dataframe(display_sumdate)

            # bar chart
            st.markdown("**DateTime Bar Chart Frequencies**")
            st.altair_chart(datecol_object.get_barchart())

            # create frequency table
            st.markdown('**Most Frequent DateTime Values**')
            frequencies = datecol_object.get_frequent()
            st.write(frequencies)

if __name__ == '__main__':
    main()