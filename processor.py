import xml.etree.ElementTree as ET
import csv
from io import BytesIO, StringIO

def xml_to_csv(xml_content: bytes) -> BytesIO:
    tree = ET.ElementTree(ET.fromstring(xml_content))
    root = tree.getroot()

    rows = []

    for mutacion in root.findall('.//mutacion_rectificacion'):
        tipo_tramite = mutacion.findtext('tipo_tramite', '')
        radicado = mutacion.findtext('radicado', '')
        resolucion = mutacion.findtext('resolucion', '')
        fecha_resolucion = mutacion.findtext('fecha_resolucion', '')
        ente_emisor = mutacion.findtext('ente_emisor', '')

        for tipo, origen_predio in [
            ('predios_actualizados', 'actualizacion'),
            ('predios_inscritos', 'inscritos')
        ]:
            for predio in mutacion.findall(f'{tipo}/predio'):
                predio_data = {
                    'tipo_tramite': tipo_tramite,
                    'radicado': radicado,
                    'resolucion': resolucion,
                    'fecha_resolucion': fecha_resolucion,
                    'ente_emisor': ente_emisor,
                    'origen_predio': origen_predio,
                    'departamento': predio.findtext('departamento', ''),
                    'municipio': predio.findtext('municipio', ''),
                    'codigo_predial_nacional': predio.findtext('codigo_predial_nacional', ''),
                    'codigo_predial_anterior': predio.findtext('codigo_predial_anterior', ''),
                    'codigo_homologado': predio.findtext('codigo_homologado', ''),
                    'matricula_inmobiliaria': predio.findtext('matricula_inmobiliaria', ''),
                    'direccion': predio.findtext('direccion', ''),
                    'area_terreno': predio.findtext('area_terreno', ''),
                    'area_construida': predio.findtext('area_construida', ''),
                    'destino_economico': predio.findtext('destino_economico', ''),
                    'condicion_predio': predio.findtext('condicion_predio', ''),
                    'tipo_predio': predio.findtext('tipo_predio', ''),
                    'tipo_derecho': predio.findtext('tipo_derecho', ''),
                }

                avaluos = predio.find('avaluos_catastrales')
                avaluo_list = []
                if avaluos is not None:
                    for av in avaluos.findall('avaluo_catastral'):
                        avaluo_list.append({
                            'avaluo': av.findtext('avaluo', ''),
                            'vigencia': av.findtext('vigencia', '')
                        })

                personas_naturales = predio.findall('interesados/persona_natural')
                personas_juridicas = predio.findall('interesados/persona_juridica')
                persona_list = []

                for p in personas_naturales:
                    persona_list.append({
                        'persona_juridica.documento': "",
                        'persona_juridica.numero_documento': '',
                        'persona_juridica.razon_social': "",
                        'documento': p.findtext('documento', ''),
                        'numero_documento': p.findtext('numero_documento', ''),
                        'primer_nombre': p.findtext('primer_nombre', ''),
                        'segundo_nombre': p.findtext('segundo_nombre', ''),
                        'primer_apellido': p.findtext('primer_apellido', ''),
                        'segundo_apellido': p.findtext('segundo_apellido', ''),
                    })

                for p in personas_juridicas:
                    persona_list.append({
                        'persona_juridica.documento': p.findtext('documento'),
                        'persona_juridica.numero_documento': p.findtext('numero_documento'),
                        'persona_juridica.razon_social': p.findtext('razon_social'),
                        'documento': "",
                        'numero_documento': "",
                        'primer_nombre': "",
                        'segundo_nombre': "",
                        'primer_apellido': "",
                        'segundo_apellido': "",
                    })

                for avaluo in avaluo_list:
                    for persona in persona_list:
                        row = {**predio_data, **avaluo, **persona}
                        rows.append(row)

    # Crear CSV en memoria
    output = StringIO()
    if rows:
        headers = rows[0].keys()
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    else:
        writer = csv.writer(output)
        writer.writerow(["mensaje"])
        writer.writerow(["No se encontraron datos para exportar."])

    # Convertir a BytesIO para respuesta
    csv_bytes = BytesIO(output.getvalue().encode("utf-8"))
    output.close()
    return csv_bytes
