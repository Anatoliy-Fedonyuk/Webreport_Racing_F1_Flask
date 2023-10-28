"""This module create Web Report of Monaco 2018 Racing using Flask framework"""
import os
from flask import Flask, render_template, request, redirect
from flask_restful import Api
from flasgger import Swagger
from flask_caching import Cache
import redis
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError


from packaging_tutorial.report_FEDONYUK.models import db, model_creation
from packaging_tutorial.report_FEDONYUK.db_util import get_report, get_drivers
from packaging_tutorial.report_FEDONYUK.report_api import ReportResource, DriversResource


_BASE_DIR = os.path.join(os.path.dirname(__file__), '../data/')
DATABASE_FILE = os.path.join(_BASE_DIR, 'monaco.db')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_FILE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


logger.add('debug.log', colorize=True, format='{time} {level} {message}', level='DEBUG')


api = Api(app, prefix='/api/v1/')
swagger = Swagger(app, template_file='Swagger/swagger.yml')

api.add_resource(ReportResource, 'report/')
api.add_resource(DriversResource, 'report/drivers/')

redis_client = redis.StrictRedis(host='localhost', port=6379)

cache_report = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': redis_client, 'CACHE_KEY_PREFIX': 'report'})
cache_drivers = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': redis_client, 'CACHE_KEY_PREFIX': 'drivers'})

cache_report.init_app(app)
cache_drivers.init_app(app)


@app.errorhandler(404)
def handle_not_found_error(error):
    """Handle 404 Not Found error"""
    logger.info("[INFO] File Not Found!")
    return redirect('/apidocs/'), 404



@app.errorhandler(SQLAlchemyError)
def handle_db_error(error):
    """Handle database-related errors."""
    logger.error(f"[ERROR] Database error: {error}")
    return render_template('error.html', error_message="Database error"), 500



@app.route('/report/')
@cache_report.cached(timeout=30, key_prefix='report')
def show_report():
    """The function processes end-points '/' & '/report/' with query-parameters order and driver_id."""
    order = request.args.get('order', 'asc')  # Get the 'order' parameter from the request, default 'asc'
    asc = (order != 'desc')  # If order is not equal to 'desc' then asc=True, otherwise asc=False

    if 'driver_id' in request.args:  # If we get 'driver_id' then redirect it to '/report/drivers/' for processing
        driver_id = request.args['driver_id']
        return redirect('/report/drivers/' + '?driver_id=' + driver_id)

    return render_template('report.html', report=get_report(asc))



@app.route('/report/drivers/')
@cache_drivers.cached(timeout=30, key_prefix='drivers')
def show_drivers():
    """The function processes end-point '/report/drivers/' with query-parameters order and driver_id."""
    order = request.args.get('order', 'asc')  # Get the 'order' parameter from the request, default 'asc'
    asc = (order != 'desc')  # If order is not equal to 'desc' then asc=True, otherwise asc=False

    if 'driver_id' in request.args:  # Getting and processing query parameter 'driver_id'
        driver_id = request.args['driver_id']
        return render_template('report.html', report=get_report(driver=driver_id))

    return render_template('drivers.html', drivers=get_drivers(asc))



if __name__ == '__main__':
    # with app.app_context():   # to create and populate a database model
    #     model_creation()
    app.run(debug=False)
