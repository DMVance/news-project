import json
import plotly
import os
import json
import calmap
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt, mpld3

# FILE_PATH = os.path.join("news_app", "static", "data", "headlines_scores_keywords.csv")

def article_vs_headline_plot(df):
    # Read in data
    # df = pd.read_csv(FILE_PATH)

    scores_no_zeros = df[["headline_score", "article_score", "news_desk"]].loc[(df["headline_score"] != 0) & (df["article_score"] != 0) & (df["section_name"] == "U.S.")]
    # ['National' 'Business' 'Politics' 'Science' 'Climate']
    
    # Marker fill colors with 50% opacity
    desk_colors_dict = { 
        "National": "rgba(30, 144, 255, 0.1)", #"dodgerblue",
        "Business": "rgba(255, 215, 0, 0.3)", #"gold",
        "Politics": "rgba(178, 34, 34, 0.3)", #"firebrick",
        "Science": "rgba(34, 139, 34, 0.3)", #"forestgreen",
        "Climate": "rgba(255, 140, 0, 0.3)", #"darkorange"
    }
    desk_colors = scores_no_zeros["news_desk"].map(desk_colors_dict)

    trace1 = {
        "x": scores_no_zeros["headline_score"],
        "y": scores_no_zeros["article_score"],
        "mode": "markers",
        "marker": {
            "color": desk_colors,
            "line": {
                "color": "rgba(105, 105, 105, .5)", #dimgrey
                "width": .5,
            }
        },
    }

    plot_data = [trace1,]
    plot_layout = {
        "title": "Articles vs Headlines"}

    data = json.dumps(plot_data, cls=plotly.utils.PlotlyJSONEncoder)
    layout = json.dumps(plot_layout, cls=plotly.utils.PlotlyJSONEncoder)

    return data, layout

def calendar_heatmap():
    
    cal_heatmap_df = pd.read_csv(os.path.join("news_app", "static", "data", "calendar_heatmap_new.csv"))

    cal_heatmap_df["date"] = cal_heatmap_df["date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    cal_heatmap_df["top_headlines"] = cal_heatmap_df["top_headlines"].apply(lambda x: eval(x))

    df2015 = cal_heatmap_df.loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2015)]
    df2016 = cal_heatmap_df.loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2016)]
    df2017 = cal_heatmap_df.loc[cal_heatmap_df["date"].apply(lambda dt: dt.year == 2017)]

    color_scale = [
        [0, "darkred"],
        [.1, "darkred"],
        [.1, "firebrick"],
        [.2, "firebrick"],
        [.2, "indianred"],
        [.3, "indianred"],
        [.3, "lightcoral"],
        [.4, "lightcoral"],
        [.4, "mistyrose"],
        [.475, "mistyrose"],
        [.475, "white"],
        [.525, "white"],
        [.525, "honeydew"],
        [.6, "honeydew"],
        [.6, "palegreen"],
        [.7, "palegreen"],
        [.7, "limegreen"],
        [.8, "limegreen"],
        [.8, "forestgreen"],
        [.9, "forestgreen"],
        [.9, "darkgreen"],
        [1, "darkgreen"],
    ]

    trace2015 = {
        "z": df2015["avg_score"],
        "x": df2015["date"],
        "y": df2015["news_desk"],
        "type": "heatmap",
        "colorscale": color_scale,
        "showscale": True,
        "text": df2015["top_headlines"],
        "hovertemplate": '<b>Most emotional %{y} headlines for %{x}</b>:' +
            '<br>%{text.score[0]} | %{text.headline[0]}' +
            '<br>%{text.score[1]} | %{text.headline[1]}' +
            '<br>%{text.score[2]} | %{text.headline[2]}' +
            "<br><b>Today's Average: %{z}</b>", 
        "showlegend": False,
        "name": "",
    }

    trace2016 = {
        "z": df2016["avg_score"],
        "x": df2016["date"],
        "y": df2016["news_desk"],
        "xaxis": "x2",
        "yaxis": "y2",
        "type": "heatmap",
        "colorscale": color_scale,
        "showscale": False,
        "text": df2016["top_headlines"],
        "hovertemplate": '<b>Most emotional %{y} headlines for %{x}</b>:' +
            '<br>%{text.score[0]} | %{text.headline[0]}' +
            '<br>%{text.score[1]} | %{text.headline[1]}' +
            '<br>%{text.score[2]} | %{text.headline[2]}' +
            "<br><b>Today's Average: %{z}</b>", 
        "showlegend": False,
        "name": "",
    }

    trace2017 = {
        "z": df2017["avg_score"],
        "x": df2017["date"],
        "y": df2017["news_desk"],
        "xaxis": "x3",
        "yaxis": "y3",
        "type": "heatmap",
        "colorscale": color_scale,
        "showscale": False,
        "text": df2017["top_headlines"],
        "hovertemplate": '<b>Most emotional %{y} headlines for %{x}:</b>' +
            '<br>%{text.score[0]} | %{text.headline[0]}' +
            '<br>%{text.score[1]} | %{text.headline[1]}' +
            '<br>%{text.score[2]} | %{text.headline[2]}' +
            "<br><b>Today's Average: %{z}</b>", 
        "showlegend": False,
        "name": "",
    }

    plot_data = [trace2015, trace2016, trace2017]

    plot_layout = {
        "title": "Average Daily Sentiment by News Desk",
        "xaxis_nticks": 12,
        "grid": {
            "rows": 3, 
            "columns": 1, 
            "pattern": "independent",
            "roworder": "bottom to top",
        }
    }

    heatmap_data = json.dumps(plot_data, cls=plotly.utils.PlotlyJSONEncoder)
    heatmap_layout = json.dumps(plot_layout, cls=plotly.utils.PlotlyJSONEncoder)

    return heatmap_data, heatmap_layout

    # # Create heatmap csv
    # df = pd.read_csv(os.path.join("static", "data", "headlines_scores_keywords.csv"))

    # df["dates"] = df["pub_date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))
    # news_desks = []
    # dates = []
    # avg_day_scores = []
    # top_headlines = []
    # for desk in df["news_desk"].unique():
    #     for day in df["dates"].unique():
    #         headlines_dict = {
    #             "headline": ["None", "None", "None"],
    #             "score": [0, 0, 0]
    #         }
    #         filtered_df = df.loc[(df["dates"] == day) & (df["news_desk"] == desk) & (df["headline_score"] !=0)]
    #         # print(filtered_df)
    #         if filtered_df["headline_score"].to_list():
    #             avg_day_scores.append(filtered_df["headline_score"].mean())
    #             top_headlines_df = filtered_df.nlargest(3, "abs_headline_score")
    #             for i in range(0, 3):
    #                 if len(top_headlines_df["headline"].to_list()) >= (i + 1):
    #                     headlines_dict["headline"][i] = top_headlines_df["headline"].to_list()[i]
    #                 if len(top_headlines_df["headline_score"].to_list()) >= (i + 1):
    #                     headlines_dict["score"][i] = top_headlines_df["headline_score"].to_list()[i] 
    #             top_headlines.append(headlines_dict)
    #         else:
    #             avg_day_scores.append(0)

    #         dates.append(day)
    #         news_desks.append(desk)


    # cal_heatmap_df_new = pd.DataFrame(
    #     list(zip(
    #         dates, 
    #         news_desks, 
    #         avg_day_scores,
    #         top_headlines,
    #     )),
    #     columns=[
    #         "date", 
    #         "news_desk", 
    #         "avg_score",
    #         "top_headlines"
    #     ])

    # cal_heatmap_df_new.to_csv(os.path.join("static", "data", "calendar_heatmap_new.csv"), index=False, encoding="utf-8-sig")
    # print(cal_heatmap_df_new.head(100))
