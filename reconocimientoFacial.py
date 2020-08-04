import cv2
import os
class ReconocimientoFacial():
    def __init__(self):
        self.initModelo()

    def initModelo(self):
        self.dataPath = 'PD'  # Cambia a la ruta donde hayas almacenado Data
        self.imagePaths = os.listdir(self.dataPath)
        print('imagePaths=', self.imagePaths)

        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()

        self.face_recognizer.read('modeloLBPHFace.xml')

        ##DICCIONARIO DE DATOS
        # cv2.VideoCapture(0) --> Camara web

        #cap = cv2.VideoCapture("rtsp://Delfin:web.1420@10.25.6.56:554/Streaming/Channels/1204")
        
        #,cv2.CAP_DSHOW

        self.faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def Reconocimiento(self, CamaraID, lugar):
        try:
            self.cap.release()
        except:
            print(" ")
        
        self.cap = cv2.VideoCapture(CamaraID)
        while True:
            self.ret, self.frame = self.cap.read()
            if self.ret == False: break

            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            self.auxFrame = self.gray.copy()

            self.faces = self.faceClassif.detectMultiScale(self.gray, 1.3, 5)

            for (x, y, w, h) in self.faces:
                self.rostro = self.auxFrame[y:y + h, x:x + w]
                self.rostro = cv2.resize(self.rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
                self.result = self.face_recognizer.predict(self.rostro)
                self.rperc = (self.result[1] + 10)

                """"
                rperc = round(100 - (result[1] - 60), 2)
                if rperc > 100:
                    rperc = 99
                if 0 <= rperc:
                    perc = str(rperc) + ' %'
                    cv2.putText(frame, '{}'.format(perc), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
                """
                if self.rperc > 100:
                    self.rperc = 99

                self.perc = str(self.rperc) + ' %'
                cv2.putText(self.frame, '{}'.format(self.perc), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
                #cv2.putText(frame, '{}'.format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

                '''
                # EigenFaces
                if result[1] < 5700:
                    cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                else:
                    cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)

                # FisherFace
                if result[1] < 500:
                    cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                else:
                    cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
                '''

                # LBPHFace
                if self.result[1] < 73:
                #if 60 <= result[1] <= 90:
                    cv2.putText(self.frame, '{}'.format(self.imagePaths[self.result[0]]), (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    if self.rperc >= 95:
                        print(self.rperc)
                        self.user = self.imagePaths[self.result[0]]
                        #BD
                        from registroemail import search
                        email = search(self.user, lugar)
                        if email == 1:
                            print('prueba')
                            from sendemail import sendemail
                            sendemail(self.user, self.rperc, lugar)
                    break

                else:
                    cv2.putText(self.frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            try:
                self.ret, self.buffer = cv2.imencode('.jpg', self.frame)
                self.frame = self.buffer.tobytes()
            except:
                self.frame = b'0'

            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + self.frame + b'\r\n')

            
    def Release(self):
        try:
            self.cap.release()
        except:
            print("no inicio")