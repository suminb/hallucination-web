from flask import Flask, request
from hallucination import ProxyFactory
import requests
import os, sys
import logging

app = Flask(__name__)

logger = logging.getLogger('hallucination-web')
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
logger.addHandler(handler) 
logger.setLevel(logging.INFO)

# TODO: Support other HTTP verbs as well
@app.route('/r', methods=['post'])
def __request__():

    url = request.form['url']

    proxy_factory = ProxyFactory(
        config=dict(db_uri=os.environ.get('DB_URI')),
        logger=logger
    )

    logger.info('proxy_factory={}'.format(proxy_factory))

    keys = filter(lambda x: x != 'url', request.form.keys())
    params = {key: request.form[key] for key in keys}

    #keys = filter(lambda x: x not in ['url', 'q'], request.form.keys())
    #params = {key: request.form[key] for key in keys}
    #data = dict(q=request.form['q'])

    headers = {
        'Referer': 'http://translate.google.com/',
        #'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0)",
        'User-Agent': request.headers['User-Agent'],
        #'Content-Length': str(sys.getsizeof(text))
    }

    try:
        #req = requests.post(url, params=params, data=data, headers=request.headers, timeout=5)
        #req = requests.get(url, params=payload, headers=headers)

        req = proxy_factory.make_request(url, headers=headers, params=params,
            req_type=requests.post, timeout=2, pool_size=10)

        if req == None:
            logger.error('Request failed (req=None)')
            return 'Request failed', 500

        return req.text, req.status_code

    except Exception as e:
        logger.exception(e)
        return str(e), 500


if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = bool(os.environ.get('DEBUG', 0))

    app.run(host=host, port=port, debug=debug)

