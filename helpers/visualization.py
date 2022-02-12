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
        alt.Color('variable', legend=alt.Legend(title=legend_label) if legend_label else None, scale=alt.Scale(domain=columns_1, range=colors_1) if colors else None),
    )

    if left_axis_target_range:
        left_axis = alt.layer(left_axis, limits_area).resolve_scale(color='independent')

    if columns_2:
        data_to_plot_two = df[columns_2]
        right_axis = alt.Chart(data_to_plot_two.tz_convert(None).reset_index().melt("timestamp"), title=title, width=width, height=height).mark_line().encode(
            alt.X('timestamp:T', axis=alt.Axis(format=date_format)),
            alt.Y("value", axis=alt.Axis(title=y_labels[1])),
            alt.Color('variable', legend=alt.Legend(title=legend_label) if legend_label else None, scale=alt.Scale(domain=columns_2, range=colors_2) if colors else None),
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
            legend=alt.Legend(title=legend_label) if legend_label else None
            # scale=alt.Scale(domain=columns, range=colors) if colors else None
        ),
        order=alt.Order('sum(variable)', sort='descending')
    )


def plot_in_grid(all_dfs, all_dfs_key,  chart_fn, col_count=2, row_count=2, **chart_kwargs):
    dfs = all_dfs[all_dfs_key]
    rows = []
    for row_nr in range(row_count):
        charts_of_row = []
        for col_nr in range(col_count):
            i = row_nr * col_count + col_nr
            df_name = list(dfs.keys())[i]
            df = dfs[df_name]
            chart = chart_fn(df, title=df_name, show_label=i==col_count, **chart_kwargs)
            charts_of_row.append(chart)
        vconcat_chart = alt.vconcat(*charts_of_row).resolve_scale(color='independent')
        rows.append(vconcat_chart)

    hconcat_chart =  alt.hconcat(title=all_dfs_key, *rows).resolve_scale(color='independent')
    hconcat_chart = hconcat_chart.configure_title(fontSize=14, offset=5, orient='top', anchor='middle')
    return hconcat_chart


def plot_humidity(df, title, show_label=False, width=400, height=235, is_long=False):
    return plot_multiline_dual_y(
        df.resample('D').mean() if is_long else df,
        ["humidity", "ambient_humidity", "ambient_humidity_at_inside_temp_RH"],
        ["dehum_rate_g_per_s"],
        width=width, 
        height=height, 
        title=f"Humidity: {title}", 
        y_labels=["RH %", "g / s"], 
        legend_label=" " if show_label else None, 
        date_format="",
        colors=["blue", "lightgreen", "green", "orange"],
        left_axis_target_range=[40,70],
    )


def plot_temperature(df, title, show_label=False, width=400, height=235, is_long=False):
    return plot_multiline_dual_y(
        df.resample('D').mean() if is_long else df,
        ["temp", "ambient_temp"],
        ["heating_rate_J_per_s"],
        width=width, 
        height=height, 
        title=f"Temperature: {title}", 
        y_labels=["C", "J / s"], 
        legend_label=" " if show_label else None,
        date_format="",
        colors=["blue", "green", "orange"],
        left_axis_target_range=[17,27]
    )


def plot_energy(df, title, show_label=False, width=400, height=235, is_long=False):
    return plot_stacked_area(
        df.resample('D').mean() if is_long else df, 
        ["energy_used_by_fan_J", "energy_used_by_heating_J", "energy_used_by_dehum_J", "energy_used_by_lighting_J"], 
        width=width,
        height=height,
        title=f"Energy usage: {title}",
        y_label="Energy used (J)",
        legend_label=" " if show_label else None,
    )