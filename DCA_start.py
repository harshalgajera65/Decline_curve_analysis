# Norne Field(North Sea)

import pandas
import matplotlib.pyplot as plt

data_file = "data.csv"
data = pandas.read_csv(data_file)
print(data.head())

# next step we convert date to python datetim

data["Date"] = pandas.to_datetime(data["Date"], format='%d-%m-%Y')

# dataframe columns must be named as ‘ds’ for time and ‘y’ for flowrate.
data.columns = ['ds', 'y']


# plotting the data
plt.figure(figsize=(12, 6))
plt.plot(data.ds, data.y)
plt.title('Production Rate  ', size=20, pad=15)
plt.xlabel('Days')
plt.ylabel('Rate (SCF/d)')
plt.show()

# Removing the outliers using the following function


def remove_outlier(dataframe, column_name, window, number_of_stdevs_away_from_mean, trim=False):
    """
    Removing outlier of production data and trim initial buildup

    INPUT:
    data: Production dataframe
    column_name: Column name of production rate
    window: Rolling average window
    number_of_stdevs_away_from_mean: Distance from standard dev. where outliers will be removed
    trim: Option to trim initial buildup (Because buildup is an outlier). Default is False.

    OUTPUT:
    data: New dataframe where outliers have been removed
    """

    # Creating a rolling average allows you to “smooth” out small fluctuations in datasets
    dataframe[column_name + '_rol_Av'] = dataframe[column_name].rolling(window=window, center=True).mean()
    dataframe[column_name + '_rol_Std'] = dataframe[column_name].rolling(window=window, center=True).std()

    # Detect anomalies by determining how far away from the mean (in terms of standard deviation)
    dataframe[column_name + '_is_Outlier'] = (abs(dataframe[column_name] - dataframe[column_name + '_rol_Av']) >
                                              (number_of_stdevs_away_from_mean * dataframe[column_name + '_rol_Std']))

    """outlier and not-outlier will be recorded in the '_is_Outlier' column as 'True' and 'False'. Now, outlier is 
    removed, so column that contains 'True' values are masked out"""

    # drop removes conditional data values here in our case will remove the entry for which Outlier is True
    # Drop return dataframe after removing some conditional datapoints

    result = dataframe.drop(dataframe[dataframe[column_name + '_is_Outlier'] == True].index).reset_index(drop=True)

    # Identify the rows where "_rol_Av" has NaNs
    result = result[result[column_name + '_rol_Av'].notna()]

    if trim:
        # Trim initial buildup
        maxi = result[column_name + '_rol_Av'].max()
        maxi_index = (result[result[column_name + '_rol_Av'] == maxi].index.values)[0]
        result = result.iloc[maxi_index:, :].reset_index(drop=True)

    return result


new_data = remove_outlier(data, "y", 10, 10, trim=False)

print(new_data.head())

# plotting the new data without outliers
plt.figure(figsize=(12, 6))
plt.plot(data.ds, data.y_rol_Av)
plt.title('Production Rate ', size=20, pad=15)
plt.xlabel('Days')
plt.ylabel('Rate (SCF/d)')
plt.show()
