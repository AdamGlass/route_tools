from base64 import b64encode

import requests
from flask import escape, jsonify, abort

from gpx import GpxParser
from stats import stats_route
from image import image_route_compare

def get_file(url):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    return r.content

def route_tools(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    request_json = request.get_json(silent=True)

    if not request_json:
        abort(500)

    if request_json['operation'] == 'epp':
        route_gpx = request_json['route_gpx']
        rider_gpx = request_json['rider_gpx']

        route_gpx_file = get_file(route_gpx)
        rider_gpx_file = get_file(rider_gpx)

        route_gpx_parser = GpxParser(route_gpx_file)
        rider_gpx_parser = GpxParser(rider_gpx_file)

        route_gpx_stats = stats_route(route_gpx_parser)
        rider_gpx_stats = stats_route(rider_gpx_parser)

        image = image_route_compare(route_gpx_parser, rider_gpx_parser)
        image_encoded = b64encode(image).decode('ascii')

        stats = {
            'route_gpx_stats' : route_gpx_stats,
            'rider_gpx_stats' : rider_gpx_stats,
            'comparison_image': image_encoded
        }
        return jsonify(stats)
    abort(500)

if __name__ == "__main__":
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/')
    def index():
        return route_tools(request)

    app.run('127.0.0.1', 8000, debug=True)
