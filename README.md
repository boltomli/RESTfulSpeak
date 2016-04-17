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
Open http://localhost:5000/ to view the API document and try it out.

```
$ curl -X GET --header 'Accept: application/json' 'http://localhost:5000/speaks/'
[{"backend": {"info": "http://espeak.sourceforge.net/", "parameters": [{"name": "text", "type": 0, "required": true, "arg": " "}, {"name": "phoneme", "type": -1, "required": false, "arg": "-x"}, {"name": "quiet", "type": -1, "required": false, "arg": "-q"}], "binary": "/usr/bin/espeak"}, "name": "espeak"}, {"backend": {"info": "http://www.festvox.org/flite/", "parameters": [{"name": "text", "type": -1, "required": true, "arg": "-t"}, {"name": "phoneme", "type": -1, "required": false, "arg": "-ps"}, {"name": "quiet", "type": -1, "required": false, "arg": "-o /dev/null"}], "binary": "/usr/bin/flite"}, "name": "flite"}]

$ curl -X GET --header 'Accept: application/json' 'http://localhost:5000/speaks/espeak'
{"info": "http://espeak.sourceforge.net/", "parameters": [{"required": true, "type": 0, "name": "text", "arg": " "}, {"required": false, "type": -1, "name": "phoneme", "arg": "-x"}, {"required": false, "type": -1, "name": "quiet", "arg": "-q"}], "binary": "/usr/bin/espeak"}

$ curl -X POST --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: application/json' -d 'text=say%20something' 'http://localhost:5000/speaks/flite'
{"value": "pau s ey s aa m th ih ng pau \n", "cmd": "['/usr/bin/flite', '-ps', '-o /dev/null', '-t', 'say something']"}
```

## TODO
In short, better model/class design.
* Customizable parameters with checking
* Audio generation (in BASE64 encoded stream perhaps)
* Flexible backends
