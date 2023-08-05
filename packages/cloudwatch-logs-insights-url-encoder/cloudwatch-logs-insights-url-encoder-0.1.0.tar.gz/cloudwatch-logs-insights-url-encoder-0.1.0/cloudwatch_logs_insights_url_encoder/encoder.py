import urllib.parse

REGION = "ap-northeast-1"


def encode_str(value: str) -> str:
    return "'" + urllib.parse.quote(value).replace("%", "*")


def encode_query_param(value) -> str:
    if value == "true" or value == "false":
        return value
    elif isinstance(value, str):
        return encode_str(value)
    elif isinstance(value, list):
        encoded_elements = ["~" + encode_str(e) for e in value]
        return "(" + "".join(encoded_elements) + ")"
    else:
        return str(value)


def generate_cloudwatch_logs_url(query_params: dict) -> str:
    encoded_query_params = {}
    for key, value in query_params.items():
        encoded_query_params[key] = encode_query_param(value)
    query = "~".join([f"{key}~{value}" for key, value in encoded_query_params.items()])
    query = f"~({query})"
    query = urllib.parse.quote(query)
    query = "?queryDetail=" + query
    query = urllib.parse.quote(query)
    query = query.replace("%", "$")
    url = f"https://{REGION}.console.aws.amazon.com/cloudwatch/home?region={REGION}#logsV2:logs-insights" + query

    return url
