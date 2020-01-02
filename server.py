from waitress import serve

from app import server

serve(server, port=8050, max_request_header_size=1073741824)



