import json
import requests
import cv2 as cv

path="save.png"
API_Key="mfro7FpM0XTxNgjTol5O0185XF1cOjcI"
API_Secret="Alov0fd4ph67yXkfboJdv5sWu0EZnYEm"


if __name__=='__main__':
    data = {
        "api_key": API_Key,
        "api_secret": API_Secret,
        "return_attributes":"gender,age,emotion,beauty"
    }


    cap = cv.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        frame = cv.resize(frame, (1000,1000))
        cv.imshow("camera", frame)
        key = cv.waitKey(30) & 0xff
        if key == ord(' ') or key == ord('\n'):
            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            cv.imwrite(path,rgb)
            f = open(path, mode="rb+")
            file = {
                "image_file": f
            }
            res = requests.post("https://api-cn.faceplusplus.com/facepp/v3/detect",
                                data=data, files=file)
            res = json.loads(res.text)
            faces=res["faces"]
            faces=faces[0]
            attributes=faces["attributes"]
            face_rec=faces["face_rectangle"]
            cv.rectangle(frame,(face_rec['left'],face_rec['top']),
                         (face_rec['left']+face_rec['width'],
                          face_rec['top']+face_rec['height']),
                         (255,0,0),2)
            cv.putText(frame,"66666",(face_rec['left']+20,face_rec['top']-20),
                       cv.FONT_HERSHEY_COMPLEX,2,(0,255,0),4)
            cv.imshow("photo",frame)
        if key == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
