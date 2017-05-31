#!/usr/bin/env python

"""
collect fingerprint information about requesting webbrowsers.

uses javascript libraries (clientjs, fingerprintjs2 and beaverbird) to
    collect client-side information.
client transmits findings to web service endpoint and data is stored
    to a sqlite database for later processing.
"""

import re
import json

from json2html import json2html

from sqlite_object import SqliteDict
from flask import Flask, render_template, send_from_directory, request
from flask_restful import Resource, Api
from flask_cachecontrol import (FlaskCacheControl, dont_cache)

app = Flask(__name__)
api = Api(app)

flask_cache_control = FlaskCacheControl()
flask_cache_control.init_app(app)


@app.route('/')
@dont_cache()
def index():
    """ serve index html that will run fingerprint js """
    print('index')
    browser = request.args.get('browser') or 'None'
    headers = dict(request.headers)
    return render_template('index.html', browser=browser, headers=headers)


@app.route('/js/<path:path>')
@dont_cache()
def send_js(path):
    """ serve own javascript files """
    print('send_js', path)
    return send_from_directory('js', path)


@app.route('/node_modules/<path:path>')
@dont_cache()
def send_nm(path):
    """ serve javascript libraries """
    print('node_modules', path)
    return send_from_directory('node_modules', path)


def remove_num_keys(tree):
    """ remove numeric dict keys, which are often duplicates from
        javascript attribute enumeration """
    if isinstance(tree, dict):
        to_delete = []
        for elt in tree.keys():
            if re.match(r'^[0-9]{1,3}', elt):
                to_delete.append(elt)
            else:
                remove_num_keys(tree[elt])

        for elt in to_delete:
            del tree[elt]
    return tree


def cleanup(data):
    """ remove large webgl/canvas fields for display """
    remove_num_keys(data['navigator'])
    del data['clientjs']['CanvasPrint']
    del data['fingerprintjs2']['canvas']
    try:
        pass
        #del data['fingerprintjs2']['webgl']
    except KeyError:
        pass
    return data


class PostResults(Resource):
    """ api endpoint to receive fingerprint findings """
    def post(self):
        """
        receive fingerprint json, store in thread-safe
            persistent sqlite database and return rendered html table
            back to caller
        """
        store = SqliteDict(filename='fingerprints.db', persist=True)
        json_data = request.get_json(force=True)

        # require "browser" field in json from "?browser=" param
        if 'browser' in json_data:
            browser = json_data['browser']
            store[browser] = json_data
            print('PostResults', browser)

            json_sorted = json.dumps(cleanup(json_data), sort_keys=True)

            table_data = json2html.convert(json_sorted)
            return render_template('table.html', table_data=table_data)
        else:
            msg = 'PostResults - no browser given'
            print(msg)
            return render_template('table.html', table_data=msg)
        # store auto closes


api.add_resource(PostResults, '/postResults')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
