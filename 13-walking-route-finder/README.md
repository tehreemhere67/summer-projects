# Shortest Walking Route Finder

A real-world shortest walking route finder built with Python, Flask, and OpenStreetMap data. Pick any two locations from the dropdown and get the shortest walking route drawn on an interactive map in your browser.

## How it works
- Uses OpenStreetMap (OSM) data pulled via the osmnx library
- Builds a real street/path graph of the area
- Runs Dijkstra's shortest path algorithm (via NetworkX) on that graph
- Displays the walking route on an interactive Leaflet.js map in the browser

## Accuracy
This app works as well as OpenStreetMap has the area documented. In well-mapped cities like Manhattan, London, Tokyo, or Singapore, walking routes will be accurate and detailed. In areas with poor OSM coverage (like many university campuses or smaller cities in Pakistan), routes may be incomplete or take longer paths because internal walking paths haven't been added to OSM by contributors.

## Can it work for any place in the world?
Yes. To use it for a different city or area, just update the `locations` dictionary in `main.py` with new coordinates and update the `center` point and `dist` radius to cover your area. The rest works automatically.

