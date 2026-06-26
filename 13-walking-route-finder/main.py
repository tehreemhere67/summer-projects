import osmnx as ox
import networkx as nx
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

locations = {
    "Times Square": (40.7580, -73.9855),
    "Central Park": (40.7851, -73.9683),
    "Empire State Building": (40.7484, -73.9967),
    "Brooklyn Bridge": (40.7061, -73.9969),
    "Statue of Liberty Ferry": (40.6892, -74.0445),
    "Grand Central Terminal": (40.7527, -73.9772),
    "One World Trade Center": (40.7127, -74.0134),
    "High Line Park": (40.7480, -74.0048),
    "Rockefeller Center": (40.7587, -73.9787),
    "Penn Station": (40.7506, -73.9971),
    "Madison Square Garden": (40.7505, -73.9934),
    "Wall Street": (40.7074, -74.0113),
}

center = (40.7484, -73.9967)
G = ox.graph_from_point(center, dist=3000, network_type="walk")

location_nodes = {}
for name, (lat, lng) in locations.items():
    node = ox.nearest_nodes(G, lng, lat)
    location_nodes[name] = node

print("Map loaded.")

@app.route("/")
def index():
    return render_template("index.html", locations=list(locations.keys()))

@app.route("/route", methods=["POST"])
def find_route():
    data = request.get_json()
    origin = data["origin"]
    destination = data["destination"]

    if origin not in locations or destination not in locations:
        return jsonify({"error": "Invalid location"}), 400

    origin_node = location_nodes[origin]
    dest_node = location_nodes[destination]

    path = nx.shortest_path(G, origin_node, dest_node, weight="length")
    length = nx.shortest_path_length(G, origin_node, dest_node, weight="length")

    # Convert path nodes to lat/lng coordinates
    coordinates = []
    for node in path:
        lat = G.nodes[node]['y']
        lng = G.nodes[node]['x']
        coordinates.append([lat, lng])

    return jsonify({
        "coordinates": coordinates,
        "distance": round(length),
        "minutes": round(length / 80),
        "origin": origin,
        "destination": destination
    })

if __name__ == "__main__":
    app.run(debug=True)