
## Disclaimer
This isn't really a project meant for anything outside of my usecase. I wanted to avoid setting up OTA Updates for my ESP32 Weather station but still be able to make changes to add or update apis for other sites while also using MQTT internally for other display options like displays in my home.
I will probably not care that much about bugs in edge cases and support for multiple stations as long as I don't need it.

## Run it
### Install Dependencies
The script has been tested on Python3.8 but should work on all Python3.x versions.
You need to install the required modules using: 
```
python3 -m pip install -r requirements.txt
```
If ``pip`` or ``pip3`` for python3 is available as a seprate command you can avoid using ``python3 -m`` for the installation.

### Executing
The project is layed out as a module therefor you have to run it as a module:
```
python3 -m weatherBackend
```
Info: Execution starts inside the weatherBackend directory, in \_\_main\_\_.py

