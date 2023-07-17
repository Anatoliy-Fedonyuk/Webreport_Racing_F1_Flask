"""This module is creation Web Report of Monaco 2018 Racing using Flask framework"""
import os
from flask import Flask, render_template, request, redirect
from flask_restful import Api
from flasgger import Swagger
# from flask_sqlalchemy import SQLAlchemy

from packaging_tutorial.report_FEDONYUK.sqlite_creation import db, DriverModel
from packaging_tutorial.report_FEDONYUK.report_api import ReportResource, DriversResource

_BASE_DIR = os.path.join(os.path.dirname(__file__), '../data/')
DATABASE_FILE = os.path.join(_BASE_DIR, 'monaco.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_FILE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
db.init_app(app)
api = Api(app, prefix='/api/v1/')
swagger = Swagger(app, template_file='Swagger/swagger.yml')

api.add_resource(ReportResource, 'report/')
api.add_resource(DriversResource, 'report/drivers/')


@app.errorhandler(404)
def handle_not_found_error(error):
    """Handle 404 Not Found error"""
    return redirect('/apidocs/'), 404


@app.route('/report/')
def show_report():
    """The function processes end-points '/' & '/report/' with query-parameters order and driver_id."""
    order = request.args.get('order', 'asc')  # Get the 'order' parameter from the request, default 'asc'
    asc = (order != 'desc')  # If order is not equal to 'desc' then asc=True, otherwise asc=False

    if 'driver_id' in request.args:  # If we get 'driver_id' then redirect it to '/report/drivers/' for processing
        driver_id = request.args['driver_id']
        return redirect('/report/drivers/' + '?driver_id=' + driver_id)

    drivers = DriverModel.query.all()
    report = [[dr.id, dr.driver_id, dr.name, dr.team, dr.best_lap] for dr in drivers]
    if not asc:
        report.reverse()
    return render_template('report.html', report=report)


@app.route('/report/drivers/')
def show_drivers():
    """The function processes end-point '/report/drivers/' with query-parameters order and driver_id."""
    order = request.args.get('order', 'asc')  # Get the 'order' parameter from the request, default 'asc'
    asc = (order != 'desc')  # If order is not equal to 'desc' then asc=True, otherwise asc=False

    if 'driver_id' in request.args:  # Getting and processing query parameter 'driver_id'
        driver_id = request.args['driver_id']

        report = [DriverModel.query.filter_by(driver_id=driver_id).all()]
        print(report)
        # report = build_report(driver=driver_id)
        return render_template('report.html', report=report)

    # drivers = get_list_drivers(asc=asc)  # We send the generated data to display the table in drivers.html
    # return render_template('drivers.html', drivers=drivers)


if __name__ == '__main__':
    app.run(debug=True)
