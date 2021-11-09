import altair as alt

def plot_timeline(df, y, size=320, width=None, height=None):
    if width == None:
        width = size
    if height == None:
        height = size

    return alt.Chart(df.reset_index(), width=300, height=150, title=y).mark_line().encode(
        alt.X("timestamp:T", axis=alt.Axis(title="time")),
        alt.Y(f"{y}:Q")
    )