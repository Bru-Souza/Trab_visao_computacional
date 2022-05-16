import cv2
from detect import detect

class DistanceAlarm:
    def __init__(self) -> None:
        self.levels: dict = {}
        self.img_calib: str = 'calib_levels'
    

    def order_bboxes(self, bboxes_list):
        bboxes_area = []
        for idx, bbox in enumerate(bboxes_list):
            bboxes_area.append(int((bbox[2]-bbox[0])*(bbox[3]-bbox[1])))

        final_areas = sorted(bboxes_area)
        return final_areas
       

    def calibation_levels(self):
        img_calib = cv2.imread(self.img_calib)

        # get all bbox from yolov5
        results = detect()
        bboxes: list = []
        for result in results:
            print(result)
            x1 = int(result[1] - result[3]/2)
            y1 = int(result[2] - result[4]/2)
            x2 = int(result[1] + result[3]/2)
            y2 = int(result[2] + result[4]/2)
            bboxes.append([x1,y1,x2,y2])

        areas = self.order_bboxes(bboxes_list=bboxes)

        riscos = ['Alto','Medio','Baixo']
        self.levels['calibration'] = {risco: area for area, risco in zip(areas, riscos)}
        
        return self.levels
    
    def run(self):

        # self.levels = {'Alto':12672, 'Medio':37632, 'Baixo': 60192}
        self.levels = {'Alto':4672, 'Medio':6632, 'Baixo': 40192}

        frame, results = detect()

        bboxes: list = []
        for result in results:
            x1 = int(result[1] - result[3]/2)
            y1 = int(result[2] - result[4]/2)
            x2 = int(result[1] + result[3]/2)
            y2 = int(result[2] + result[4]/2)
            bboxes.append([x1,y1,x2,y2])
        
    
        for idx, bbox in enumerate(bboxes):
            area = int((bbox[2]-bbox[0])*(bbox[3]-bbox[1]))

            font = cv2.FONT_HERSHEY_SIMPLEX
            if area >= self.levels['Baixo']:
                level = 'Risco Baixo'
                cv2.rectangle(frame,(bbox[0],bbox[1]),(bbox[2],bbox[3]),(0,255,0),3)
                cv2.putText(frame,level,(bbox[0],bbox[1]-10), font, 0.5, (0,255,0),1,cv2.LINE_AA)

            elif area < self.levels['Baixo'] and area >= self.levels['Medio']:
                level = 'Risco Medio'
                cv2.rectangle(frame,(bbox[0],bbox[1]),(bbox[2],bbox[3]),(0,165,255),3)
                cv2.putText(frame,level,(bbox[0],bbox[1]-10), font, 0.5, (0,165,255),1,cv2.LINE_AA)
            else:
                level = 'Risco Alto'
                cv2.rectangle(frame,(bbox[0],bbox[1]),(bbox[2],bbox[3]),(0,0,255),3)
                cv2.putText(frame,level,(bbox[0],bbox[1]-10), font, 0.5, (0,0,255),1,cv2.LINE_AA)
            
            
        cv2.imshow('teste', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite('Result.jpg', frame)
            

    

alarm = DistanceAlarm()
alarm.run()

