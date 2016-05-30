# RESTfulSpeak
Read text from variant TTS backends through REST API

## Prerequisite
* A working espeak or flite installation. Customized binary is supported as well.
* Python virtualenv is highly recommended.

```
pip install -r requirements.txt
```

|Vendor|Platform|Documentation|
|------|--------|-------------|
|espeak|['darwin', 'linux', 'win32', 'cygwin']|[Offical home page](http://espeak.sourceforge.net/)|
|flite|['darwin', 'linux', 'cygwin']|[Offical home page](http://www.festvox.org/flite/)|
|saypy|['darwin']|Python wrapper script on OS X calling [NSSpeechSynthesizer.phonemesFromText](https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/Classes/NSSpeechSynthesizer_Class/index.html#//apple_ref/occ/instm/NSSpeechSynthesizer/phonemesFromText:)|
|CSSpeak.exe|['win32']|Sample C# code getting [System.Speech.Synthesis.PhonemeReachedEventArgs](https://msdn.microsoft.com/en-us/library/system.speech.synthesis.phonemereachedeventargs%28v=vs.110%29.aspx)|

## Run
```
python api.py
```

## Test
Open http://localhost:5000/ to view the API document and try it out. Or through CLI:

```
$ curl -X GET --header 'Accept: application/json' 'http://localhost:5000/speaks/'
[{"name": "espeak", "backend": {"binary": "/usr/local/bin/espeak", "parameters": [{"name": "text", "arg": " ", "type": 0, "required": true}, {"name": "phoneme", "arg": "-x", "type": -1, "required": false}, {"name": "quiet", "arg": "-q", "type": -1, "required": false}], "availability": ["darwin", "linux", "win32", "cygwin"], "info": "http://espeak.sourceforge.net/"}}, {"name": "flite", "backend": {"binary": "/usr/local/bin/flite", "parameters": [{"name": "text", "arg": "-t", "type": -1, "required": true}, {"name": "phoneme", "arg": "-ps", "type": -1, "required": false}, {"name": "quiet", "arg": "-o /dev/null", "type": -1, "required": false}], "availability": ["darwin", "linux", "cygwin"], "info": "http://www.festvox.org/flite/"}}, {"name": "saypy", "backend": {"binary": "vendor/saypy", "parameters": [{"name": "text", "arg": " ", "type": -1, "required": true}, {"name": "phoneme", "arg": " ", "type": -1, "required": false}, {"name": "quiet", "arg": " ", "type": -1, "required": false}], "availability": ["darwin"], "info": "https://github.com/boltomli/RESTfulSpeak"}}]

$ curl -X GET --header 'Accept: application/json' 'http://localhost:5000/speaks/espeak'
{"info": "http://www.festvox.org/flite/", "binary": "/usr/local/bin/flite", "parameters": [{"name": "text", "arg": "-t", "type": -1, "required": true}, {"name": "phoneme", "arg": "-ps", "type": -1, "required": false}, {"name": "quiet", "arg": "-o /dev/null", "type": -1, "required": false}], "availability": ["darwin", "linux", "cygwin"]}

$ curl -X POST --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: application/json' -d 'text=say%20something' 'http://localhost:5000/speaks/flite'
{"cmd": "['/usr/local/bin/espeak', '-x', '-q', 'say something']", "value": " s'eI s'VmTIN\n"}
```

Mac only:
```
$ curl -X POST --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: application/json' -d 'text=say%20something' 'http://localhost:5000/speaks/saypy'
{"cmd": "['vendor/saypy', 'say something']", "value": "_s1EY _s1UXmTIHN.\n"}
```

Windows only:
```
curl -X POST --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: application/json' -d 'text=say%20something' 'http://localhost:5000/speaks/CSSpeak.exe'
{"value": "_ s ey s ah m th ih ng _ ", "cmd": "['vendor\\\\CSSpeak.exe', 'say something']"}
```

## TODO
In short, better model/class design.
* Customizable parameters with checking
* Audio generation (in BASE64 encoded stream perhaps)
