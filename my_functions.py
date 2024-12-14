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