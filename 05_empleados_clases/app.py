import empleados_service as ep
import streamlit as st

url = "empleados.csv"
egestor = ep.Gestor_Empleados(url)

tab_nuevo, tab_buscar, tab_departamentos_salarios = st.tabs([
    "Nuevo empleado",
    "Buscar empleado",
    "Búsqueda por departamentos o salarios"
])

with tab_nuevo:
    empleado = st.text_input("Nombre del empleado:")
    edad = st.number_input("Edad del empleado:", min_value=16, max_value=100, step=1)
    salario = st.number_input("Salario del empleado:", min_value=0.0, step=100.0)
    departamento = st.text_input("Departamento del empleado:")
    
    if st.button("Alta empleado"):
        if empleado and departamento:
            nuevo = ep.Empleado(empleado, int(edad), float(salario), departamento)
            st.toast("¡Empleado agregado!")
        else:
            st.warning("Por favor, rellena el nombre y el departamento.")

with tab_buscar:
    nombre_buscar = st.text_input("Introduce el nombre del empleado a buscar:")
    if st.button("Buscar empleado"):
        resultado = egestor.buscar_empleado(nombre_buscar)
        if resultado:
            st.success(f"**Nombre:** {resultado.nombre} | **Edad:** {resultado.edad} | **Salario:** {resultado.salario} € | **Departamento:** {resultado.departamento}")
        else:
            st.error("No se encontró ningún empleado con ese nombre.")

with tab_departamentos_salarios:
    filtro = st.radio("Tipo de filtro", ["Por departamento", "Por salarios"])
    
    if filtro == "Por departamento":
        lista_deps = egestor.departamentos()
        if lista_deps:
            dep = st.selectbox("Seleccione departamento", lista_deps)
            resultados = egestor.empleados_departamento(dep)
            # Convertimos los objetos Empleado a diccionarios con vars() para que st.dataframe los muestre bien
            st.dataframe([vars(e) for e in resultados], use_container_width=True)
        else:
            st.info("Aún no hay departamentos registrados en el archivo CSV.")
            
    else:
        sal_min = st.number_input("Salario mínimo", min_value=0.0, step=100.0)
        sal_max = st.number_input("Salario máximo", min_value=0.0, step=100.0, value=5000.0)
        if st.button("Filtrar por salario"):
            resultados = egestor.empleados_por_salarios(float(sal_min), float(sal_max))
            if resultados:
                st.dataframe([vars(e) for e in resultados], use_container_width=True)
            else:
                st.info("No hay empleados en ese rango salarial.")


# Al aplicar vars() a un objeto en Python, este se transforma en un diccionario (dict) 
# que contiene sus atributos de instancia y sus valores (extraídos de su atributo interno __dict__).
# Si tienes una lista de objetos (por ejemplo, instancias de una clase o un @dataclass), 
# aplicar vars(obj) a cada uno los convierte en una lista de diccionarios, que es precisamente 
# el formato ideal para que st.dataframe() muestre los nombres de los atributos como encabezados de columna.

# ¿Cómo funciona la transformación?

# 1. Un solo objeto: vars(objeto) devuelve un diccionario { "atributo": valor }.
# 2. Lista de objetos: [vars(obj) for obj in lista_objetos] devuelve una lista de diccionarios, 
# donde cada objeto pasa a ser una fila de la tabla.