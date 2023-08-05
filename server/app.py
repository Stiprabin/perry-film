import sys
from flask import (
    Flask,
    request,
    jsonify,
    Response
)
from parsers import parser_lordfilm, parser_jelang
from for_request import data_list


app = Flask(__name__)


@app.route('/')
def home() -> str:
    return "Welcome to the club, buddy!"


@app.route('/', methods=['POST'])
def post() -> Response:
    url = request.form['url']
    query = request.form['query']

    print(f"Запрос \"{query}\" получен!")
    print(sys.platform)

    if url == data_list[0][0]:
        films: list = parser_lordfilm.parser(
            url=data_list[0][1],
            query=query,
            search_id="ajax_search"
        )
    elif url == data_list[1][0]:
        films: list = parser_lordfilm.parser(
            url=data_list[1][1],
            query=query,
            search_id="story"
        )
    else:
        films: list = parser_jelang.parser(
            url=data_list[-1][1],
            query=query
        )

    return jsonify(films)
