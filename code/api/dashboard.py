from flask import Blueprint
from datetime import datetime
from api.client import GuardDuty
from api.charts.factory import ChartFactory
from api.utils import jsonify_data, get_jwt, get_json
from api.schemas import DashboardTileSchema, DashboardTileDataSchema

dashboard_api = Blueprint('dashboard', __name__)


@dashboard_api.route('/tiles', methods=['POST'])
def tiles():
    _ = get_jwt()
    charts = ChartFactory().list_charts()

    return jsonify_data(charts)


@dashboard_api.route('/tiles/tile', methods=['POST'])
def tile():
    _ = get_jwt()
    _ = get_json(DashboardTileSchema())
    return jsonify_data({})


@dashboard_api.route('/tiles/tile-data', methods=['POST'])
def tile_data():
    _ = get_jwt()
    payload = get_json(DashboardTileDataSchema())

    chart = ChartFactory().get_chart(payload['tile_id'])
    client = GuardDuty()
    criteria = chart.criterion(payload['period'])
    client.search(criteria, unlimited=True)
    findings = client.findings

    end_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    start_time = datetime.utcfromtimestamp(
        criteria["Criterion"]["updatedAt"]["Gt"]
    )
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")

    return jsonify_data(
        {
            **chart.build(findings),
            **{
                "observed_time": {
                    "start_time": start_time,
                    "end_time": end_time
                },
                "valid_time": {
                    "start_time": start_time,
                    "end_time": end_time
                }
            }
        }
    )
