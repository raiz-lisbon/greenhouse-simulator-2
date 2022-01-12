import pandas as pd
import altair as alt

alt.data_transformers.disable_max_rows()


def plot_timeline(df, y, size=320, width=None, height=None, y_label="value"):
    if width == None:
        width = size
    if height == None:
        height = size

    return alt.Chart(df.tz_convert(None).reset_index(), width=width, height=height, title=y).mark_line().encode(
        alt.X("timestamp:T", axis=alt.Axis(title="time")),
        alt.Y(f"{y}:Q", axis=alt.Axis(title=y_label))
    )


def plot_multiline(df, columns, size=320, width=None, height=None, title="", y_label="value", legend_label="variable", date_format='%H:%M', colors=None):
    """
    Params
    ------
    colors : list
        List of colors corresponding to columns, in the same order
    """

    if width == None:
        width = size
    if height == None:
        height = size
    
    data_to_plot = df[columns]
    return alt.Chart(data_to_plot.tz_convert(None).reset_index().melt("timestamp"), title=title, width=width, height=height).mark_line().encode(
        alt.X('timestamp:T', axis=alt.Axis(format=date_format)),
        alt.Y("value", axis=alt.Axis(title=y_label)),
        alt.Color(
            'variable', 
            legend=alt.Legend(title=legend_label), 
            scale=alt.Scale(domain=columns, range=colors) if colors else None
        )
    )


def plot_x_y_multiline(df, x, ys, size=320, width=None, height=None, title="", x_label="variable", y_label="value", legend_label="variable"):
    if width == None:
        width = size
    if height == None:
        height = size
    
    return alt.Chart(df[ys + [x]].melt(x), title=title).mark_line().encode(
        alt.X(x, axis=alt.Axis(title=x_label)),
        alt.Y("value", axis=alt.Axis(title=y_label)),
        alt.Color('variable', legend=alt.Legend(title=legend_label))
    )


def plot_multiline_dual_y(
    df, 
    columns_1, 
    columns_2=None, 
    size=320, 
    width=None, 
    height=None, 
    title="", 
    y_labels=["value1", "value2"], 
    legend_label="variable", 
    date_format='%H:%M', 
    colors=None,
    left_axis_target_range=None
):
    """
    Params
    ------
    colors : list
        List of colors corresponding to columns, in the same order
    """
    colors_1 = colors[0:len(columns_1)]
    colors_2 = colors[len(columns_1):]

    if width == None:
        width = size
    if height == None:
        height = size

    if left_axis_target_range:
        # Add area to display target range
        cutoff = pd.DataFrame({
            'start': [left_axis_target_range[0]],
            'stop': [left_axis_target_range[1]]
        })

        limits_area = alt.Chart(
            cutoff.reset_index()
        ).mark_rect(
            opacity=0.1
        ).encode(
            x=alt.value(0),
            x2=alt.value(width),
            y='start',
            y2='stop',
            color=alt.Color("index:N", legend=None, scale=alt.Scale(domain=[0], range=[colors_1[-1]]))
        )
    
    data_to_plot_one = df[columns_1]
    left_axis = alt.Chart(data_to_plot_one.tz_convert(None).reset_index().melt("timestamp"), title=title, width=width, height=height).mark_line().encode(
        alt.X('timestamp:T', axis=alt.Axis(format=date_format)),
        alt.Y("value", axis=alt.Axis(title=y_labels[0])),
        alt.Color('variable', legend=alt.Legend(title=legend_label), scale=alt.Scale(domain=columns_1, range=colors_1) if colors else None)

    )

    if left_axis_target_range:
        left_axis = alt.layer(left_axis, limits_area).resolve_scale(color='independent')

    if columns_2:
        data_to_plot_two = df[columns_2]
        right_axis = alt.Chart(data_to_plot_two.tz_convert(None).reset_index().melt("timestamp"), title=title, width=width, height=height).mark_line().encode(
            alt.X('timestamp:T', axis=alt.Axis(format=date_format)),
            alt.Y("value", axis=alt.Axis(title=y_labels[1])),
            alt.Color('variable', legend=alt.Legend(title=legend_label), scale=alt.Scale(domain=columns_2, range=colors_2) if colors else None)

        )

        return alt.layer(left_axis, right_axis).resolve_scale(y='independent', color='independent')
    else:
        return left_axis



def plot_stacked_area(df, columns, size=320, width=None, height=None, title="", y_label="value", legend_label="variable", date_format='%H:%M', colors=None):
    """
    Params
    ------
    colors : list
        List of colors corresponding to columns, in the same order
    """

    if width == None:
        width = size
    if height == None:
        height = size
    
    data_to_plot = df[columns]
    return alt.Chart(data_to_plot.tz_convert(None).reset_index().melt("timestamp"), title=title, width=width, height=height).mark_area().encode(
        alt.X('timestamp:T', axis=alt.Axis(format=date_format)),
        alt.Y("value", axis=alt.Axis(title=y_label)),
        alt.Color(
            'variable', 
            legend=alt.Legend(title=legend_label),
            scale=alt.Scale(domain=columns, range=colors) if colors else None
        ),
        order=alt.Order('sum(variable)', sort='descending')
    )