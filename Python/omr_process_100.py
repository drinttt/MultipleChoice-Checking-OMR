import sys
import cv2
import numpy as np
import mysql.connector
import os
import re
import math
# Check if enough arguments are provided
if len(sys.argv) < 3:
    print("Usage: python script.py <path_to_save_images> <exam_id>")
    sys.exit(1)

save_images_path = sys.argv[1] 
exam_id = sys.argv[2] 

#17-18 for run in python and comment line 9-14
# save_images_path = 'C://xampp//htdocs//api//result'
# exam_id = "33c2a3"

# Connect to MySQL database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='omr'
)
# Check if connection is successful
if connection.is_connected():
    cursor = connection.cursor()

    print("Connected to MySQL database")

rows_count = 25
cols_count = 5

is_bug = False

threshold_multiplier = 1.15

# Define array mapping for a, b, c, d, e
array_mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}

def fetch_answers(id_exam):
    cursor = connection.cursor()
    cursor.execute("SELECT answer_key FROM exam_answer_key WHERE id_exam = %s", (id_exam,))
    answers = cursor.fetchall()
    cursor.close()
    return [ans[0] for ans in answers]

id_exam = exam_id 
array = fetch_answers(id_exam)

number_of_questions = len(array)
# 1-24
if number_of_questions<25:
    rest = 25-number_of_questions
    row1 = number_of_questions
    row2 = 0
    row3 = 0
    row4 = 0
    array1 = array[0:25-rest] 
# 25
elif number_of_questions==25:
    array1 = array[0:25]
    row1 = number_of_questions
    row2 = 0
    row3 = 0
    row4 = 0
# 26-49
elif 25<number_of_questions<50:
    rest = 50-number_of_questions
    array1 = array[0:25]
    array2 = array[25:50-rest]
    row1 = 25
    row2 = 25-rest
    row3 = 0
    row4 = 0
# 50
elif number_of_questions==50:
    array1 = array[0:25]
    array2 = array[25:50]
    row1 = 25
    row2 = 25
    row3 = 0
    row4 = 0
# 51-74
elif 50<number_of_questions<75:
    rest = 75-number_of_questions
    array1 = array[0:25]
    array2 = array[25:50]
    array3 = array[50:75-rest]
    row1 = 25
    row2 = 25
    row3 = 25 - rest
    row4 = 0
# 75
elif number_of_questions==75:
    array1 = array[0:25]
    array2 = array[25:50]
    array3 = array[50:75]
    row1 = 25
    row2 = 25
    row3 = 25
    row4 = 0
# 76-100
elif 75<number_of_questions<100:
    rest = 100-number_of_questions
    array1 = array[0:25]
    array2 = array[25:50]
    array3 = array[50:75]
    array4 = array[75:100-rest]
    row1 = 25
    row2 = 25
    row3 = 25 
    row4 = 25-rest 
# 100
# elif number_of_questions==100:
else:
    array1 = array[0:25]
    array2 = array[25:50]
    array3 = array[50:75]
    array4 = array[75:100]
    row1 = 25
    row2 = 25
    row3 = 25
    row4 = 25

if number_of_questions<=25:
    answer_array1 = [array_mapping[val] for val in array1]
elif 25<number_of_questions<=50:
    answer_array1 = [array_mapping[val] for val in array1]
    answer_array2 = [array_mapping[val] for val in array2]
elif 50<number_of_questions<=75:
    answer_array1 = [array_mapping[val] for val in array1]
    answer_array2 = [array_mapping[val] for val in array2]
    answer_array3 = [array_mapping[val] for val in array3]
# elif 75<number_of_questions<=100:
else:
    answer_array1 = [array_mapping[val] for val in array1]
    answer_array2 = [array_mapping[val] for val in array2]
    answer_array3 = [array_mapping[val] for val in array3]
    answer_array4 = [array_mapping[val] for val in array4]

src_dir =  'C://xampp//htdocs//api//uploads//' + exam_id
image_files = os.listdir(src_dir)

total_score = 0

x1new = 0
x2new = 0
bw1new = 0
bh1new = 0

y1new = 0
y2new = 0
bw2new = 0
bh2new = 0

x3new = 0
y3new = 0
bw3new = 0
bh3new = 0

x4new = 0
y4new = 0
bw4new = 0
bh4new = 0

for base_name in image_files:
    if base_name.endswith('.jpg') or base_name.endswith('.jpeg') or base_name.endswith('.png'):
    # Extract id_student and id_exam from image name
        match_result = re.match(r'(.+)\.jpg', base_name)
        if match_result:
            id_student = match_result.group(1)
        else:
            print("Pattern not found in filename:", base_name)
            continue
    # Open image
    img = cv2.imread(os.path.join(src_dir, base_name))
    height, width, _ = img.shape

    if width>3000:
        thick = 6 #เส้นกรอบ
        thickness = 6 #ความหนาคำว่า please recheck ในตาราง
        font_scale = 2.5
        fontScale = 3
        fontScale2 = 7.5
    else:
        thick = 2
        thickness = 2
        font_scale = 0.5
        fontScale = 1
        fontScale2 = 3.5

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    h, w = gray.shape
    
    results = np.zeros((rows_count, cols_count))

    # Find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find the largest contour
    max_contour = max(contours, key=cv2.contourArea)
    
    # Get the bounding box of the largest contour
    x1, y1, w1, h1 = cv2.boundingRect(max_contour)
    bw1 = w1 / cols_count
    bh1 = h1 / rows_count
    cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1),(128,0,128), 4) #largest bounding box (purple)
    #print("Top-left point of the largest bounding box (x, y):", (x1, y1))

    second_max_contour = None
    second_max_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > second_max_area and area < cv2.contourArea(max_contour):
            second_max_area = area
            second_max_contour = contour

    x2, y2, w2, h2 = cv2.boundingRect(second_max_contour)
    bw2 = w2 / cols_count
    bh2 = h2 / rows_count
    cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (128,0,128), 4)  #largest bounding box (purple)

    third_max_contour = None
    third_max_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > third_max_area and area < cv2.contourArea(second_max_contour):
            third_max_area = area
            third_max_contour = contour

    x3, y3, w3, h3 = cv2.boundingRect(third_max_contour)
    bw3 = w3 / cols_count
    bh3 = h3 / rows_count
    cv2.rectangle(img, (x3, y3), (x3 + w3, y3 + h3), (128,0,128), 4)  #largest bounding box (purple)

    four_max_contour = None
    four_max_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > four_max_area and area < cv2.contourArea(third_max_contour):
            four_max_area = area
            four_max_contour = contour

    x4, y4, w4, h4 = cv2.boundingRect(four_max_contour)
    bw4 = w4 / cols_count
    bh4 = h4 / rows_count
    cv2.rectangle(img, (x4, y4), (x4 + w4, y4 + h4), (128,0,128), 4)  #largest bounding box (purple)
    

    points = [(x1, y1, bh1, bw1), (x2, y2, bh2, bw2), (x3, y3, bh3, bw3), (x4, y4, bh4, bw4)]
    print(points)
        
    # เรียงลำดับค่า (x, y) ตาม x
    sorted_points = sorted(points, key=lambda point: point[0])

    print(sorted_points[0])
    print(sorted_points[1])
    print(sorted_points[2])
    print(sorted_points[3])
 
    x1new,y1new,bh1new,bw1new = sorted_points[0]
    x2new,y2new,bh2new,bw2new = sorted_points[1]
    x3new,y3new,bh3new,bw3new = sorted_points[2]
    x4new,y4new,bh4new,bw4new = sorted_points[3]

    
    # loop1----------------------------------------------------------------------------------------
    for j in range(rows_count):
        for i in range(cols_count):
            mask = np.zeros(thresh.shape, dtype="uint8")

            # คำนวณตำแหน่งของแต่ละ checkbox
            p1 = (int(i * bw1new) + x1new, int(j * bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
            p2 = (int(i * bw1new + bw1new) + x1new, int(j * bh1new + bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
            cv2.rectangle(mask, p1, p2, (255, 0, 0), -1)

            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            # cv2.imwrite('D://Dear//IV//Project//OMR_WebApp//images//res//thresh_%s.png' % base_name, mask)
            results[j][i] = cv2.countNonZero(mask)

    if 0<=number_of_questions<=100:
        k = 0
        for j in range(row1):
            threshold = results[j].mean() * threshold_multiplier
            for i in range(cols_count):
                total = results[j][i]
                if total >= threshold:
                    if (total - threshold)>20:
                        p1 = (int(i * bw1new) + x1new, int(j * bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
                        p2 = (int(i * bw1new + bw1new) + x1new, int(j * bh1new + bh1new) + y1new)  
                        if answer_array1[k] == i:
                            total_score += 1
                            cv2.rectangle(img, p1, p2, (0, 255,0), thick)
                            try:
                                # ทำการตรวจสอบว่าข้อมูลนั้นมีอยู่ในฐานข้อมูลหรือไม่
                                check_query = "SELECT * FROM student_answer WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                check_data = (id_exam, id_student, j+1)
                                cursor.execute(check_query, check_data)
                                existing_data = cursor.fetchone()
                                if existing_data:
                                    # ถ้ามีข้อมูลอยู่แล้ว ให้ทำการอัพเดตข้อมูลใหม่
                                    update_query = "UPDATE student_answer SET student_answer = %s WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                    update_data = (chr(ord('a') + i), id_exam, id_student, j+1)
                                    cursor.execute(update_query, update_data)
                                    connection.commit()
                                    print("Update successful")
                                else:
                                    # ถ้าไม่มีข้อมูลให้ทำการเพิ่มข้อมูลใหม่
                                    insert_query = "INSERT INTO student_answer (id_exam, id_student, no_student_answer, student_answer) VALUES (%s, %s, %s, %s)"
                                    insert_data = (id_exam, id_student, j+1, chr(ord('a') + i))
                                    cursor.execute(insert_query, insert_data)
                                    connection.commit()
                                    print("Insert successful")
                            except mysql.connector.Error as error:
                                print("Failed to insert/update record into MySQL table:", error)
                                connection.rollback()
                        else:
                            pe1 = (int(answer_array1[k] * bw1new) + x1new, int(j * bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
                            pe2 = (int(answer_array1[k] * bw1new + bw1new) + x1new, int(j * bh1new + bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
                            cv2.rectangle(img, pe1, pe2, (0, 0, 255), thick)
                            try:
                                # ทำการตรวจสอบว่าข้อมูลนั้นมีอยู่ในฐานข้อมูลหรือไม่
                                check_query = "SELECT * FROM student_answer WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                check_data = (id_exam, id_student, j+1)
                                cursor.execute(check_query, check_data)
                                existing_data = cursor.fetchone()
                                if existing_data:
                                    # ถ้ามีข้อมูลอยู่แล้ว ให้ทำการอัพเดตข้อมูลใหม่
                                    update_query = "UPDATE student_answer SET student_answer = %s WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                    update_data = (chr(ord('a') + i), id_exam, id_student, j+1)
                                    cursor.execute(update_query, update_data)
                                    connection.commit()
                                    print("Update successful")
                                else:
                                    # ถ้าไม่มีข้อมูลให้ทำการเพิ่มข้อมูลใหม่
                                    insert_query = "INSERT INTO student_answer (id_exam, id_student, no_student_answer, student_answer) VALUES (%s, %s, %s, %s)"
                                    insert_data = (id_exam, id_student, j+1, chr(ord('a') + i))
                                    cursor.execute(insert_query, insert_data)
                                    connection.commit()
                                    print("Insert successful")
                            except mysql.connector.Error as error:
                                print("Failed to insert/update record into MySQL table:", error)
                                connection.rollback()
                    else:
                        #อันนี้ boolean เพื่อไปบอก คะแนนว่ามีบัคนะ
                        is_bug = True
                        #อันนี้ใส่ไว้บนกรอบ
                        text = "Please Recheck"
                        org = (x1new, int(j * bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        color = (0, 0, 255)  # สีแดง
                        # thickness = 2
                        cv2.putText(img, text, org, font, font_scale, color, thickness)
                        #อันนี้ใส่กรอบแดงยาว
                        pe1 = (x1new, int(j * bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
                        pe2 = (int(bw1new*5) + x1new,int(j * bh1new + bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
                        cv2.rectangle(img, pe1, pe2, (255,0,0), thick)
            k += 1

    # loop2----------------------------------------------------------------------------------------
        for j in range(row2):
            for i in range(cols_count):
                mask = np.zeros(thresh.shape, dtype="uint8")

                # คำนวณตำแหน่งของแต่ละ checkbox
                p1 = (int(i * bw2new) + x2new, int(j * bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
                p2 = (int(i * bw2new + bw2new) + x2new, int(j * bh2new + bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
                cv2.rectangle(mask, p1, p2, (255, 0, 0), -1)

                mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                results[j][i] = cv2.countNonZero(mask)
        n = 0
        for j in range(row2):
            threshold = results[j].mean() * threshold_multiplier
            for i in range(cols_count):
                total = results[j][i]
                if total >= threshold:
                    if (total - threshold)>20:
                            p1 = (int(i * bw2new) + x2new, int(j * bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
                            p2 = (int(i * bw2new + bw2new) + x2new, int(j * bh2new + bh2new) + y2new)
                            if answer_array2[n] == i:
                                total_score += 1
                                cv2.rectangle(img, p1, p2, (0, 255, 0), thick)
                                try:
                                    # ทำการตรวจสอบว่าข้อมูลนั้นมีอยู่ในฐานข้อมูลหรือไม่
                                    check_query = "SELECT * FROM student_answer WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                    check_data = (id_exam, id_student, j+26)
                                    cursor.execute(check_query, check_data)
                                    existing_data = cursor.fetchone()
                                    if existing_data:
                                        # ถ้ามีข้อมูลอยู่แล้ว ให้ทำการอัพเดตข้อมูลใหม่
                                        update_query = "UPDATE student_answer SET student_answer = %s WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                        update_data = (chr(ord('a') + i), id_exam, id_student, j+26)
                                        cursor.execute(update_query, update_data)
                                        connection.commit()
                                        print("Update successful")
                                    else:
                                        # ถ้าไม่มีข้อมูลให้ทำการเพิ่มข้อมูลใหม่
                                        insert_query = "INSERT INTO student_answer (id_exam, id_student, no_student_answer, student_answer) VALUES (%s, %s, %s, %s)"
                                        insert_data = (id_exam, id_student, j+26, chr(ord('a') + i))
                                        cursor.execute(insert_query, insert_data)
                                        connection.commit()
                                        print("Insert successful")
                                except mysql.connector.Error as error:
                                    print("Failed to insert/update record into MySQL table:", error)
                                    connection.rollback()
                            else:
                                pe1 = (int(answer_array2[n] * bw2new) + x2new, int(j * bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
                                pe2 = (int(answer_array2[n] * bw2new + bw2new) + x2new, int(j * bh2new + bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
                                cv2.rectangle(img, pe1, pe2, (0, 0, 255), thick)
                                try:
                                    # ทำการตรวจสอบว่าข้อมูลนั้นมีอยู่ในฐานข้อมูลหรือไม่
                                    check_query = "SELECT * FROM student_answer WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                    check_data = (id_exam, id_student, j+26)
                                    cursor.execute(check_query, check_data)
                                    existing_data = cursor.fetchone()
                                    if existing_data:
                                        # ถ้ามีข้อมูลอยู่แล้ว ให้ทำการอัพเดตข้อมูลใหม่
                                        update_query = "UPDATE student_answer SET student_answer = %s WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                        update_data = (chr(ord('a') + i), id_exam, id_student, j+26)
                                        cursor.execute(update_query, update_data)
                                        connection.commit()
                                        print("Update successful")
                                    else:
                                        # ถ้าไม่มีข้อมูลให้ทำการเพิ่มข้อมูลใหม่
                                        insert_query = "INSERT INTO student_answer (id_exam, id_student, no_student_answer, student_answer) VALUES (%s, %s, %s, %s)"
                                        insert_data = (id_exam, id_student, j+26, chr(ord('a') + i))
                                        cursor.execute(insert_query, insert_data)
                                        connection.commit()
                                        print("Insert successful")
                                except mysql.connector.Error as error:
                                    print("Failed to insert/update record into MySQL table:", error)
                                    connection.rollback()
                    else:
                            #อันนี้ boolean เพื่อไปบอกว่ามีบัคนะ
                            is_bug = True
                            #อันนี้ใส่ไว้บนกรอบ
                            text = "Please Recheck"
                            org = (x2new, int(j * bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            color = (0, 0, 255)  # สีแดง
                            # thickness = 2
                            cv2.putText(img, text, org, font, font_scale, color, thickness)
                            #อันนี้ใส่กรอบแดงยาว
                            pe1 = (x2new, int(j * bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
                            pe2 = (int(bw2new*5) + x2new,int(j * bh2new + bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
                            cv2.rectangle(img, pe1, pe2, (255,0,0), thick)
            n += 1
    # loop3----------------------------------------------------------------------------------------
        for j in range(row3):
                for i in range(cols_count):
                    mask = np.zeros(thresh.shape, dtype="uint8")

                    # คำนวณตำแหน่งของแต่ละ checkbox
                    p1 = (int(i * bw3new) + x3new, int(j * bh3new) + y3new)  # เพิ่มตำแหน่งเริ่มต้น
                    p2 = (int(i * bw3new + bw3new) + x3new, int(j * bh3new + bh3new) + y3new)  # เพิ่มตำแหน่งเริ่มต้น
                    cv2.rectangle(mask, p1, p2, (255, 0, 0), -1)

                    mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                    results[j][i] = cv2.countNonZero(mask)

        n = 0
        for j in range(row3):
            threshold = results[j].mean() * threshold_multiplier
            for i in range(cols_count):
                total = results[j][i]
                if total >= threshold:
                    if (total - threshold)>20:
                        p1 = (int(i * bw3new) + x3new, int(j * bh3new) + y3new)  # เพิ่มตำแหน่งเริ่มต้น
                        p2 = (int(i * bw3new + bw3new) + x3new, int(j * bh3new + bh3new) + y3new)  
                        if answer_array3[n] == i:
                            total_score += 1
                            cv2.rectangle(img, p1, p2, (0, 255, 0), thick)
                            try:
                                # ทำการตรวจสอบว่าข้อมูลนั้นมีอยู่ในฐานข้อมูลหรือไม่
                                check_query = "SELECT * FROM student_answer WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                check_data = (id_exam, id_student, j+51)
                                cursor.execute(check_query, check_data)
                                existing_data = cursor.fetchone()
                                if existing_data:
                                    # ถ้ามีข้อมูลอยู่แล้ว ให้ทำการอัพเดตข้อมูลใหม่
                                    update_query = "UPDATE student_answer SET student_answer = %s WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                    update_data = (chr(ord('a') + i), id_exam, id_student, j+51)
                                    cursor.execute(update_query, update_data)
                                    connection.commit()
                                    print("Update successful")
                                else:
                                    # ถ้าไม่มีข้อมูลให้ทำการเพิ่มข้อมูลใหม่
                                    insert_query = "INSERT INTO student_answer (id_exam, id_student, no_student_answer, student_answer) VALUES (%s, %s, %s, %s)"
                                    insert_data = (id_exam, id_student, j+51, chr(ord('a') + i))
                                    cursor.execute(insert_query, insert_data)
                                    connection.commit()
                                    print("Insert successful")
                            except mysql.connector.Error as error:
                                print("Failed to insert/update record into MySQL table:", error)
                                connection.rollback()

                        else:
                            pe1 = (int(answer_array3[n] * bw3new) + x3new, int(j * bh3new) + y3new)  # เพิ่มตำแหน่งเริ่มต้น
                            pe2 = (int(answer_array3[n] * bw3new + bw3new) + x3new, int(j * bh3new + bh3new) + y3new)  # เพิ่มตำแหน่งเริ่มต้น
                            cv2.rectangle(img, pe1, pe2, (0, 0, 255), thick)
                            try:
                                # ทำการตรวจสอบว่าข้อมูลนั้นมีอยู่ในฐานข้อมูลหรือไม่
                                check_query = "SELECT * FROM student_answer WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                check_data = (id_exam, id_student, j+51)
                                cursor.execute(check_query, check_data)
                                existing_data = cursor.fetchone()
                                if existing_data:
                                    # ถ้ามีข้อมูลอยู่แล้ว ให้ทำการอัพเดตข้อมูลใหม่
                                    update_query = "UPDATE student_answer SET student_answer = %s WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                    update_data = (chr(ord('a') + i), id_exam, id_student, j+51)
                                    cursor.execute(update_query, update_data)
                                    connection.commit()
                                    print("Update successful")
                                else:
                                    # ถ้าไม่มีข้อมูลให้ทำการเพิ่มข้อมูลใหม่
                                    insert_query = "INSERT INTO student_answer (id_exam, id_student, no_student_answer, student_answer) VALUES (%s, %s, %s, %s)"
                                    insert_data = (id_exam, id_student, j+51, chr(ord('a') + i))
                                    cursor.execute(insert_query, insert_data)
                                    connection.commit()
                                    print("Insert successful")
                            except mysql.connector.Error as error:
                                print("Failed to insert/update record into MySQL table:", error)
                                connection.rollback()
                    else:
                            #อันนี้ boolean เพื่อไปบอก คะแนนว่ามีบัคนะ
                            is_bug = True
                            #อันนี้ใส่ไว้บนกรอบ
                            text = "Please Recheck"
                            org = (x3new, int(j * bh3new) + y3new)  # เพิ่มตำแหน่งเริ่มต้น
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            color = (0, 0, 255)  # สีแดง
                            # thickness = 2
                            cv2.putText(img, text, org, font, font_scale, color, thickness)
                            #อันนี้ใส่กรอบแดงยาว
                            pe1 = (x3new, int(j * bh3new) + y3new)  # เพิ่มตำแหน่งเริ่มต้น
                            pe2 = (int(bw3new*5) + x3new,int(j * bh3new + bh3new) + y3new)  # เพิ่มตำแหน่งเริ่มต้น
                            cv2.rectangle(img, pe1, pe2, (255,0,0), thick)
            n += 1
    # loop4----------------------------------------------------------------------------------------
        for j in range(row4):
                    for i in range(cols_count):
                        mask = np.zeros(thresh.shape, dtype="uint8")

                        # คำนวณตำแหน่งของแต่ละ checkbox
                        p1 = (int(i * bw4new) + x4new, int(j * bh4new) + y4new)  # เพิ่มตำแหน่งเริ่มต้น
                        p2 = (int(i * bw4new + bw4new) + x4new, int(j * bh4new + bh4new) + y4new)  # เพิ่มตำแหน่งเริ่มต้น
                        cv2.rectangle(mask, p1, p2, (255, 0, 0), -1)

                        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                        results[j][i] = cv2.countNonZero(mask)

        n = 0
        for j in range(row4):
            threshold = results[j].mean() * threshold_multiplier
            for i in range(cols_count):
                total = results[j][i]
                if total >= threshold:
                    if (total - threshold)>20:
                        p1 = (int(i * bw4new) + x4new, int(j * bh4new) + y4new)  # เพิ่มตำแหน่งเริ่มต้น
                        p2 = (int(i * bw4new + bw4new) + x4new, int(j * bh4new + bh4new) + y4new)  
                        if answer_array4[n] == i:
                            total_score += 1
                            cv2.rectangle(img, p1, p2, (0, 255, 0), thick)
                            try:
                                # ทำการตรวจสอบว่าข้อมูลนั้นมีอยู่ในฐานข้อมูลหรือไม่
                                check_query = "SELECT * FROM student_answer WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                check_data = (id_exam, id_student, j+76)
                                cursor.execute(check_query, check_data)
                                existing_data = cursor.fetchone()
                                if existing_data:
                                    # ถ้ามีข้อมูลอยู่แล้ว ให้ทำการอัพเดตข้อมูลใหม่
                                    update_query = "UPDATE student_answer SET student_answer = %s WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                    update_data = (chr(ord('a') + i), id_exam, id_student, j+76)
                                    cursor.execute(update_query, update_data)
                                    connection.commit()
                                    print("Update successful")
                                else:
                                    # ถ้าไม่มีข้อมูลให้ทำการเพิ่มข้อมูลใหม่
                                    insert_query = "INSERT INTO student_answer (id_exam, id_student, no_student_answer, student_answer) VALUES (%s, %s, %s, %s)"
                                    insert_data = (id_exam, id_student, j+76, chr(ord('a') + i))
                                    cursor.execute(insert_query, insert_data)
                                    connection.commit()
                                    print("Insert successful")
                            except mysql.connector.Error as error:
                                print("Failed to insert/update record into MySQL table:", error)
                                connection.rollback()
                        else:
                            pe1 = (int(answer_array4[n] * bw4new) + x4new, int(j * bh4new) + y4new)  # เพิ่มตำแหน่งเริ่มต้น
                            pe2 = (int(answer_array4[n] * bw4new + bw4new) + x4new, int(j * bh4new + bh4new) + y4new)  # เพิ่มตำแหน่งเริ่มต้น
                            cv2.rectangle(img, pe1, pe2, (0, 0, 255), thick)
                            try:
                                # ทำการตรวจสอบว่าข้อมูลนั้นมีอยู่ในฐานข้อมูลหรือไม่
                                check_query = "SELECT * FROM student_answer WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                check_data = (id_exam, id_student, j+76)
                                cursor.execute(check_query, check_data)
                                existing_data = cursor.fetchone()
                                if existing_data:
                                    # ถ้ามีข้อมูลอยู่แล้ว ให้ทำการอัพเดตข้อมูลใหม่
                                    update_query = "UPDATE student_answer SET student_answer = %s WHERE id_exam = %s AND id_student = %s AND no_student_answer = %s"
                                    update_data = (chr(ord('a') + i), id_exam, id_student, j+76)
                                    cursor.execute(update_query, update_data)
                                    connection.commit()
                                    print("Update successful")
                                else:
                                    # ถ้าไม่มีข้อมูลให้ทำการเพิ่มข้อมูลใหม่
                                    insert_query = "INSERT INTO student_answer (id_exam, id_student, no_student_answer, student_answer) VALUES (%s, %s, %s, %s)"
                                    insert_data = (id_exam, id_student, j+76, chr(ord('a') + i))
                                    cursor.execute(insert_query, insert_data)
                                    connection.commit()
                                    print("Insert successful")
                            except mysql.connector.Error as error:
                                print("Failed to insert/update record into MySQL table:", error)
                                connection.rollback()
                    else:
                            #อันนี้ boolean เพื่อไปบอก คะแนนว่ามีบัคนะ
                            is_bug = True
                            #อันนี้ใส่ไว้บนกรอบ
                            text = "Please Recheck"
                            org = (x4new, int(j * bh4new) + y4new)  # เพิ่มตำแหน่งเริ่มต้น
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            # font_scale = 0.65
                            color = (0, 0, 255)  # สีแดง
                            # thickness = 2
                            cv2.putText(img, text, org, font, font_scale, color, thickness)
                            #อันนี้ใส่กรอบแดงยาว
                            pe1 = (x4new, int(j * bh4new) + y4new)  # เพิ่มตำแหน่งเริ่มต้น
                            pe2 = (int(bw4new*5) + x4new,int(j * bh4new + bh4new) + y4new)  # เพิ่มตำแหน่งเริ่มต้น
                            cv2.rectangle(img, pe1, pe2, (255,0,0), )
            n += 1
# -----------------------------------------------------------------------------------------------------

    # endloop----------------------------------------------------------------------------------------
    print(f"total_score {total_score}")
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    Wpicture = math.ceil(x4new + (bw2new))
    Hpicture = math.ceil(y4new + (bh4new * 28))

    Wpicture_bug = math.ceil(x4new)

    if width>3000:
        Hpicture_bug = math.ceil(y4new - 150)
    else:
        Hpicture_bug = math.ceil(y4new - 100)
    
    
    print("Wpicture: ",Wpicture," Hpicture: ",Hpicture," bw4new: ",bw4new," bh4new: ",bh4new," x4new: ",x4new," y4new: ",y4new)
    bottomLeftCornerOfText = (Wpicture, Hpicture)  # Position to place the text
    # fontScale2 = 3.5
    fontColor = (0, 0, 255)  
    lineType = 2
    cv2.putText(img, str(total_score), bottomLeftCornerOfText, font, fontScale2, fontColor, lineType)
    
    #ถ้า bug ก็เขียนบอก
    if is_bug:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (Wpicture_bug, Hpicture_bug)  # Position to place the text
            # ถ่าย 1 / สแกน 3
            # fontScale = 1
            fontColor = (0, 0, 255)
            lineType = 2
            bug_word = 'Please Recheck'
            cv2.putText(img, str(bug_word), bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            
    try:
        update_query = "UPDATE student SET total_score = %s WHERE id_exam = %s AND id_student = %s"
        data = (total_score, id_exam, id_student)
        cursor.execute(update_query, data)
        connection.commit()
        print("Update successful")
    except mysql.connector.Error as error:
        print("Failed to update record in MySQL table:", error)
        connection.rollback()
    
    output_dir = f'{save_images_path}/{exam_id}'
    os.makedirs(output_dir, exist_ok=True) 
    cv2.imwrite(f'{output_dir}/res_{id_student}.png', img)
    total_score = 0

cursor.close()
connection.close()