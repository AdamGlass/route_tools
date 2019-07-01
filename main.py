import os
from base64 import b64encode
from datetime import timedelta
import uuid

import requests
from flask import escape, jsonify, abort, redirect

from google.cloud import storage

from gpx import GpxParser
from stats import stats_route
from image import image_route_compare, image_route
from similarity import similarity

def get_file(url):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    return r.content

def get_blob():
    gcs_client = storage.Client()
    bucket_name = os.environ['GCS_BUCKET']
    bucket = gcs_client.get_bucket(bucket_name)
    name = uuid.uuid4().hex + '.png'
    blob = bucket.blob(name)
    return blob

def upload_to_blob(blob, image):
    blob.upload_from_string(image)
    blob.make_public()
    url = blob.public_url
    return url

def get_comparison_image_url(route, rider):
    blob = get_blob()
    image = image_route_compare(route, rider)
    url = upload_to_blob(blob, image)
    return url

def get_image_url(rider):
    blob = get_blob()
    image = image_route(rider)
    url = upload_to_blob(blob, image)
    return url

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

    rider_gpx = request.args.get('rider_gpx')
    route_gpx = request.args.get('route_gpx') 
    
    if not request.args.get('op'):
        abort(500)

    op = request.args['op']

    if rider_gpx:
        rider_gpx_file = get_file(rider_gpx)
        rider_gpx_parser = GpxParser(rider_gpx_file)

    if route_gpx:
        route_gpx_file = get_file(route_gpx)
        route_gpx_parser = GpxParser(route_gpx_file)
        
    if rider_gpx and route_gpx and op == 'compare':
        url = get_comparison_image_url(route_gpx_parser, rider_gpx_parser)

        return redirect(url)

    if rider_gpx and route_gpx and op == 'stats':
        route_gpx_stats = stats_route(route_gpx_parser)
        rider_gpx_stats = stats_route(rider_gpx_parser)

        sim = similarity(route_gpx_parser, rider_gpx_parser)

        stats = {
            'route_gpx_stats' : route_gpx_stats,
            'rider_gpx_stats' : rider_gpx_stats,
            'similarity': sim
        }
        return jsonify(stats)

    if rider_gpx and op == 'image':
        url = get_image_url(rider_gpx_parser)
        return redirect(url)

    abort(500)

if __name__ == "__main__":
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/')
    def index():
        return route_tools(request)

    app.run('127.0.0.1', 8001, debug=True)
