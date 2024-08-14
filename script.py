import csv
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read(10000)
        result = chardet.detect(raw_data)
        return result['encoding']

def read_register_file(register_file, encoding):
    student_dict = {}
    with open(register_file, mode='r', encoding=encoding) as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            student_number = row['شماره دانشجويي ']
            firstname = row['نام']
            lastname = row['نام خانوادگي']
            student_dict[student_number] = f"{firstname} {lastname}"
    return student_dict

'''
    student_number = row['‘г«—е ѕ«д‘ћжнн ']
    firstname = row['д«г']
    lastname = row['д«г ќ«дж«ѕРн']
'''

def read_major_file(major_file, encoding):
    student_numbers_in_major = []
    with open(major_file, mode='r', encoding=encoding) as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            student_numbers_in_major.append(row['شماره دانشجویی'])
    return student_numbers_in_major

def find_missing_students(student_dict, student_numbers_in_major):
    missing_students = {}
    for student_number, fullname in student_dict.items():
        if student_number not in student_numbers_in_major:
            missing_students[student_number] = fullname
    return missing_students

def write_missing_students_to_csv(missing_students, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['شماره دانشجویی', 'نام و نام خانوادگی'])
        for student_number, fullname in missing_students.items():
            writer.writerow([student_number, fullname])

register_file = 'ثبت - ثبت.csv.csv'
major_file = 'گرایش.csv'
output_file = 'دانشجویان_گمشده.csv'

register_file_encoding = detect_encoding(register_file)
major_file_encoding = detect_encoding(major_file)

student_dict = read_register_file(register_file, register_file_encoding)
student_numbers_in_major = read_major_file(major_file, major_file_encoding)

missing_students = find_missing_students(student_dict, student_numbers_in_major)

write_missing_students_to_csv(missing_students, output_file)

print(f"فایل خروجی با نام '{output_file}' با موفقیت ایجاد شد.")
