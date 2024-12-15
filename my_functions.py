### Function to easily plot scatter for variables
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns

def plot_scatter(data, x, y, hue):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=data, x=x, y=y, hue=hue, palette='tab10')
    plt.title(f'Relação entre {x} e {y}')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.legend(title=hue, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()  # Adjust layout to fit legend
    plt.show()

### Function to easily plot histogram for variables
def plot_hist(df, x):
    # Create a figure with a single subplot
    fig = plt.figure(figsize=(20,8))
    gs = GridSpec(2,3)

    # Get the axes object using add_subplot and then call the hist method on it
    ax = fig.add_subplot(gs[0,0])
    ax.hist(df[x], bins=30, color='skyblue', edgecolor='black') # Use ax.hist

    plt.xlabel('')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of {x}')
    plt.grid(axis='y', alpha=0.75)
    plt.show()

### Function to describe dataframe and check for outliers
def check_outliers(data):
    df_describe = data.describe().T.round(1)
    df_describe["IQR"] = df_describe["75%"] - df_describe["25%"] # defining IQR
    df_describe["BotOutlier"] = df_describe["25%"] - 1.5*df_describe["IQR"] # determining cutoff for Bottom outliers
    df_describe["TopOutlier"] = df_describe["75%"] + 1.5*df_describe["IQR"] # determining cutoff for Top outliers
    df_describe['CheckBotOut'] = df_describe.apply(lambda row: 'Yes' if row['min'] < row["BotOutlier"] else 'No', axis=1) # mark for possible Bottom outliers
    df_describe['CheckTopOut'] = df_describe.apply(lambda row: 'Yes' if row['max'] > row["TopOutlier"] else 'No', axis=1) # mark for possible Top outliers
    return df_describe

### Function to easily compare boxplot of restauantes_ativos by region and tabel of renda_media
def boxplot_table(df, cluster):

    # Define the figure and GridSpec layout
    fig = plt.figure(figsize=(14, 8))
    gs = GridSpec(2, 2, width_ratios=[3, 1], height_ratios=[3, 1], wspace=0.4, hspace=0.4)

    # Boxplot in the lower-left section
    ax_boxplot = fig.add_subplot(gs[:, 0])  # Occupies both rows in the first column
    category_order = df[df['cluster'] == cluster].groupby('region')['restaurantes_ativos'].median().sort_values().index
    sns.boxplot(
        x='region',
        y='restaurantes_ativos',
        data=df[df['cluster'] == cluster],
        order=category_order,
        ax=ax_boxplot
    )
    ax_boxplot.set_title('restaurantes_ativos distribution per region level')
    ax_boxplot.set_xlabel('')
    ax_boxplot.set_ylabel('Restaurantes_ativos (%)')

    # Add median values as text annotations
    medians = df[df['cluster'] == cluster].groupby('region')['restaurantes_ativos'].median()
    for i, region in enumerate(category_order):
        median = medians[region]
        ax_boxplot.text(
            i, median, f'{median:.1f}',
            ha='center', va='bottom', color='black', fontsize=10, weight='bold'
        )

    # Aggregated table in the upper-right section
    ax_table = fig.add_subplot(gs[0, 1])  # Upper-right quarter
    aggregation = df[df['cluster'] == cluster].groupby('region').agg({
        'cidade': 'count',
        'renda_media': 'median'
    }).rename(columns={'cidade':'cidades', 'renda_media':'renda (R$)'})
    aggregation = aggregation.reindex(category_order).astype({'cidades': 'int', 'renda (R$)': 'int'})


    # Hide the axes for the table and add the data
    ax_table.axis('tight')
    ax_table.axis('off')
    table = ax_table.table(
        cellText=aggregation.values,
        colLabels=aggregation.columns,
        rowLabels=aggregation.index,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(aggregation.columns) + 1)))

    plt.show()