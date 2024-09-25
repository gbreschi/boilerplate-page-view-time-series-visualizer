import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# 1. Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=["date"])

# 2. Clean the data by filtering out the top 2.5% and bottom 2.5%
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]




# 3. Function to draw the line plot
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


# 4. Function to draw the bar plot
def draw_bar_plot():
    # Copy and modify data for the bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Pivot the data for the bar plot
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Plot the bar chart
    fig = df_bar.plot(kind='bar', figsize=(10, 6)).figure
    plt.title('Average Daily Page Views per Month')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', labels=['January', 'February', 'March', 
    'April', 'May', 'June', 'July', 'August', 'September', 
    'October', 'November', 'December'])
    
    # Save and return the image
    fig.savefig('bar_plot.png')
    return fig



# 5. Function to draw the box plot# 5. Function to draw the box plot
def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')  # Use abbreviated month names

    # Ensure the 'value' column is numeric
    df_box['value'] = pd.to_numeric(df_box['value'], errors='coerce')

    # Sort by month order for the box plot
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')

    # Create the box plot figure
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    # Year-wise Box Plot (Trend)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise Box Plot (Seasonality)
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save and return the image
    fig.savefig('box_plot.png')
    return fig
