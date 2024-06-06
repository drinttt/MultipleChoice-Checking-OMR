import sys
import cv2
import numpy as np
import mysql.connector
import os
import re

# # Check if enough arguments are provided
if len(sys.argv) < 3:
    print("Usage: python script.py <path_to_save_images> <exam_id>")
    sys.exit(1)

# Store the command line arguments
save_images_path = sys.argv[1]  # The path where you want to save the images
exam_id = sys.argv[2]  # The unique exam ID

# save_images_path = 'C://xampp//htdocs//api//result'
# exam_id = "7a11c4"

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

# Answers count
rows_count = 25
cols_count = 4

# The multiplier used for each row average value in order to define the threshold value
threshold_multiplier = 1.15

def fetch_answers(id_exam):
    cursor = connection.cursor()
    cursor.execute("SELECT answer_key FROM exam_answer_key WHERE id_exam = %s", (id_exam,))
    answers = cursor.fetchall()
    cursor.close()
    # connection.close()
    return [ans[0] for ans in answers]

# Define array mapping for a, b, c, d
array_mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
# Define the array to compare with
# แบ่งอาร์เรย์เป็นสองชุด

#array = ['a','a','b','b','c','c','b','c','b','c','c','d','d','b','c','a','a','d','b','b','c','d','d','c','d','a','b','b','a','c','b','a','c','c','b','d','c','b','a','a','b','c','b','b','b','c','d','d','d','c']
id_exam = exam_id 
array = fetch_answers(id_exam)


# แบ่งเป็นชุดที่ 1 (1-25)ั

first_set = array[:25]
# แบ่งเป็นชุดที่ 2 (26-50)
second_set = array[25:]

total_score = 0
x1new = 0
x2new = 0
y1new = 0
y2new = 0
bw1new = 0
bw2new = 0
bh1new = 0
bh2new = 0

answer_array = [array_mapping[val] for val in first_set]
answer_array2 = [array_mapping[val] for val in second_set]
print("answer_array: ",answer_array)
# Directory containing images
src_dir =  'C://xampp//htdocs//api//uploads//' + exam_id

    # Get list of all files in the directory
image_files = os.listdir(src_dir)

    # Iterate over each image file
for base_name in image_files:
    if base_name.endswith('.jpg') or base_name.endswith('.jpeg') or base_name.endswith('.png'):
    # Proceed with processing image
    # Extract id_student and id_exam from image name
        # match_result = re.match(r'(\d{2}-\d{6}-\d{4}-\d{1})\.jpg', base_name)
        match_result = re.match(r'(.+)\.jpg', base_name)

        if match_result:
            id_student = match_result.group(1)
        else:
            print("Pattern not found in filename:", base_name)
            continue

    # Open image
    img = cv2.imread(os.path.join(src_dir, base_name))
    # Convert image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    # Convert image in black/white
    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Save the black and white image
    # cv2.imwrite('D://Dear//IV//Project//OMR_WebApp//res//thresh_%s.png' % base_name, thresh)
    # 'D:\\Dear\\IV\\Project\\OMR_WebApp\\pages\\omr_process.py'

    h, w = gray.shape

    # The size of the checkboxes

    # bw = 55  # ความกว้างของ checkbox
    # bh = 39  # ความสูงของ checkbox

    results = np.zeros((rows_count, cols_count))  # สร้าง results ก่อนลูปเพื่อป้องกันปัญหา

    # Find contours
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    max_contour = max(contours, key=cv2.contourArea)
    # Get the bounding box of the largest contour
    x1, y1, w1, h1 = cv2.boundingRect(max_contour)

    # Draw the bounding box of the largest contour on the original image with purple color (BGR format)
    cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1),(128,0,128), 4) #largest bounding box (purple)
    bw1 = w1 / cols_count
    bh1 = h1 / rows_count
    
    # Print the coordinates of the top-left point of the largest bounding box
    print("Top-left point of the largest bounding box (x, y):", (x1, y1))

    # Find the second largest contour
    second_max_contour = None
    second_max_area = 0

    # Iterate through contours
    for contour in contours:
        # Calculate the area of the contour
        area = cv2.contourArea(contour)
        # If the current contour has a larger area than the previous second max, update the second max
        if area > second_max_area and area < cv2.contourArea(max_contour):
            second_max_area = area
            second_max_contour = contour

    # Get the bounding box of the second largest contour
    x2, y2, w2, h2 = cv2.boundingRect(second_max_contour)
    bw2 = w2 / cols_count
    bh2 = h2 / rows_count
    
    # Draw the bounding box of the second largest contour on the original image with purple color (BGR format)
    cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (128,0,128), 4)  #largest bounding box (purple)

    print("Top-left point of the second largest bounding box (x2, y2):", (x2, y2))
    if x1 > x2:
        x1new = x2
        y1new = y2
        x2new = x1
        y2new = y1
        bw1new = bw2
        bw2new = bw1
        bh1new = bh2
        bh2new = bh1

    # question in batches of 6
    for j in range(rows_count):
        for i in range(cols_count):
            # construct a mask that reveals only the current
            # "bubble" for the question
            mask = np.zeros(thresh.shape, dtype="uint8")

            # คำนวณตำแหน่งของแต่ละ checkbox
            p1 = (int(i * bw1new) + x1new, int(j * bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
            p2 = (int(i * bw1new + bw1new) + x1new, int(j * bh1new + bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
            cv2.rectangle(mask, p1, p2, (255, 0, 0), -1)

            # apply the mask to the thresholded image, then
            # count the number of non-zero pixels in the
            # bubble area
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            results[j][i] = cv2.countNonZero(mask)

            # Draw the bounding rectangle
            # cv2.rectangle(img, p1, p2, (0, 255, 0), 2)
    k = 0
    for j in range(rows_count):
        threshold = results[j].mean() * threshold_multiplier
        for i in range(cols_count):
            total = results[j][i]

            if total >= threshold:
                p1 = (int(i * bw1new) + x1new, int(j * bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
                p2 = (int(i * bw1new + bw1new) + x1new, int(j * bh1new + bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
                # Draw the bounding rectangle in cyan
                # cv2.rectangle(img, p1, p2, (0, 0, 255), 3)
                # Compare with answer array
                if answer_array[k] == i:
                    # Correct answer
                    print(f"Row {j + 1}, answer {answer_array[k]} , Checkbox {i + 1}: Correct")
                    total_score += 1
                    cv2.rectangle(img, p1, p2, (0, 255,0), 2)
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
                    # Incorrect answer
                    print(f"Row {j + 1}, answer {answer_array[k]} , Checkbox {i + 1}: Incorrect")
                    pe1 = (int(answer_array[k] * bw1new) + x1new, int(j * bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
                    pe2 = (int(answer_array[k] * bw1new + bw1new) + x1new, int(j * bh1new + bh1new) + y1new)  # เพิ่มตำแหน่งเริ่มต้น
                    cv2.rectangle(img, pe1, pe2, (0, 0, 255), 2)
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
        k += 1

    # loop2
    # each question has 6 possible answers, to loop over the
    # question in batches of 6

    for j in range(rows_count):
        for i in range(cols_count):
            # construct a mask that reveals only the current
            # "bubble" for the question
            mask = np.zeros(thresh.shape, dtype="uint8")

            # คำนวณตำแหน่งของแต่ละ checkbox
            p1 = (int(i * bw2new) + x2new, int(j * bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
            p2 = (int(i * bw2new + bw2new) + x2new, int(j * bh2new + bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
            cv2.rectangle(mask, p1, p2, (255, 0, 0), -1)

            # apply the mask to the thresholded image, then
            # count the number of non-zero pixels in the
            # bubble area
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            results[j][i] = cv2.countNonZero(mask)
            # Draw the bounding rectangle
            # cv2.rectangle(img, p1, p2, (0, 255, 0), 2)

    n = 0
    for j in range(rows_count):
        threshold = results[j].mean() * threshold_multiplier
        for i in range(cols_count):
            total = results[j][i]
            if total >= threshold:
                p1 = (int(i * bw2new) + x2new, int(j * bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
                p2 = (int(i * bw2new + bw2new) + x2new, int(j * bh2new + bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
                # Draw the bounding rectangle in cyan
                # cv2.rectangle(img, p1, p2, (0, 0, 255), 3)
                if answer_array2[n] == i:
                    # Correct answer
                    print(f"Row {j + 26} ,answer {answer_array2[n]} , Checkbox {i}: Correct")
                    total_score += 1
                    cv2.rectangle(img, p1, p2, (0, 255, 0), 2)
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
                    # Incorrect answer
                    print(f"Row {j + 26},answer {answer_array2[n]}, Checkbox {i}: Incorrect")
                    pe1 = (int(answer_array2[n] * bw2new) + x2new, int(j * bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
                    pe2 = (int(answer_array2[n] * bw2new + bw2new) + x2new, int(j * bh2new + bh2new) + y2new)  # เพิ่มตำแหน่งเริ่มต้น
                    cv2.rectangle(img, pe1, pe2, (0, 0, 255), 2)
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
        n += 1

    # Save the image with the bounding rectangles
    print(f"total_score {total_score}")
    # Draw the total_score on the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (500, 800)  # Position to place the text
    fontScale = 5
    fontColor = (0, 0, 255)  
    lineType = 2

    cv2.putText(img, str(total_score), bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
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
    #print(f'{output_dir}/res_{base_name}.png')
    # cv2.imwrite('C:/xampp__/htdocs/api/result/394a63/res_%s.png' % base_name, img)
    total_score = 0

cursor.close()
connection.close()