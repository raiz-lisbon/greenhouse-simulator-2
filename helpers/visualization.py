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


def plot_multiline_dual_y(df, columns_1, columns_2, size=320, width=None, height=None, title="", y_labels=["value1", "value2"], legend_label="variable", date_format='%H:%M', colors=None):
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
    
    data_to_plot_one = df[columns_1]
    line_one = alt.Chart(data_to_plot_one.tz_convert(None).reset_index().melt("timestamp"), title=title, width=width, height=height).mark_line().encode(
        alt.X('timestamp:T', axis=alt.Axis(format=date_format)),
        alt.Y("value", axis=alt.Axis(title=y_labels[0])),
        alt.Color('variable', legend=alt.Legend(title=legend_label), scale=alt.Scale(domain=columns_1, range=colors) if colors else None)

    )

    data_to_plot_two = df[columns_2]
    line_two = alt.Chart(data_to_plot_two.tz_convert(None).reset_index().melt("timestamp"), title=title, width=width, height=height).mark_line().encode(
        alt.X('timestamp:T', axis=alt.Axis(format=date_format)),
        alt.Y("value", axis=alt.Axis(title=y_labels[1])),
        alt.Color('variable', legend=alt.Legend(title=legend_label), scale=alt.Scale(domain=columns_2, range=colors) if colors else None)

    )

    return alt.layer(line_one, line_two).resolve_scale(y='independent')


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