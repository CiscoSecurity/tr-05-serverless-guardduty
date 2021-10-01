from flask import Blueprint

from api.client import GuardDuty
from api.tiles.factory import TileFactory
from api.utils import jsonify_data, get_jwt, get_json
from api.schemas import DashboardTileDataSchema, DashboardTileSchema

dashboard_api = Blueprint('dashboard', __name__)


@dashboard_api.route('/tiles', methods=['POST'])
def tiles():
    _ = get_jwt()
    tiles_list = TileFactory().list_tiles()

    return jsonify_data(tiles_list)


@dashboard_api.route('/tiles/tile', methods=['POST'])
def tile():
    _ = get_jwt()
    payload = get_json(DashboardTileSchema())

    tile_obj = TileFactory().get_tile(payload['tile_id'])

    return jsonify_data(tile_obj.tile())


@dashboard_api.route('/tiles/tile-data', methods=['POST'])
def tile_data():
    _ = get_jwt()
    payload = get_json(DashboardTileDataSchema())
    tile_id, period = payload['tile_id'], payload['period']
    tile_obj = TileFactory().get_tile(tile_id)
    client = GuardDuty()
    client.search(
        criteria=tile_obj.finding_criteria(period),
        order=tile_obj.sort_criteria,
        unlimited=True if not tile_obj.limit else False,
        limit=tile_obj.limit
    )

    return jsonify_data(tile_obj.tile_data(client.findings, period))
