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
import plotly.express as px
import plotly.graph_objects as go

def boxplot_table_plotly(df, cluster):
    # Filter the data for the specified cluster
    filtered_df = df[df['cluster'] == cluster]
    
    # Sort regions by median value of `restaurantes_ativos`
    medians = filtered_df.groupby('region')['restaurantes_ativos'].median().sort_values()
    sorted_regions = medians.index.tolist()  # List of regions sorted by median
    
    # Create a Plotly boxplot, sorted by median
    fig_boxplot = px.box(
        filtered_df,
        x='region',
        y='restaurantes_ativos',
        category_orders={'region': sorted_regions},  # Custom order for regions
        title='',
        labels={'restaurantes_ativos': 'Restaurantes Ativos (%)', 'region': 'Region'},
        points='all',  # Add individual data points
        hover_data=('region',
                    'chs',
                    'uf',
                    'cidade')
    )
    
    # Add median values as annotations
    for region in sorted_regions:
        median_value = medians[region]
        fig_boxplot.add_annotation(
            x=region,
            y=median_value,
            text=f'{median_value:.1f}',  # Format median as 1 decimal place
            showarrow=False,
            font=dict(size=12, color='black'),
            align='center',
            yshift=10  # Adjust position above the box
        )
    
    # Aggregate data for the table
    aggregation = filtered_df.groupby('region').agg({
        'cidade': 'count',
        'renda_media': 'median'
    }).rename(columns={'cidade': 'Cidades', 'renda_media': 'Renda (R$)'})

    # Transform specific columns to integers
    aggregation = aggregation.astype({'Cidades': 'int', 'Renda (R$)': 'int'})
    
    # Convert the table data into a Plotly Table
    table = go.Figure(data=[
        go.Table(
            header=dict(
                values=['Region', 'Cidades', 'Renda (R$)'],
                fill_color='lightgray',
                align='center',
                font=dict(size=12, color='black')
            ),
            cells=dict(
                values=[
                    aggregation.index, 
                    aggregation['Cidades'], 
                    aggregation['Renda (R$)']
                ],
                fill_color='white',
                align='center',
                font=dict(size=12, color='black')
            )
        )
    ])
    
    # Display both figures
    fig_boxplot.update_layout(height=600, width=800)
    table.update_layout(height=300, width=800)
    
    # Show the boxplot and table
    fig_boxplot.show()
    table.show()