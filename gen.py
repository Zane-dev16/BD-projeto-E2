import random
import string
from faker import Faker

fake = Faker("pt_PT")

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
    for clinic in clinics:
        location = random.choice(locations)
        address = fake.address().replace("\n", ", ")
        postal_code = fake.postcode()
        query = f"INSERT INTO clinica (name, address, postal_code, location) VALUES ('{clinic}', '{address}', '{postal_code}', '{location}');"
        clinic_queries.append(query)
    return clinic_queries


def generate_nurses():
    nurse_queries = []
    generated_nifs = set()
    for clinic in clinics:
        for _ in range(random.randint(5, 6)):
            nif = "".join(random.choices(string.digits, k=9))  # Generate a 9-digit NIF
            while nif in generated_nifs:  # Regenerate NIF if it's already been used
                nif = "".join(random.choices(string.digits, k=9))
            generated_nifs.add(nif)
            name = fake.name()
            phone = fake.phone_number()
            address = fake.address().replace("\n", ", ")
            query = f"INSERT INTO enfermeiro (nif, nome, telefone, morada, nome_clinica) VALUES ('{nif}', '{name}', '{phone}', '{address}', '{clinic}');"
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
        address = fake.address().replace("\n", ", ")
        query = f"INSERT INTO medico (nif, nome, telefone, morada, especialidade) VALUES ('{nif}', '{name}', '{phone}', '{address}', '{specialty}');"
        doctor_queries.append(query)
    return doctor_queries


def assign_doctors_to_clinics():
    assignment_queries = []
    doctors = list(generated_doc_nifs)  # Use NIFs instead of names
    doctor_clinic_day_assignments = {doctor: [] for doctor in doctors}
    clinic_day_doctor_assignments = {
        (clinic, day): [] for clinic in clinics for day in range(1, 8)
    }

    # Assign each doctor to two clinics on random days
    for doctor in doctors:
        for _ in range(2):
            clinic, day = random.choice(list(clinic_day_doctor_assignments.keys()))
            if (clinic, day) not in doctor_clinic_day_assignments[doctor]:
                doctor_clinic_day_assignments[doctor].append((clinic, day))
                clinic_day_doctor_assignments[(clinic, day)].append(doctor)

    # Ensure each clinic on each day has at least eight doctors
    for (clinic, day), assigned_doctors in clinic_day_doctor_assignments.items():
        while len(assigned_doctors) < 8:
            unassigned_doctors = [
                doctor
                for doctor in doctors
                if len(doctor_clinic_day_assignments[doctor]) < 2
            ]
            if unassigned_doctors:
                new_doctor = random.choice(unassigned_doctors)
                assigned_doctors.append(new_doctor)
                doctor_clinic_day_assignments[new_doctor].append((clinic, day))
            else:
                break

    # Generate assignment queries
    for doctor, assigned_clinic_days in doctor_clinic_day_assignments.items():
        for clinic, day in assigned_clinic_days:
            query = f"INSERT INTO trabalha (nif, nome, dia_da_semana) VALUES ('{doctor}', '{clinic}', {day});"
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
        address = fake.address().replace("\n", ", ")
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=90)
        query = f"INSERT INTO paciente (ssn, nif, nome, telefone, morada, data_nasc) VALUES ('{ssn}', '{nif}', '{name}', '{phone}', '{address}', '{birth_date}');"
        patient_queries.append(query)
    return patient_queries


def generate_appointments():

    patient_ssns = list(generated_ssns)
    doctor_nifs = list(generated_doc_nifs)
    clinic_names = list(clinics)

    # Ensure each patient has at least one consulta
    for patient_ssn in patient_ssns:
        doctor_nif = random.choice(doctor_nifs)
        clinic = random.choice(clinic_names)
        date = fake.date_between(start_date="-1y", end_date="today")
        time = fake.time()
        sns_code = "".join(
            random.choices(string.digits, k=12)
        )  # Generate a 12-digit SNS code
        while (
            sns_code in generated_sns_codes
        ):  # Regenerate SNS code if it's already been used
            sns_code = "".join(random.choices(string.digits, k=12))
        generated_sns_codes.add(sns_code)
        query = f"INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns) VALUES ('{patient_ssn}', '{doctor_nif}', '{clinic}', '{date}', '{time}', '{sns_code}');"
        consulta_queries.append(query)

    return consulta_queries


def generate_prescriptions():
    prescription_queries = []
    for consulta in consulta_queries:
        if random.random() < 0.8:
            medicines = random.randint(1, 6)
            for _ in range(medicines):
                medicine = fake.word()
                quantity = random.randint(1, 3)
                sns_code = consulta.split("'")[
                    1
                ]  # Extract the SNS code from the consulta query
                query = f"INSERT INTO receita (codigo_sns, medicamento, quantidade) VALUES ('{sns_code}', '{medicine}', {quantity});"
                prescription_queries.append(query)
    return prescription_queries


def generate_symptom_observations():
    symptom_queries = []
    for consulta in consulta_queries:
        symptoms = random.randint(1, 5)
        for _ in range(symptoms):
            symptom = random.choice(parameters_symptoms)
            id = consulta.split(" ")[2]  # Extract the ID from the consulta query
            query = f"INSERT INTO observacao (id, parametro, valor) VALUES ({id}, '{symptom}', NULL);"
            symptom_queries.append(query)
    return symptom_queries


def generate_metric_observations():
    metric_queries = []
    for consulta in consulta_queries:
        metrics = random.randint(0, 3)
        for _ in range(metrics):
            metric = random.choice(parameters_metrics)
            value = round(random.uniform(0.0, 100.0), 2)
            id = consulta.split(" ")[2]  # Extract the ID from the consulta query
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
