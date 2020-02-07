import csv

def get_patient_info(patient_id):
    field_names = ["id", "name"]
    error = {}
    with open('patients.csv', 'r', encoding='utf-8') as fd:
        patients_csv = csv.DictReader(fd)
        field_names = patients_csv.fieldnames
        for patient in patients_csv:
            if patient['id'] == patient_id:
                return patient
    for field_name in field_names:
        error[field_name] = ""
    return error

def get_medicine_info(patient_id):
    field_names = ["id", "medicine"]
    error = {}
    with open('medicine_info.csv', 'r', encoding='utf-8') as fd:
        csv_dict_fd = csv.DictReader(fd)
        field_names = csv_dict_fd.fieldnames
        for medicine_info in csv_dict_fd:
            if medicine_info['id'] == patient_id:
                return medicine_info
    for field_name in field_names:
        error[field_name] = ""
    return error

