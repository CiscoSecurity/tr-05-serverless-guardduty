from datetime import datetime

from flask import Blueprint

from api.client import GuardDuty
from api.charts.factory import ChartFactory
from api.utils import jsonify_data, get_jwt, get_json
from api.schemas import DashboardTileDataSchema

dashboard_api = Blueprint('dashboard', __name__)


@dashboard_api.route('/tiles', methods=['POST'])
def tiles():
    _ = get_jwt()
    charts = ChartFactory().list_charts()

    return jsonify_data(charts)


@dashboard_api.route('/tiles/tile-data', methods=['POST'])
def tile_data():
    _ = get_jwt()
    payload = get_json(DashboardTileDataSchema())

    chart = ChartFactory().get_chart(payload['tile_id'], payload['period'])
    client = GuardDuty()
    criteria = chart.criterion()
    client.search(criteria, unlimited=True)
    findings = client.findings

    end_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    start_time = datetime.fromtimestamp(
        criteria["Criterion"]["updatedAt"]["Gt"]/1000.0
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
