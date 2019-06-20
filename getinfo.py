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


    cap = cv.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frame = cv.resize(frame, (800,600))
        cv.imshow("camera", frame)
        key = cv.waitKey(30) & 0xff
        if key == ord(' ') or key == ord('\n'):
            cv.imwrite(path,frame)
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
            cv.putText(frame,"Gender:"+attributes['gender']['value'],(face_rec['left']-50,face_rec['top']-90),
                       cv.FONT_HERSHEY_COMPLEX_SMALL,2,(0,255,0),2)
            cv.putText(frame,"Age:"+str(attributes['age']['value']),(face_rec['left']-50,face_rec['top']-130),
                       cv.FONT_HERSHEY_COMPLEX_SMALL,2,(0,255,0),2)
            cv.putText(frame,"Emotion:"+str(max(attributes['emotion'],key=attributes['emotion'].get)),
                       (face_rec['left']-50,face_rec['top']-50),
                       cv.FONT_HERSHEY_COMPLEX_SMALL,2,(0,255,0),2)
            cv.putText(frame,"Beauty:"+str(attributes['beauty'][str(attributes['gender']['value']).lower()+"_score"]),
                       ((face_rec['left']-50,face_rec['top']-10)),
                       cv.FONT_HERSHEY_COMPLEX_SMALL,2,(0,255,0),2)
            cv.imshow("photo",frame)
        if key == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
