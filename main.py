from flask import Flask, render_template, request
import pandas as pd
import folium

app = Flask(__name__)

# Connect to your database and retrieve the groups of locations
# database_connection = ...
# cursor = database_connection.cursor()
# cursor.execute("SELECT * FROM groups")
# groups = cursor.fetchall()

# for the example I'll use a list of groups

groups_df = pd.read_csv('preprocess/linhas_metro.csv')

groups_df.dropna(inplace=True)
groups = groups_df[['linha', 'linhaID']].drop_duplicates().to_dict('records')
print(groups)
#groups = [{'name': 'group 1', 'id': 1}, {'name': 'group 2', 'id': 2}, {'name': 'group 3', 'id': 3}]

# Create a dictionary to store the locations for each group
locations = groups_df.groupby('linhaID').apply(lambda x: list(zip(x['latitude'], x['longitude']))).reset_index().dropna()[0].to_dict()
print(locations)

@app.route("/")
def index():
    return render_template("index.html", groups=groups)

@app.route("/map", methods=["POST"])
def map():
    # Get the selected group ID
    group_id = request.form.get("group")

    # Create a map centered on the first location of the selected group
    df = groups_df[groups_df.linhaID == int(group_id)]
    locs = list(zip(df['latitude'], df['longitude']))
    map = folium.Map(location=locs[0], zoom_start=13)

    # Add markers for each location in the selected group
    for location in locs:
        folium.Marker(location).add_to(map)
        # Add a marker for each location
        folium.Marker(location=location,
                      popup=
                      df.loc[(df['latitude'] == location[0]) & (df['longitude'] == location[1]), 'estacao'].values[
                          0]).add_to(map)

    return render_template("map.html", map=map._repr_html_())

if __name__ == "__main__":
    app.run(debug=True)