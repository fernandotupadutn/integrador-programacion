import os
import csv
import unicodedata

# Nombre del archivo CSV donde se guardará el catálogo de países
nombre_archivo = 'paises.csv'

# ------------------ UTILIDADES ------------------

def normalizar(texto):
    """
    Normaliza un texto:
    - Convierte a minúsculas
    - Quita espacios extra
    - Elimina acentos (ej: 'América' -> 'america')
    """
    texto = " ".join(texto.strip().lower().split())
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto

def crear_sino_existe():
    """
    Crea el archivo CSV si no existe.
    Escribe los encabezados: nombre, poblacion, superficie, continente.
    """
    if not os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['nombre', 'poblacion', 'superficie', 'continente'])

def leer_archivo():
    """
    Lee el archivo CSV y devuelve una lista de diccionarios con los países.
    Valida que población y superficie sean números enteros antes de convertirlos.
    """
    crear_sino_existe()
    paises_catalogo = []
    with open(nombre_archivo, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            if fila['nombre'] and fila['poblacion'].isdigit() and fila['superficie'].isdigit():
                paises_catalogo.append({
                    'nombre': fila['nombre'],
                    'poblacion': int(fila['poblacion']),
                    'superficie': int(fila['superficie']),
                    'continente': fila['continente']
                })
    return paises_catalogo

def guardar_archivo(paises_catalogo):
    """
    Guarda la lista de países en el archivo CSV.
    Sobrescribe el archivo con los datos actualizados (persistencia).
    """
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['nombre','poblacion','superficie','continente'])
        writer.writeheader()
        writer.writerows(paises_catalogo)

def buscar_pais(paises_catalogo, nombre):
    """
    Busca un país por nombre (coincidencia parcial o exacta).
    Devuelve una lista con los países encontrados.
    """
    nombre_norm = normalizar(nombre)
    return [p for p in paises_catalogo if nombre_norm in normalizar(p['nombre'])]

# ------------------ CLAVES DE ORDENAMIENTO  ------------------

def clave_nombre(pais):
    """Devuelve el nombre del país (para ordenar alfabéticamente)."""
    return pais['nombre']

def clave_poblacion(pais):
    """Devuelve la población del país (para ordenar por cantidad de habitantes)."""
    return pais['poblacion']

def clave_superficie(pais):
    """Devuelve la superficie del país (para ordenar por extensión territorial)."""
    return pais['superficie']

# ------------------ FUNCIONES PRINCIPALES ------------------

def agregar_pais(paises_catalogo):
    """
    Agrega un nuevo país al catálogo:
    - Solicita nombre, población, superficie y continente.
    - Valida que los datos sean correctos y no vacíos.
    - Evita duplicados por nombre.
    - Guarda los cambios en el CSV.
    """
    nombre = input("Nombre del país: ").strip()
    if not nombre:
        print("Nombre vacío.")
        return
    if buscar_pais(paises_catalogo, nombre):
        print("El país ya existe.")
        return
    poblacion = input("Población: ")
    superficie = input("Superficie: ")
    continente = input("Continente: ").strip()
    if not (poblacion.isdigit() and superficie.isdigit()) or not continente:
        print("Datos inválidos.")
        return
    paises_catalogo.append({
        'nombre': nombre,
        'poblacion': int(poblacion),
        'superficie': int(superficie),
        'continente': continente
    })
    guardar_archivo(paises_catalogo)
    print("País agregado.")

def actualizar_pais(paises_catalogo):
    """
    Actualiza los datos de población y superficie de un país existente.
    Toma el primer país que coincida con la búsqueda (parcial o exacta).
    """
    nombre = input("País a actualizar: ")
    encontrados = buscar_pais(paises_catalogo, nombre)
    if not encontrados:
        print("No encontrado.")
        return
    pais = encontrados[0]
    poblacion = input("Nueva población: ")
    superficie = input("Nueva superficie: ")
    if poblacion.isdigit() and superficie.isdigit():
        pais['poblacion'] = int(poblacion)
        pais['superficie'] = int(superficie)
        guardar_archivo(paises_catalogo)
        print("Datos actualizados.")
    else:
        print("Valores inválidos.")

def mostrar_catalogo(paises_catalogo):
    """Muestra todos los países cargados en el catálogo."""
    for p in paises_catalogo:
        print(p)

def filtrar_continente(paises_catalogo):
    """Filtra países por continente ingresado por el usuario (comparación normalizada)."""
    cont = input("Continente: ")
    filtrados = [p for p in paises_catalogo if normalizar(cont) == normalizar(p['continente'])]
    print(filtrados if filtrados else "Ningún país encontrado.")

def filtrar_poblacion(paises_catalogo):
    """Filtra países dentro de un rango de población [mínimo, máximo]."""
    minimo = int(input("Población mínima: "))
    maximo = int(input("Población máxima: "))
    filtrados = [p for p in paises_catalogo if minimo <= p['poblacion'] <= maximo]
    print(filtrados if filtrados else "Ningún país encontrado.")

def filtrar_superficie(paises_catalogo):
    """Filtra países dentro de un rango de superficie [mínimo, máximo]."""
    minimo = int(input("Superficie mínima: "))
    maximo = int(input("Superficie máxima: "))
    filtrados = [p for p in paises_catalogo if minimo <= p['superficie'] <= maximo]
    print(filtrados if filtrados else "Ningún país encontrado.")

def ordenar_por_nombre(paises_catalogo):
    """Ordena y muestra países por nombre alfabético (A→Z)."""
    for p in sorted(paises_catalogo, key=clave_nombre):
        print(p)

def ordenar_por_poblacion(paises_catalogo):
    """Ordena y muestra países por población (ascendente)."""
    for p in sorted(paises_catalogo, key=clave_poblacion):
        print(p)

def ordenar_por_superficie(paises_catalogo, asc=True):
    """
    Ordena y muestra países por superficie.
    - asc=True: ascendente.
    - asc=False: descendente.
    """
    for p in sorted(paises_catalogo, key=clave_superficie, reverse=not asc):
        print(p)

def estadisticas(paises_catalogo):
    """
    Calcula y muestra estadísticas básicas:
    - País con mayor y menor población.
    - Promedio de población.
    - Promedio de superficie.
    - Cantidad de países por continente.
    """
    if not paises_catalogo:
        print("Catálogo vacío.")
        return
    mayor = max(paises_catalogo, key=clave_poblacion)
    menor = min(paises_catalogo, key=clave_poblacion)
    prom_pob = sum(p['poblacion'] for p in paises_catalogo) / len(paises_catalogo)
    prom_sup = sum(p['superficie'] for p in paises_catalogo) / len(paises_catalogo)
    continentes = {}
    for p in paises_catalogo:
        continentes[p['continente']] = continentes.get(p['continente'], 0) + 1
    print("Mayor población:", mayor)
    print("Menor población:", menor)
    print("Promedio población:", prom_pob)
    print("Promedio superficie:", prom_sup)
    print("Cantidad por continente:", continentes)

# ------------------ MENÚ ------------------

def menu():
    """
    Menú principal del programa:
    - Ofrece todas las opciones requeridas.
    - Ejecuta la acción seleccionada y vuelve al menú hasta salir.
    """
    paises_catalogo = leer_archivo()
    while True:
        print("\n--- MENÚ ---")
        print("1. Agregar país")
        print("2. Actualizar datos de un país")
        print("3. Buscar país por nombre")
        print("4. Filtrar por continente")
        print("5. Filtrar por rango de población")
        print("6. Filtrar por rango de superficie")
        print("7. Ordenar países")
        print("8. Mostrar estadísticas")
        print("9. Mostrar catálogo")
        print("0. Salir")
        opcion = input("Opción: ")
        match opcion:
            case "1": agregar_pais(paises_catalogo)
            case "2": actualizar_pais(paises_catalogo)
            case "3": 
                nombre = input("Nombre: ")
                resultados = buscar_pais(paises_catalogo, nombre)
                if resultados:
                    print(resultados)
                else:
                    print("El país ingresado no existe en el catálogo.")

            case "4": filtrar_continente(paises_catalogo)
            case "5": filtrar_poblacion(paises_catalogo)
            case "6": filtrar_superficie(paises_catalogo)
            case "7":
                # Submenú de ordenamiento
                print("a) Nombre\nb) Población\nc) Superficie asc\nd) Superficie desc")
                sub = input("Elija: ")
                if sub=="a": ordenar_por_nombre(paises_catalogo)
                elif sub=="b": ordenar_por_poblacion(paises_catalogo)
                elif sub=="c": ordenar_por_superficie(paises_catalogo, asc=True)
                elif sub=="d": ordenar_por_superficie(paises_catalogo, asc=False)
            case "8": estadisticas(paises_catalogo)
            case "9": mostrar_catalogo(paises_catalogo)
            case "0":
                # Salida limpia del programa
                print("Fin del programa."); break
            case _:
                # Opción no válida: se informa y continúa el bucle
                print("Opción inválida.")

# Punto de entrada: ejecuta el menú al iniciar el script
menu()
