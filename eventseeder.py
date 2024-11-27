from datetime import datetime, timedelta
from api.models import Evento  # Asegúrate de usar el nombre correcto de tu app

# Fecha inicial y final
fecha_inicio = datetime(2024, 6, 1)
fecha_fin = datetime(2024, 12, 1)

# Crear evento de inicio de clases
Evento.objects.create(
    titulo="Inicio de Clases",
    descripcion="Inicio del semestre académico.",
    tipo="inicio_clases",
    fecha_inicio=fecha_inicio,
    fecha_fin=fecha_inicio,
)

# Crear evento de fin de clases
Evento.objects.create(
    titulo="Fin de Clases",
    descripcion="Cierre del semestre académico.",
    tipo="fin_clases",
    fecha_inicio=fecha_fin,
    fecha_fin=fecha_fin,
)

print("Eventos creados con éxito.")

# Generar eventos de exámenes cada mes entre junio y diciembre
for i in range(6):  # 6 meses entre junio y diciembre
    fecha_examen = fecha_inicio + timedelta(days=i * 30)
    Evento.objects.create(
        titulo=f"Exámenes del Mes {fecha_examen.strftime('%B')}",
        descripcion=f"Exámenes programados para el mes de {fecha_examen.strftime('%B')}.",
        tipo="examen",
        fecha_inicio=fecha_examen,
        fecha_fin=fecha_examen + timedelta(days=1),  # Un día de duración
    )

print("Eventos de exámenes creados con éxito.")
