import json
import decimal

def json_response(data, response_code=200):
    return json.dumps(data, cls=DecimalEncoder), response_code, {'Content-Type': 'application/json'}


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)