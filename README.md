# RESTfulSpeak
Read text from variant TTS backends through REST API

## Prerequisite
* A working espeak or flite installation.
* Python virtualenv is highly recommended.

```
pip install -r requirements.txt
```

## Run
```
python api.py
```

## Test
```
$ curl http://localhost:5000/backends
{"espeak": {"info": "http://espeak.sourceforge.net/", "binary": "/usr/bin/espeak", "parameters": {"phoneme": "-x", "ssml": "-m", "version": {"p": "--version"}, "help": {"p": "--help"}, "text": {"v": ""}, "text file": {"p": "-f", "v": ""}, "output": {"p": "-w", "v": ""}, "voice": {"p": "-v", "v": ""}, "quiet": "-q"}}, "flite": {"info": "http://www.festvox.org/flite/", "binary": "./flite2/flite", "parameters": {"phoneme": "-ps", "ssml": "-ssml", "version": {"p": "--version"}, "help": {"p": "--help"}, "text": {"p": "-t", "v": ""}, "text file": {"p": "-f", "v": ""}, "output": {"p": "-o", "v": ""}, "voice": {"p": "-voice", "v": ""}, "quiet": "-o /dev/null"}}}

$ curl http://localhost:5000/backends/espeak -d "text=say something" -X POST
{"phonemes": " s'eI s'VmTIN\n", "cmd": ["/usr/bin/espeak", "-x", "-q", "say something"]}
```

## TODO
In short, better model/class design.
* Customizable parameters with checking
* Audio generation (in BASE64 encoded stream perhaps)
* Flexible backends
