import random
import string
from faker import Faker

fake = Faker("pt_PT")
import datetime

# Configurações e dados de exemplo
clinics = [
    "Clínica Gonçalves",
    "Clínica Harmonia",
    "Clínica Cura Total",
    "Clínica Bem Estar",
    "Clínica Saúde Integral",
]
locations = [
    "Lisboa",
    "Sintra",
    "Oeiras",
    "Cadaval",
    "Sobral De Monte Agraço",
    "Alenquer",
    "Torres Vedras",
    "Lourinhã",
    "Mafra",
    "Cascais",
    "Loures",
    "Arruda dos Vinhos",
    "Azambuja",
    "Amadora",
    "Odivelas",
    "Vila Franca de Xira",
]
specialties = ["Ortopedia", "Cardiologia", "Dermatologia", "Neurologia", "Pediatria"]
general_practitioners = 20
other_specialists = 40
patients = 5000
parameters_symptoms = [
    "Febre",
    "Tosse",
    "Dor de garganta",
    "Fadiga",
    "Dificuldade para respirar",
    "Perda de olfato ou paladar",
    "Calafrios",
    "Congestão nasal",
    "Náusea",
    "Vômito",
    "Diarreia",
    "Erupção cutânea",
    "Olhos vermelhos",
    "Confusão",
    "Desmaio",
    "Sangramento nasal",
    "Dor no peito",
    "Falta de ar",
    "Dor lombar",
    "Inchaço nas pernas",
    "Dor ao urinar",
    "Dor nos testículos",
    "Dor nos seios",
    "Dor nos dentes",
    "Dor nas gengivas",
    "Dor no estômago",
    "Dor no fígado",
    "Dor no baço",
    "Dor no pâncreas",
    "Dor no rim",
    "Dor no ovário",
    "Dor no útero",
    "Dor no ânus",
    "Dor no cóccix",
    "Dor no quadril",
    "Dor no joelho",
    "Dor no tornozelo",
    "Dor no pé",
    "Dor no ombro",
    "Dor no cotovelo",
    "Dor no pulso",
    "Dor no pescoço",
    "Dor na coluna",
    "Dor no peito ao respirar",
    "Dor de cabeça",
    "Dor muscular",
    "Dor nos olhos",
    "Dor nas articulações",
    "Dor nos ouvidos",
    "Dor nos dentes",
    "Dor nas gengivas",
    "Dor no estômago",
    "Dor no fígado",
    "Dor no baço",
    "Dor no pâncreas",
    "Dor no rim",
    "Dor no ovário",
    "Dor no útero",
    "Dor no ânus",
    "Dor no cóccix",
]

parameters_metrics = [
    "Temperatura corporal (febre)",
    "Pressão arterial (sistólica e diastólica)",
    "Frequência cardíaca (pulsação)",
    "Frequência respiratória",
    "Nível de oxigênio no sangue (saturação de oxigênio)",
    "Glicemia (níveis de açúcar no sangue)",
    "Nível de dor (escala de 0 a 10)",
    "Peso corporal",
    "Altura",
    "Circunferência abdominal",
    "Circunferência da cintura",
    "Circunferência do quadril",
    "Circunferência da cabeça (em bebês)",
    "Circunferência do braço (para avaliar desnutrição)",
    "Circunferência da coxa",
    "Circunferência do tornozelo",
    "Circunferência do pescoço",
    "Circunferência do pulso",
    "Tamanho da pupila (para avaliar função neurológica)",
    "Força muscular (avaliada por testes específicos)",
    "Amplitude de movimento das articulações",
]

generated_patient_nifs = set()
generated_nifs = set()
generated_ssns = set()
generated_doc_nifs = set()
generated_sns_codes = set()
consulta_queries = []


def generate_clinics():
    clinic_queries = []
    selected_locations = random.sample(locations, 3)  # Select 3 different locations
    for i, clinic in enumerate(clinics):
        address = fake.address().replace("\n", ", ")
        address = address.replace("'", "")
        # Generating a Portuguese postal code format: XXXX-XXX
        # Generate a random phone number
        phone_number = fake.phone_number()
        # Ensure the phone number only contains digits
        phone_number = ''.join(filter(str.isdigit, phone_number))
        
        query = f"INSERT INTO clinica (nome, telefone, morada) VALUES ('{clinic}', '{phone_number}', '{address}');"
        clinic_queries.append(query)
    return clinic_queries

def generate_nurses():
    nurse_queries = []
    for clinic in clinics:
        num_nurses = random.randint(5, 6)  # Generate between 5 and 6 nurses per clinic
        selected_location = random.choice(locations)
        for _ in range(num_nurses):
            nurse_name = fake.name()
            address = fake.address().replace("\n", ", ")
            address = address.replace("'", "")
            # Generating a Portuguese postal code format: XXXX-XXX
            postal_code = fake.postcode().replace(" ", "-")
            full_address = f"{address}, {postal_code} {selected_location}"
            # Generate a random phone number
            phone_number = fake.phone_number()
            # Ensure the phone number only contains digits
            phone_number = ''.join(filter(str.isdigit, phone_number))
            # Generate a random NIF
            nif = ''.join([str(random.randint(0, 9)) for _ in range(9)])
            
            query = f"INSERT INTO enfermeiro (nif, nome, telefone, morada, nome_clinica) VALUES ('{nif}', '{nurse_name}', '{phone_number}', '{full_address}', '{clinic}');"
            nurse_queries.append(query)
    return nurse_queries


def generate_doctors():
    doctor_queries = []
    doctors = []
    for i in range(general_practitioners):
        name = fake.name()
        specialty = "Clínica Geral"
        doctors.append((name, specialty))
    for i in range(other_specialists):
        name = fake.name()
        specialty = random.choice(specialties)
        doctors.append((name, specialty))
    for name, specialty in doctors:
        nif = "".join(random.choices(string.digits, k=9))  # Generate a 9-digit NIF
        while nif in generated_nifs:  # Regenerate NIF if it's already been used
            nif = "".join(random.choices(string.digits, k=9))
        generated_nifs.add(nif)
        generated_doc_nifs.add(nif)
        phone = fake.phone_number()
        phone = ''.join(filter(str.isdigit, phone))
        address = fake.address().replace("\n", ", ")
        query = f"INSERT INTO medico (nif, nome, telefone, morada, especialidade) VALUES ('{nif}', '{name}', '{phone}', '{address}', '{specialty}');"
        doctor_queries.append(query)
    return doctor_queries


doctor_clinic_day_assignments = {}  # Global dictionary to store assignments
clinic_day_doctor_assignments = {}
def assign_doctors_to_clinics():
    global doctor_clinic_day_assignments
    doctor_clinic_day_assignments = {doctor: [] for doctor in generated_doc_nifs}
    global clinic_day_doctor_assignments
    doc_nifs = list(generated_doc_nifs)
    clinic_day_doctor_assignments = {
        (clinic, day): [] for clinic in clinics for day in range(1, 8)
    }

    # Counter to keep track of the doctor index
    doctor_index = 0

    # Iterate through the days of the week
    assignment_queries = []
    for i, day in enumerate(range(1, 8)):
        # Iterate through the doctors 8 times per day
        for j, doctor in enumerate(doc_nifs):
            clinic = clinics[(i+j) % len(clinics)]  # Modulo to cycle through clinics
            doctor_clinic_day_assignments[doctor].append((clinic, day))
            clinic_day_doctor_assignments[(clinic, day)].append(doctor)
            doctor_index = (doctor_index + 1) % len(doc_nifs)  # Cycle through doctors
            query = f"INSERT INTO trabalha (nif, nome, dia_da_semana) VALUES ('{doctor}', '{clinic}', {day-1});"
            assignment_queries.append(query)
    return assignment_queries


def generate_patients():
    patient_queries = []
    for _ in range(patients):
        ssn = "".join(random.choices(string.digits, k=11))  # Generate an 11-digit SSN
        while ssn in generated_ssns:  # Regenerate SSN if it's already been used
            ssn = "".join(random.choices(string.digits, k=11))
        generated_ssns.add(ssn)
        nif = "".join(random.choices(string.digits, k=9))  # Generate a 9-digit NIF
        while nif in generated_nifs:  # Regenerate NIF if it's already been used
            nif = "".join(random.choices(string.digits, k=9))
        generated_nifs.add(nif)
        generated_patient_nifs.add(nif)
        name = fake.name()
        phone = fake.phone_number()
        phone = ''.join(filter(str.isdigit, phone))
        address = fake.address().replace("\n", ", ")
        address = address.replace("'", "")
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=90)
        query = f"INSERT INTO paciente (ssn, nif, nome, telefone, morada, data_nasc) VALUES ('{ssn}', '{nif}', '{name}', '{phone}', '{address}', '{birth_date}');"
        patient_queries.append(query)
    return patient_queries

def generate_appointments():
    generated_patient_appointments = []
    generated_doctor_appointments = []
    consulta_queries = []
    patient_ssns = list(generated_ssns)
    patient_index = 0
    codigo_sns_counter = 1  # Start the codigo_sns counter at 1

    # Iterate over each day in 2023 and 2024
    for year in [2023, 2024]:
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    date = datetime.date(year, month, day)
                except ValueError:
                    # Skip invalid dates (e.g., February 30th)
                    continue
                
                # Iterate over each clinic
                for clinic in clinics:
                    # Get the list of doctors working at the clinic on this day
                    doctors_working = clinic_day_doctor_assignments[(clinic, ((date.weekday() + 1) % 7) + 1)]

                    # Iterate over each doctor assigned to the clinic on this day
                    for j in range(20):
                        # Get the next available patient
                        patient_ssn = patient_ssns[patient_index % len(patient_ssns)]
                        doctor_nif = doctors_working[j % len(doctors_working)]

                        while True:
                            # Generate a random time (hour:minute)
                            hour = random.choice([8, 9, 10, 11, 14, 15, 16, 17])  # Selecting from 8-11h and 14-17h
                            minute = random.choice([0, 30])  # Selecting 0 or 30 minutes
                            time = f"{hour:02}:{minute:02}"
                            
                            # Check if the combination of nif, date, and time is unique
                            if (patient_ssn, date, time) not in generated_patient_appointments and (doctor_nif, date, time) not in generated_doctor_appointments:
                                break  # Unique combination found
                        
                        
                        # Generate the unique codigo_sns
                        codigo_sns = f"{codigo_sns_counter:012d}"
                        codigo_sns_counter += 1  # Increment the counter
                        
                        # Construct the SQL query for the appointment and add it to the list
                        query = f"INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns) VALUES ('{patient_ssn}', '{doctor_nif}', '{clinic}', '{date}', '{time}', '{codigo_sns}');"
                        generated_patient_appointments.append((patient_ssn, date, time))  # Add the combination to the list
                        generated_doctor_appointments.append((doctor_nif, date, time))  # Add the combination to the list
                        consulta_queries.append(query)
                        
                        # Increment the patient index
                        patient_index += 1
    
    return consulta_queries

def generate_prescriptions():
    prescription_queries = []
    # Calculate the stopping point (80% of the list length)
    stop_index = int(len(consulta_queries) * 0.8)
    # Iterate through the list until the stopping point
    for i in range(stop_index):
        consulta = consulta_queries[i]
        medicines = random.randint(1, 6)
        for _ in range(medicines):
            medicine = fake.word()
            quantity = random.randint(1, 3)
            sns_code = consulta.split("'")[
                -2
            ]
            query = f"INSERT INTO receita (codigo_sns, medicamento, quantidade) VALUES ('{sns_code}', '{medicine}', {quantity});"
            prescription_queries.append(query)
    return prescription_queries


def generate_symptom_observations():
    symptom_queries = []
    id = 0
    for consulta in consulta_queries:
        symptoms = random.randint(1, 5)
        id += 1
        for i in range(symptoms):
            symptom = parameters_symptoms[(i + id) % len(parameters_metrics)]
            query = f"INSERT INTO observacao (id, parametro, valor) VALUES ({id}, '{symptom}', NULL);"
            symptom_queries.append(query)
    return symptom_queries


def generate_metric_observations():
    metric_queries = []
    id = 0
    for consulta in consulta_queries:
        id += 1
        metrics = random.randint(0, 3)
        for i in range(metrics):
            metric = parameters_metrics[(i + id) % len(parameters_metrics)]
            value = round(random.uniform(0.0, 100.0), 2)
            query = f"INSERT INTO observacao (id, parametro, valor) VALUES ({id}, '{metric}', {value});"
            metric_queries.append(query)
    return metric_queries


# Gerar todas as queries
queries = []
queries.extend(generate_clinics())
queries.extend(generate_nurses())
queries.extend(generate_doctors())
queries.extend(assign_doctors_to_clinics())
queries.extend(generate_patients())
queries.extend(generate_appointments())
queries.extend(generate_prescriptions())
queries.extend(generate_symptom_observations())
queries.extend(generate_metric_observations())

# Printar todas as queries
for query in queries:
    print(query)

