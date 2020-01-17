import frappe
import csv
from toolz import first


def execute(filename, processed_filename):
    patient_activities = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cirrus_animal_id = row.get('cirrus_animal_id')
            visit_date = row.get('visit_date')
            patient_activity = _generate_patient_activity(cirrus_animal_id, visit_date)
            if patient_activity:
                patient_activities.append({
                    'cirrus_animal_id': cirrus_animal_id,
                    'visit_date': visit_date,
                    'patient_activity': patient_activity.name
                })

    with open(processed_filename, 'w') as processed_csvfile:
        writer = csv.DictWriter(processed_csvfile, fieldnames=['cirrus_animal_id', 'visit_date', 'patient_activity'])
        writer.writeheader()
        for patient_activity in patient_activities:
            writer.writerow(patient_activity)


def _generate_patient_activity(cirrusvet_id, posting_date):
    patients = _get_patients(cirrusvet_id)

    if len(patients) == 1:
        patient = first(patients)
        patient_activity = frappe.get_doc({
            'doctype': 'Patient Activity',
            'patient': patient.get('name'),
            'posting_date': posting_date
        })
        patient_activity.save()
        return patient_activity

    return None


def _get_patients(cirrusvet_id):
    return frappe.get_all('Patient', filters={'vc_cirrusvet': cirrusvet_id})
