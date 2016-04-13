# This Python file uses the following encoding: utf-8
from flask import Flask, request
from flask_restplus import Api, Resource, reqparse
from subprocess import check_output

app = Flask(__name__)
api = Api(app)

# TODO: Backends should be initialized pragmatically.
Backends = {
    'espeak': {
        'binary': '/usr/bin/espeak',
        'info': 'http://espeak.sourceforge.net/',
        'parameters': {
            'version': {'p': '--version'},
            'help': {'p': '--help'},
            'output': {'p': '-w', 'v': ''},
            'text file': {'p': '-f', 'v': ''},
            'text': {'v': ''},
            'voice': {'p': '-v', 'v': ''},
            'ssml': '-m',
            'phoneme': '-x',
            'quiet': '-q',
        },
    },
    'flite': {
        'binary': './flite2/flite',
        'info': 'http://www.festvox.org/flite/',
        'parameters': {
            'version': {'p': '--version'},
            'help': {'p': '--help'},
            'output': {'p': '-o', 'v': ''},
            'text file': {'p': '-f', 'v': ''},
            'text': {'p': '-t', 'v': ''},
            'voice': {'p': '-voice', 'v': ''},
            'ssml': '-ssml',
            'phoneme': '-ps',
            'quiet': '-o /dev/null',
        },
    },
}


def abort_if_backend_isnt_available(backend_name):
    if backend_name not in Backends:
        abort(404, message="Backend {} isn't available.".format(backend_name))


def build_cmd(backend_name, args):
    if 'text' not in args.keys():
        abort(204, message="Text to speak is invalid.")

    default_parameters = Backends[backend_name]['parameters']
    text_parameter = default_parameters['text']
    text = args['text'].strip()
    if 'p' not in text_parameter.keys():
        text_cmd = [text]
    else:
        text_cmd = [text_parameter['p'], text]

    return [
        # Fill optional parameters
        Backends[backend_name]['binary'],
        default_parameters['phoneme'],
        default_parameters['quiet'],
    ] + text_cmd
    # Text must appear at the end (to make espeak happy)


parser = reqparse.RequestParser()
parser.add_argument('text', type=str, help='Text to speak')
parser.add_argument('parameters', type=str, help='Parameter to backend')


# Backend
# shows a single backend and lets you speak with it
class Backend(Resource):
    def get(self, backend_name):
        abort_if_backend_isnt_available(backend_name)
        return Backends[backend_name]

    def post(self, backend_name):
        abort_if_backend_isnt_available(backend_name)
        args = parser.parse_args()
        cmd = build_cmd(backend_name, args)
        outputs = check_output(cmd).decode('utf-8')
        phonemes = {'phonemes': outputs, 'cmd': cmd}
        return phonemes, 200


# BackEndList
# shows a list of all backends
class BackendList(Resource):
    def get(self):
        return Backends


#
# Actually setup the Api resource routing here
#
api.add_resource(BackendList, '/backends')
api.add_resource(Backend, '/backends/<backend_name>')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
