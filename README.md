# Thermo Ai Central Server
Broadcast Image, Video  with the help of Flask and Opencv
## SETUP With conda
```bash
./conda_setup.sh
cd thermo-ai-central-server/
python app.py

```
##  Demo:
```bash
http://35.213.153.96:5009/
```

### Code structure
 * controllers: 
    * __init__.py
    * spec_network
      * templates  # list template file html, css using inside this module
      * __init__.py
      * assets.py # list python function
      * events.py # list socket like socket.on, socket.emit
      * forms.py  # list form using WTForm
      * routes.py # list route like /home, /login, /chat