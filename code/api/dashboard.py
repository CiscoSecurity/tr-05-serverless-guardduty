from flask import Blueprint

from api.client import GuardDuty
from api.tiles.factory import TileFactory
from api.utils import jsonify_data, get_jwt, get_json
from api.schemas import DashboardTileDataSchema

dashboard_api = Blueprint('dashboard', __name__)


@dashboard_api.route('/tiles', methods=['POST'])
def tiles():
    _ = get_jwt()
    tiles_list = TileFactory().list_tiles()

    return jsonify_data(tiles_list)


@dashboard_api.route('/tiles/tile-data', methods=['POST'])
def tile_data():
    _ = get_jwt()
    payload = get_json(DashboardTileDataSchema())

    tile = TileFactory().get_tile(payload['tile_id'], payload['period'])
    client = GuardDuty()
    client.search(tile.criteria(), unlimited=True)

    return jsonify_data(tile.tile_data(client.findings))
