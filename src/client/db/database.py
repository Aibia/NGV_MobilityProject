import csv

def get_patient_info(patient_id):
    field_names = ["id", "name"]
    error = {}
    with open('patient.csv', 'r', encoding='utf-8') as fd:
        patients_csv = csv.DictReader(fd)
        field_names = patients_csv.fieldnames
        for patient in patients_csv:
            if patient['id'] == patient_id:
                return patient
    for field_name in field_names:
        error[field_name] = ""
    return error

