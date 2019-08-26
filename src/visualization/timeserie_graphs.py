### Import packages for dataset visualization. Lets use ploty to create dynamy graph.
import plotly as py
from plotly import graph_objs as go
from plotly.offline import plot, iplot, init_notebook_mode
import plotly.express as px 
from matplotlib import pyplot
import matplotlib.pyplot as plt
### Import packages for time series analysis
from statsmodels.tsa.seasonal import seasonal_decompose

def ts_graph_line(df_daily, TARGET, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily[TARGET], mode="lines", name=TARGET))

    # Edit the layout
    fig.update_layout(title=title,
                       xaxis_title='Day',
                       yaxis_title='Price Close',
    )
    return fig

def violin_plot(df, TARGET, time):
    fig = go.Figure()
    list_time = df[time].unique()

    for t in list_time:
        fig.add_trace(go.Violin(x=df[time][df[time]==t],
                                y=df[TARGET][df[time]==t],
                                name=f"{time}_{str(t)}",
                                box_visible=True,
                                meanline_visible=True))

    fig.update_layout(title=f"Violin Plot of Price Close by {time}",
                       xaxis_title=time,
                       yaxis_title='Price Close',
    )

    fig.show()

def graph_additive_decomposition(df_daily, TARGET):
    #Additive Decomposition
    result_add = seasonal_decompose(df_daily[TARGET], model="additive", extrapolate_trend="freq")

    # Plot
    plt.rcParams.update({'figure.figsize': (10,10)})
    #result_mul.plot().suptitle('Multiplicative Decompose', fontsize=22)
    result_add.plot().suptitle('Additive Decompose', fontsize=22)
    plt.show()

def graph_outliers(df_daily, TARGET):
    #Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily[TARGET], mode="lines", name=TARGET))
    fig.add_trace(go.Scatter(x=df_daily.index, y=df_daily.day_outlier, mode="markers", name="Outliers"))

    # Edit the layout
    fig.update_layout(title=f'BITCOIN TIMESERIE BY DAY - OUTLIERS',
                       xaxis_title='Day',
                       yaxis_title='Price Close',
    )
    return fig

def change_name_columns(string):
    string = string.replace("_lag", "")
    string = string.replace("Close_diff__", "")
    return string

def graph_correlation_features(df_features, lag):
    features_lag  = [i for i in df_features.columns if lag in i]
    df_features_aux = df_features.filter(features_lag)
    df_features_aux.columns = [change_name_columns(string) for string in features_lag]
    fig = px.scatter_matrix(df_features_aux)

    fig.update_layout(
        title=f'Bitcoin Features {lag}',
            xaxis = go.layout.XAxis(
                tickangle=45
        ),
        height=1050

    )
    fig.update_xaxes(tickangle=45)
    return fig
