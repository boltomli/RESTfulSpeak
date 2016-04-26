# This Python file uses the following encoding: utf-8
from flask import Flask
from flask_restplus import Api, Resource, fields
from subprocess import check_output

app = Flask(__name__)
api = Api(app, version='0.1', title='Speak API',
          description='Get phonemes of a text from various TTS backends')

ns = api.namespace('speaks', descripton='Speak operations')

# TODO: Backends should be initialized pragmatically.
Backends = {
    'espeak': {
        'binary': '/usr/bin/espeak',
        'info': 'http://espeak.sourceforge.net/',
        'parameters': [
            {'name': 'text', 'arg': ' ', 'type': 0, 'required': True},
            {'name': 'phoneme', 'arg': '-x'},
            {'name': 'quiet', 'arg': '-q'},
        ],
    },
    'flite': {
        'binary': '/usr/bin/flite',
        'info': 'http://www.festvox.org/flite/',
        'parameters': [
            {'name': 'text', 'arg': '-t', 'required': True},
            {'name': 'phoneme', 'arg': '-ps'},
            {'name': 'quiet', 'arg': '-o /dev/null'},
        ],
    },
}

parameter = api.model('Parameter', {
    'name': fields.String(required=True, description='The option name'),
    'arg': fields.String(required=True, description='The argument/switch'),
    'type': fields.Integer(default=-1, description='A custom field tba'),
    'required': fields.Boolean(default=False),
})

backend = api.model('Backend', {
    'binary': fields.String(required=True, description='The backend binary'),
    'info': fields.String(required=True, description='The info site'),
    'parameters': fields.List(fields.Nested(parameter, required=True,
                                            description='The parameter list')),
})

backend_list = api.model('Backend list', {
    'name': fields.String(required=True, description='Name of the backend'),
    'backend': fields.Nested(backend, description='The backend'),
})

result = api.model('Result', {
    'value': fields.String,
    'cmd': fields.String
})


def abort_if_backend_isnt_available(name):
    if name not in Backends:
        api.abort(404, message="Backend {} isn't available.".format(name))


def build_cmd(backend_name, text):
    default_parameters = Backends[backend_name]['parameters']
    text_arg = [p['arg'] for p in default_parameters if p['name'] == 'text'][0]
    phoneme_arg = [p['arg'] for p in default_parameters if p['name'] == 'phoneme'][0]
    quiet_arg = [p['arg'] for p in default_parameters if p['name'] == 'quiet'][0]

    if text_arg.strip() == '': # Such as espeak
        text_cmd = [text.strip()]
    else:
        text_cmd = [text_arg, text.strip()]

    return [
        # Fill optional parameters
        Backends[backend_name]['binary'],
        phoneme_arg,
        quiet_arg,
    ] + text_cmd
    # Text must appear at the end (to make espeak happy)


parser = api.parser()
parser.add_argument('text', type=str, help='Text to speak', required=True, location='form')


@ns.route('/<string:backend_name>')
@api.doc(responses={404: 'Backend not found'},
         params={'backend_name': 'The backend name'})
class Backend(Resource):
    '''Show a single backend and speak with it'''
    @api.doc(description='Name should be one of {0}'.format(', '.join(Backends.keys())))
    @api.marshal_with(backend)
    def get(self, backend_name):
        '''Show a backend'''
        abort_if_backend_isnt_available(backend_name)
        return Backends[backend_name]

    @api.doc(parser=parser)
    @api.marshal_with(result, code=201)
    def post(self, backend_name):
        '''Speak with a backend'''
        abort_if_backend_isnt_available(backend_name)
        args = parser.parse_args()
        cmd = build_cmd(backend_name, args['text'])
        outputs = check_output(cmd).decode('utf-8')
        return {'value': outputs, 'cmd': cmd}, 201


@ns.route('/')
class BackendList(Resource):
    '''Show a list of all available backends'''
    @api.marshal_list_with(backend_list)
    def get(self):
        '''List all backends'''
        return [{'name': name, 'backend': backend} for name, backend in Backends.items()]


if __name__ == '__main__':
    app.run(host='0.0.0.0')
