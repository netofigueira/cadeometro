from flask import Flask, render_template, request, jsonify
import pandas as pd
from src.buildings.build_lister_quinto_andar import BuildListerQuintoAndar
from src.buildings.build_getter_quinto_andar import BuildGetterQuintoAndar
from src.buildings.building import Building
app = Flask(__name__)

# Connect to your database and retrieve the groups of locations
# database_connection = ...
# cursor = database_connection.cursor()
# cursor.execute("SELECT * FROM groups")
# groups = cursor.fetchall()

# for the example I'll use a list of groups

groups_df = pd.read_csv('preprocess/linhas_metro_google.csv')

groups_df.dropna(inplace=True)
groups = groups_df[['linha', 'linhaID']].drop_duplicates().to_dict('records')
#groups = [{'name': 'group 1', 'id': 1}, {'name': 'group 2', 'id': 2}, {'name': 'group 3', 'id': 3}]

# Create a dictionary to store the locations for each group
locations = groups_df.groupby('linhaID').apply(lambda x: list(zip(x['latitude'], x['longitude']))).reset_index().dropna()[0].to_dict()
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
    lats = df.latitude.to_list()
    lngs = df.longitude.to_list()
    names = df.estacao.to_list()
    line_name = df.linha.values[0].split('-')[-1].lower()
    return render_template("map.html", locs=locs, line_name=line_name,lats=lats, lngs =lngs, names=names, subwayChoice=group_id)


@app.route("/get_quinto_andar_data", methods=['GET'])
def get_quinto_andar():


    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))
    max_price = int(request.args.get('max_price'))
    min_price = int(request.args.get('min_price'))

    builder = BuildListerQuintoAndar()
    url_builder = BuildGetterQuintoAndar()
    buildings_close = builder.get_buildings_close(lat=lat, lon=lng, max_price=max_price, min_price=min_price)
    buildings_close = sorted(buildings_close, key=lambda b: b._id)

    #tresh = min(10, len(buildings_close))

    # filtrar 10 elementos por enquanto, pq estão carregando mtos
    # lidar com isso dps
    #buildings_close = buildings_close[:tresh]
    return jsonify({
        'buildings': [
            {'lat': building.lat, 'lng': building.lon, 'building_id':building._id, 'url': url_builder.get_building_url(building)}
            for building in buildings_close
        ]
    })


@app.route("/get_building_data", methods=['GET'])
def get_building_data():

    building_id  = request.args.get('building_id')
    builder = BuildGetterQuintoAndar()

    building_data = builder.get_building_basic_data(Building(str(building_id)))
    building_url = builder.get_building_url(Building(str(building_id)))
    # filtrar 10 elementos por enquanto, pq estão carregando mtos
    # lidar com isso dps
    return jsonify({
        'building_photos': [
            { 'photo_url': url}
            for url in building_data.principal_images_url
        ],
        'name':building_data.name,
        'description': building_data.description.removesuffix(', e fica próximo ao metrô.').removeprefix('Alugue sem depender de ninguém!'),
        'building_url':building_url,
        'building_address':building_data.address
    })

if __name__ == "__main__":
    app.run(debug=True)
