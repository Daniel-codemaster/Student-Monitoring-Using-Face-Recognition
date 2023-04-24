from datetime import datetime
from unicodedata import name
from django.shortcuts import render, HttpResponse, redirect
from whatsapp_api.main import upload
import face_recognition
import cv2
import dlib
import threading
import time
import numpy as np
from core.models import Student, Camera, Notification, Location
from django.core.files.storage import FileSystemStorage
from io import BytesIO

def index_view(request):
    return render(request, 'index.html',{})

def scan_view(request):
    return render(request, 'monitoring/scan.html', {})
    
def details_view(request):
    return render(request, 'monitoring/details.html', {})

def send_alert(frame, camera):
    #download image
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H%M")
    filename = 'captured/%s_%s.jpg' % (camera.name.replace(" ", "_"), current_time)
    buffer = BytesIO()
    ret, jpg_buffer = cv2.imencode('.jpg', frame)
    buffer.write(jpg_buffer)

    fs = FileSystemStorage()
    filename = fs.save(filename, buffer)
    url = fs.url(filename)
    location = Location.objects.get(id = camera.location.id)

    uploaded = upload(filename, location.name)

    msg = 'This image hase been captured at location: %s' % (camera.location)
    
    notification = Notification(message=msg, 
                                status="Sent" if uploaded else "Failed", 
                                attachment_url=url, 
                                location=location,
                                )
    notification.save()


def doRecognizePerson(face_locations, rgb_small_frame, known_face_encodings, known_face_names, faceNames, faceTrackers, fid, camera, frame):
    
    face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)
    
    name = "Unrecognized"
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(
                            known_face_encodings, face_encoding)
                        
        face_distances = face_recognition.face_distance(
            known_face_encodings, face_encoding)
        
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index] and face_distances[best_match_index] < 0.50:
            student_id = known_face_names[best_match_index]
            
            try:                       
                           
                student = Student.objects.get(id=student_id)
                if(student.Last_location != camera.location):

                    student.Last_location = camera.location
                    student.save()
                    print("location updated")

                    #send alert
                    t2 = threading.Thread( target = send_alert ,
                                            args=(frame, camera))
                    t2.start()

                name = student.forename

                for id in faceNames.keys():
                    if faceNames[ id ] == name:
                        print("Removing fid " + str(id) + " from list of trackers")
                        faceTrackers.pop(id, None)

                
            except Exception as ex:
                print(ex)
                    
        faceNames[ fid ] = name

def ajax(request):
    global attendance

    known_face_encodings = []
    known_face_names = []

    students = Student.objects.all()
    
    for person in students:
        image_of_person = face_recognition.load_image_file(f'media/{person.picture_url}')
        
        person_face_encoding = face_recognition.face_encodings(image_of_person)[0]
        known_face_encodings.append(person_face_encoding)
        known_face_names.append(f'{person.id}')

    video_capture = cv2.VideoCapture(0)

    camera = Camera.objects.get(name = "Web cam")

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    capture = True
    save= True
    uploaded = False

    frameCounter = 0
    currentFaceID = 0

    faceTrackers = {}
    faceNames = {}

    while capture:

        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        rgb_small_frame = small_frame[:, :, ::-1]
     
        fidsToDelete = []
        for fid in faceTrackers.keys():
            trackingQuality = faceTrackers[ fid ].update( small_frame )

            #If the tracking quality is not good enough, we must delete
            #this tracker
            if trackingQuality < 5:
                fidsToDelete.append( fid )

        for fid in fidsToDelete:
            print("Removing fid " + str(fid) + " from list of trackers")
            faceTrackers.pop( fid , None )

        if (frameCounter % 10) == 0:
            face_locations = face_recognition.face_locations(rgb_small_frame)
        
            if len(face_locations) > 0:
                for (top, right, bottom, left) in face_locations:
                    x = left
                    y = top
                    w = right - left
                    h = bottom - top

                    x_bar = x + 0.5 * w
                    y_bar = y + 0.5 * h

                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    matchedFid = None

                    for fid in faceTrackers.keys():
                        tracked_position =  faceTrackers[fid].get_position()

                        t_x = int(tracked_position.left())
                        t_y = int(tracked_position.top())
                        t_w = int(tracked_position.width())
                        t_h = int(tracked_position.height())

                        #calculate the centerpoint
                        t_x_bar = t_x + 0.5 * t_w
                        t_y_bar = t_y + 0.5 * t_h

                        if ( ( t_x <= x_bar   <= (t_x + t_w)) and 
                                ( t_y <= y_bar   <= (t_y + t_h)) and 
                                ( x   <= t_x_bar <= (x + w  )) and 
                                ( y   <= t_y_bar <= (y + h  ))):
                            matchedFid = fid

                            if faceNames[fid] == 'Unrecognized':
                                t2 = threading.Thread( target = doRecognizePerson ,
                                            args=(face_locations, rgb_small_frame, known_face_encodings, known_face_names, faceNames, faceTrackers, fid, camera, frame))
                                t2.start() 
                    
                    if matchedFid is None:

                        print("Creating new tracker " + str(currentFaceID))
                        
                        #Create and store the tracker 
                        tracker = dlib.correlation_tracker()
                        tracker.start_track(small_frame,
                                            dlib.rectangle( x,
                                                            y,
                                                            x+w,
                                                            y+h))

                        faceTrackers[ currentFaceID] = tracker
                        t = threading.Thread( target = doRecognizePerson ,
                                            args=(face_locations, rgb_small_frame, known_face_encodings, known_face_names, faceNames, faceTrackers, currentFaceID, camera, frame))
                        t.start() 
                        currentFaceID += 1

            '''
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)

            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 0.5, (255, 255, 255), 1)
            '''
            process_this_frame = not process_this_frame 

        frameCounter += 1

        for fid in faceTrackers.keys():
            tracked_position =  faceTrackers[fid].get_position()

            t_x = int(tracked_position.left())
            t_y = int(tracked_position.top())
            t_w = int(tracked_position.width())
            t_h = int(tracked_position.height())

            t_x *= 4
            t_y *= 4
            t_w *= 4
            t_h *= 4

            cv2.rectangle(frame, (t_x, t_y),
                                    (t_x + t_w , t_y + t_h),
                                    (0,165,255) ,2)


            if fid in faceNames.keys():
                cv2.putText(frame, faceNames[fid] , 
                            (int(t_x + t_w/2), int(t_y)), 
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 2)
            else:
                cv2.putText(frame, "Detecting..." , 
                            (int(t_x + t_w/2), int(t_y)), 
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 2)

        #largeResult = cv2.resize(frame, (0, 0), fx=4, fy=4)
        cv2.imshow('Video', frame)
        cv2.setWindowProperty('Video', cv2.WND_PROP_TOPMOST, 1)
        
        if cv2.waitKey(1) & 0xFF == 13:
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return HttpResponse("Done")