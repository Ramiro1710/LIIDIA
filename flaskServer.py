import requests
from reconocimientoFacial import ReconocimientoFacial
from flask import Flask, render_template, Response

app = Flask(__name__)
rf = ReconocimientoFacial()

dicci = {
"104": "04-Z-izq",
"204" : "05-caseta",
"304" : "06-area-bicicletas",
"404" : "08-auditorio-pral.",
"504" : "09-auditorio-pasillo",
"604" : "14-juridico-co",
"704" : "07- auditorio-pasillo-cocineta",
"804" : "11-auditorio-huerto",
"904" : "22-inversores",
"1004" : "16-geografia",
"1104" : "01-comedor-b",
"1204" : "24-site-servido",
"1304" : "21-ups-site",
"1404" : "19-antena-bod",
"1504" : "13-reloj-checa",
"1604" : "23-site-entrada",
"1704" : "20-bodega-ad",
"1804" : "15-direccion-g",
"1904" : "10-pasillo-rece",
"2004" : "12-planeacion-",
"2104" : "17-comedor-int",
"2204" : "03-porton-dere",
"2304" : "02-area-discap"
}

def find_camera(id):
    cameras = [1104, 2304, 2204 ,104, 204, 304, 704, 404, 504, 1904, 804, 2004, 1504, 604, 1804, 1004, 2104, 1404, 1704, 1304, 904, 1604, 1204]   
    camera = f"rtsp://Delfin:web.1420@10.25.6.56:554/Streaming/Channels/{str(cameras[int(id)])}"
    return camera, dicci[str(cameras[int(id)])]

@app.route("/")
def index():
    rf.Release()
    return render_template('index.html')

@app.route("/LIIDIA")
def camaras():
    rf.Release()
    return render_template('LIIDIA.html')

@app.route("/Documentacion")
def documentacion():
    rf.Release()
    return render_template('documentacion.html')

@app.route("/Integrantes")
def integrantes():
    rf.Release()
    return render_template('integrantes.html')

@app.route('/video_feed/<string:id>/<string:date>', methods=["GET"])
def video_feed(id, date):
    rf.Release()
    print(find_camera(int(id)))
    url, lugar = find_camera(int(id))
    return Response(rf.Reconocimiento(url, lugar),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    