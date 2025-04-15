# Import packages
from dash import (
    Dash,
    html,
    dash_table,
    dcc,
    Input,
    Output,
    callback,
)
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("AB_NYC_2019_cleaned.csv")
numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(include="object").columns.tolist()

# Initialize app
app = Dash(__name__)
server = app.server

# App layout
app.layout = html.Div(
    style={
        "fontFamily": "Segoe UI, sans-serif",
        "backgroundColor": "black",
        "color": "#f5f6fa",
        "padding": "30px",
    },
    children=[
        html.H1(
            "Airbnb Listings Analysis – NYC 2019",
            style={
                "textAlign": "center",
                "color": "#f5f6fa",
                "marginBottom": "10px",
                "fontSize": "36px",
            },
        ),
        html.P(
            "Interactive Dashboard: Analyze neighborhood trends, room types, and pricing of NYC Airbnb listings.",
            style={
                "textAlign": "center",
                "maxWidth": "900px",
                "margin": "0 auto 30px auto",
                "color": "#dcdde1",
                "fontSize": "18px",
            },
        ),
        html.Div(
            style={
                "backgroundColor": "#1e1e1e",
                "padding": "30px",
                "borderRadius": "12px",
                "boxShadow": "0 4px 12px rgba(255,255,255,0.1)",
                "maxWidth": "1100px",
                "margin": "auto",
            },
            children=[
                html.Label(
                    "🔢 Enter Column Name for numerical univariate analysis:",
                    style={"fontWeight": "bold", "color": "#f5f6fa"},
                ),
                dcc.RadioItems(
                    id="input",
                    options=[{"label": col, "value": col} for col in numeric_cols],
                    value=numeric_cols[0],
                    labelStyle={"display": "inline-block", "marginRight": "15px"},
                    style={"marginBottom": "20px", "color": "#f5f6fa"},
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "justifyContent": "space-between",
                        "gap": "30px",
                    },
                    children=[
                        html.Div(id="histo", style={"flex": "1", "minWidth": "300px"}),
                        html.Div(id="box", style={"flex": "1", "minWidth": "300px"}),
                    ],
                ),
                html.Div(
                    id="stats",
                    style={
                        "marginTop": "40px",
                        "textAlign": "center",
                    },
                ),
                html.Hr(style={"margin": "40px 0", "borderColor": "#444"}),
                html.Label(
                    "🎯 Enter Column Name for categorical univariate analysis:",
                    style={"fontWeight": "bold", "color": "#f5f6fa"},
                ),
                dcc.RadioItems(
                    id="input2",
                    options=[{"label": col, "value": col} for col in categorical_cols],
                    value=categorical_cols[0],
                    labelStyle={"display": "inline-block", "marginRight": "15px"},
                    style={"marginBottom": "20px", "color": "#f5f6fa"},
                ),
                html.Div(id="barpie", style={"flex": "1", "minWidth": "300px"}),
                html.Hr(style={"margin": "40px 0", "borderColor": "#444"}),
                html.Label(
                    "📊 Categorical vs Numerical Analysis:",
                    style={
                        "fontWeight": "bold",
                        "color": "#f5f6fa",
                        "fontSize": "20px",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    "🗂️ Select Categorical Column:",
                                    style={"color": "#f5f6fa", "marginBottom": "5px"},
                                ),
                                dcc.Dropdown(
                                    id="cat_col",
                                    options=[
                                        {"label": col, "value": col}
                                        for col in categorical_cols
                                    ],
                                    value=categorical_cols[0],
                                    style={
                                        "backgroundColor": "#1E1E1E",
                                        "color": "black",
                                        "borderRadius": "8px",
                                        "padding": "6px",
                                        "fontWeight": "bold",
                                    },
                                ),
                            ],
                            style={
                                "width": "30%",
                                "display": "inline-block",
                                "marginRight": "3%",
                            },
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "🔢 Select Numerical Column:",
                                    style={"color": "#f5f6fa", "marginBottom": "5px"},
                                ),
                                dcc.Dropdown(
                                    id="num_col",
                                    options=[
                                        {"label": col, "value": col}
                                        for col in numeric_cols
                                    ],
                                    value=numeric_cols[0],
                                    style={
                                        "backgroundColor": "#1E1E1E",
                                        "color": "black",
                                        "borderRadius": "8px",
                                        "padding": "6px",
                                        "fontWeight": "bold",
                                    },
                                ),
                            ],
                            style={
                                "width": "30%",
                                "display": "inline-block",
                                "marginRight": "3%",
                            },
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "🧮 Select Aggregation Function:",
                                    style={"color": "#f5f6fa", "marginBottom": "5px"},
                                ),
                                dcc.Dropdown(
                                    id="func",
                                    options=[
                                        {"label": func, "value": func}
                                        for func in [
                                            "mean",
                                            "max",
                                            "min",
                                            "median",
                                            "sum",
                                        ]
                                    ],
                                    value="mean",
                                    style={
                                        "backgroundColor": "#1E1E1E",
                                        "color": "black",
                                        "borderRadius": "8px",
                                        "padding": "6px",
                                        "fontWeight": "bold",
                                    },
                                ),
                            ],
                            style={"width": "30%", "display": "inline-block"},
                        ),
                    ],
                    style={
                        "marginBottom": "30px",
                        "padding": "20px",
                        "backgroundColor": "#1e1e1e",
                        "borderRadius": "12px",
                        "boxShadow": "0 4px 12px rgba(255,255,255,0.05)",
                    },
                ),
                html.Div(
                    id="catnum_output",
                    style={
                        "display": "flex",
                        "flexWrap": "wrap",
                        "gap": "30px",
                        "justifyContent": "center",
                    },
                ),
            ],
        ),
    ],
)


# Callback for numerical column
@callback(
    Output("stats", "children"),
    Output("histo", "children"),
    Output("box", "children"),
    Input("input", "value"),
)
def num_uni(col, data=df):
    if col not in data.columns or not pd.api.types.is_numeric_dtype(data[col]):
        return (
            html.Div(
                f"⚠️ '{col}' is not a valid numeric column.", style={"color": "red"}
            ),
            html.Div(),
            html.Div(),
        )

    histo = px.histogram(
        data_frame=data,
        x=col,
        color_discrete_sequence=["#8e44ad"],
        title=f"📊 Distribution of {col.capitalize()}",
        template="plotly_dark",
    )
    histo.update_layout(
        title_font=dict(size=20, color="#f5f6fa"),
        xaxis_title=col.capitalize(),
        yaxis_title="Count",
        xaxis_tickangle=45,
    )

    box = px.box(
        data_frame=data,
        y=col,
        color_discrete_sequence=["#16a085"],
        title=f"📦 Box Plot of {col.capitalize()}",
        template="plotly_dark",
    )
    box.update_layout(
        title_font=dict(size=20, color="#f5f6fa"),
        yaxis_title=col.capitalize(),
    )

    stats_df = data[col].describe().reset_index()
    stats_df.columns = ["Statistic", "Value"]
    stats_df["Value"] = stats_df["Value"].apply(lambda x: f"{x:.2f}")

    stats_table = dash_table.DataTable(
        data=stats_df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in stats_df.columns],
        style_table={"margin": "auto", "width": "60%"},
        style_cell={
            "textAlign": "center",
            "padding": "8px",
            "fontFamily": "Segoe UI",
            "backgroundColor": "#2f3640",
            "color": "#f5f6fa",
            "border": "1px solid #444",
        },
        style_header={
            "backgroundColor": "#353b48",
            "color": "white",
            "fontWeight": "bold",
            "border": "1px solid #444",
        },
    )

    return stats_table, dcc.Graph(figure=histo), dcc.Graph(figure=box)


# Callback for categorical column
@callback(Output("barpie", "children"), Input("input2", "value"))
def cat_uni(col):
    if col not in df.columns:
        return html.Div(f"⚠️ Column '{col}' not found.", style={"color": "red"})

    if df[col].nunique() < 5:
        counts = df[col].value_counts()
        fig = px.pie(
            names=counts.index,
            values=counts.values,
            title=f"🥧 Pie Chart of {col.capitalize()}",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            template="plotly_dark",
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
    else:
        counts = df[col].value_counts().nlargest(10)
        fig = px.bar(
            x=counts.index,
            y=counts.values,
            title=f"📈 Top 10 {col.capitalize()} (Categorical)",
            color=counts.index,
            color_discrete_sequence=px.colors.qualitative.Set3,
            labels={"x": col.capitalize(), "y": "Count"},
            template="plotly_dark",
        )
        fig.update_layout(
            xaxis_tickangle=45,
            title_font=dict(size=20, color="#f5f6fa"),
        )

    return dcc.Graph(figure=fig)


@callback(
    Output("catnum_output", "children"),
    Input("cat_col", "value"),
    Input("num_col", "value"),
    Input("func", "value"),
)
def cat_vs_num(cat, num, func):
    table = df.groupby(cat)[num].agg(["mean", "max", "min", "median", "sum"])

    # Box plot 🎁
    box = px.box(
        data_frame=df,
        y=num,
        x=cat,
        color=cat,
        title=f"Box Plot of {num} by {cat} 📦",
        template="plotly_dark",
    )
    box.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white", size=14),
        title_font=dict(size=20),
    )
    box.update_xaxes(title=f"{cat} 🏷️", tickangle=45, showgrid=False)
    box.update_yaxes(title=f"{num} 📊", showgrid=True)

    # Bar plot 🧱
    bar = px.bar(
        data_frame=table,
        y=table[func],
        x=table.index,
        color=table.index,
        title=f"{func.capitalize()} of {num} by {cat} 📈",
        template="plotly_dark",
    )
    bar.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white", size=14),
        title_font=dict(size=20),
        showlegend=False,
    )
    bar.update_xaxes(title=f"{cat} 🏷️", tickangle=45, showgrid=False)
    bar.update_yaxes(title=f"{func.capitalize()} {num} 💡", showgrid=True)

    return dcc.Graph(figure=box), dcc.Graph(figure=bar)
if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8080)


# Run app
if __name__ == "__main__":
    app.run()
