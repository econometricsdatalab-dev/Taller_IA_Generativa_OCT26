#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crear_informe_EDL.py
Genera Base_Informe_EDL.docx con identidad visual EDL.

Requisitos:
    pip install python-docx

Antes de ejecutar:
    1. Coloca logo_EDL_oficial.png en la misma carpeta que este script.
    2. Ejecuta:  python crear_informe_EDL.py
    3. Se generará Base_Informe_EDL.docx.

Luego, en Word, guarda como plantilla .dotx:
    Archivo > Guardar como > Explorar > "Plantilla de Word (*.dotx)"
    NO cambies solo la extensión de .docx a .dotx.
"""

import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------- Paleta EDL ----------
NEGRO_BANDA = "090909"
TEXTO = "222222"
ACENTO = "F04A1D"
GRIS_CLARO = "595959"
BLANCO = "FFFFFF"

LOGO_FILE = "logo_EDL_oficial.png"
ARCHIVO_SALIDA = "Base_Informe_EDL.docx"

# ---------- Utilidades XML ----------

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def set_row_height_at_least(row, cm):
    trPr = row._tr.get_or_add_trPr()
    trHeight = OxmlElement('w:trHeight')
    trHeight.set(qn('w:val'), str(int(cm * 567)))  # twips
    trHeight.set(qn('w:hRule'), 'atLeast')
    trPr.append(trHeight)


def set_cell_margins(cell, top=60, bottom=60, left=108, right=108):
    """Márgenes internos de celda en dxa."""
    tcPr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement('w:tcMar')
    for tag, val in (('top', top), ('bottom', bottom),
                     ('start', left), ('end', right),
                     ('left', left), ('right', right)):
        node = OxmlElement(f'w:{tag}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        mar.append(node)
    tcPr.append(mar)


def add_field(paragraph, code, size=Pt(9), color=GRIS_CLARO, bold=False):
    run = paragraph.add_run()
    f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = code
    f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'end')
    run._r.append(f1); run._r.append(it); run._r.append(f2)
    run.font.size = size
    run.font.color.rgb = RGBColor.from_string(color)
    run.bold = bold
    return run


def add_run_with_field(paragraph, prefix, code, size=Pt(9), color=GRIS_CLARO):
    if prefix:
        r = paragraph.add_run(prefix)
        r.font.size = size
        r.font.color.rgb = RGBColor.from_string(color)
    add_field(paragraph, code, size=size, color=color)


# ---------- Estilos reales ----------

def configurar_estilos(doc):
    st = doc.styles

    # Normal
    normal = st['Normal']
    normal.font.name = 'Arial'
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor.from_string(TEXTO)
    rPr = normal.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts'); rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), 'Arial')
    rFonts.set(qn('w:hAnsi'), 'Arial')
    rFonts.set(qn('w:cs'), 'Arial')
    pf = normal.paragraph_format
    pf.line_spacing = 1.15
    pf.space_after = Pt(6)
    pf.space_before = Pt(0)

    # Título 1 (estilo real Heading 1, renombrado para UI en español)
    h1 = st['Heading 1']
    h1.name = 'Título 1'
    h1.font.name = 'Arial'
    h1.font.size = Pt(16)
    h1.font.bold = True
    h1.font.color.rgb = RGBColor.from_string(ACENTO)
    h1pf = h1.paragraph_format
    h1pf.space_before = Pt(18)
    h1pf.space_after = Pt(8)
    h1pf.line_spacing = 1.15
    h1pf.keep_with_next = True

    # Título 2
    h2 = st['Heading 2']
    h2.name = 'Título 2'
    h2.font.name = 'Arial'
    h2.font.size = Pt(13)
    h2.font.bold = True
    h2.font.color.rgb = RGBColor.from_string(TEXTO)
    h2pf = h2.paragraph_format
    h2pf.space_before = Pt(12)
    h2pf.space_after = Pt(6)
    h2pf.line_spacing = 1.15
    h2pf.keep_with_next = True

    # Leyenda
    nombres = [s.name for s in st]
    if 'Leyenda' not in nombres:
        leyenda = st.add_style('Leyenda', WD_STYLE_TYPE.PARAGRAPH)
    else:
        leyenda = st['Leyenda']
    leyenda.font.name = 'Arial'
    leyenda.font.size = Pt(9)
    leyenda.font.color.rgb = RGBColor.from_string(GRIS_CLARO)
    leyenda.paragraph_format.line_spacing = 1.15
    leyenda.paragraph_format.space_after = Pt(6)
    leyenda.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Tabla (estilo de párrafo para contenido de celdas)
    if 'Tabla' not in nombres:
        tabla_st = st.add_style('Tabla', WD_STYLE_TYPE.PARAGRAPH)
    else:
        tabla_st = st['Tabla']
    tabla_st.font.name = 'Arial'
    tabla_st.font.size = Pt(10)
    tabla_st.font.color.rgb = RGBColor.from_string(TEXTO)
    tabla_st.paragraph_format.line_spacing = 1.15
    tabla_st.paragraph_format.space_after = Pt(0)

    return st


# ---------- Encabezado y pie de página ----------

def configurar_encabezado_pie(section, titulo_corto):
    section.different_first_page_header_footer = True

    # Primera página (portada): encabezado y pie vacíos
    first_hp = section.first_page_header
    first_hp.is_linked_to_previous = False
    for p in list(first_hp.paragraphs):
        p.text = ''
    first_fp = section.first_page_footer
    first_fp.is_linked_to_previous = False
    for p in list(first_fp.paragraphs):
        p.text = ''

    # Encabezado del cuerpo (páginas 2 en adelante)
    hp = section.header
    hp.is_linked_to_previous = False
    for p in list(hp.paragraphs):
        p.text = ''
    p = hp.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run(titulo_corto)
    run.font.name = 'Arial'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor.from_string(GRIS_CLARO)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '2')
    bottom.set(qn('w:color'), ACENTO)
    pBdr.append(bottom)
    pPr.append(pBdr)

    # Pie de cuerpo con numeración automática: Página X de Y
    fp = section.footer
    fp.is_linked_to_previous = False
    for p in list(fp.paragraphs):
        p.text = ''
    p = fp.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run_with_field(p, 'Página ', 'PAGE')
    r = p.add_run(' de ')
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor.from_string(GRIS_CLARO)
    add_run_with_field(p, '', 'NUMPAGES')


# ---------- Portada ----------

def agregar_pagina_portada(doc, logo_file):
    # Banda negra como tabla 1x1 para controlar altura y centrado
    tabla_banda = doc.add_table(rows=1, cols=1)
    tabla_banda.alignment = WD_TABLE_ALIGNMENT.CENTER
    celda = tabla_banda.cell(0, 0)
    celda.width = Cm(16.0)  # A4 21 cm - 2.5 - 2.5
    set_cell_background(celda, NEGRO_BANDA)
    set_row_height_at_least(tabla_banda.rows[0], 4.2)
    set_cell_margins(celda, top=120, bottom=120, left=180, right=180)
    celda.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    par = celda.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(logo_file):
        # Ancho fijo, altura automática: conserva forma, colores y proporción
        par.add_run().add_picture(logo_file, width=Cm(14.0))
    else:
        run = par.add_run('[LOGO EDL - coloque logo_EDL_oficial.png]')
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        run.bold = True
        run.font.color.rgb = RGBColor.from_string(BLANCO)

    # Campos de portada centrados
    doc.add_paragraph()  # separación tras la banda
    campos = [
        ('[TÍTULO]', True, 22, ACENTO),
        ('[SUBTÍTULO]', False, 15, TEXTO),
        ('', False, 10, TEXTO),
        ('[AUTOR]', False, 12, TEXTO),
        ('[FECHA]', False, 12, TEXTO),
        ('[VERSIÓN]', False, 12, TEXTO),
    ]
    for texto, negrita, tam, color in campos:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(texto)
        run.font.name = 'Arial'
        run.font.size = Pt(tam)
        run.bold = negrita
        run.font.color.rgb = RGBColor.from_string(color)

    # Salto de página: cuerpo inicia en página 2 sin número
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.add_run().add_break(WD_BREAK.PAGE)


# ---------- Cuerpo ----------

def agregar_espacio_figura(doc, numero):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    run = p.add_run(f'[INSERTAR FIGURA {numero} AQUÍ]')
    run.font.name = 'Arial'
    run.font.size = Pt(10)
    run.italic = True
    run.font.color.rgb = RGBColor.from_string(GRIS_CLARO)

    pley = doc.add_paragraph(style='Leyenda')
    r1 = pley.add_run(f'Figura {numero}: [DESCRIPCIÓN DE LA FIGURA]   ')
    r1.font.bold = True
    r1.font.name = 'Arial'
    r2 = pley.add_run('[FUENTE]   [PERIODO]   [RESULTADO]')
    r2.font.name = 'Arial'


def agregar_tabla_indicadores(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    run = p.add_run('[Tabla editable de indicadores: modifique, agregue o elimine filas.]')
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor.from_string(GRIS_CLARO)

    tabla = doc.add_table(rows=1, cols=4)
    tabla.style = 'Table Grid'
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    ancho_col = Cm(4.0)
    headers = ['Indicador', 'Valor', 'Unidad', 'Fuente']

    for i, h in enumerate(headers):
        celda = tabla.cell(0, i)
        celda.width = ancho_col
        set_cell_background(celda, ACENTO)
        par = celda.paragraphs[0]
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.space_after = Pt(0)
        run = par.add_run(h)
        run.font.name = 'Arial'
        run.font.size = Pt(10)
        run.bold = True
        run.font.color.rgb = RGBColor.from_string(BLANCO)

    for _ in range(5):
        fila = tabla.add_row()
        for celda in fila.cells:
            celda.width = ancho_col
            par = celda.paragraphs[0]
            par.style = doc.styles['Tabla']
            par.paragraph_format.space_after = Pt(0)
            par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            par.add_run('[ ]')


def agregar_cuerpo(doc):
    secciones = [
        ('Resumen ejecutivo',
         '[Resuma aquí los hallazgos principales, el alcance del análisis y las decisiones que soporta este informe. No exceda de una página.]'),
        ('Objetivos',
         '[Describa el objetivo general y los objetivos específicos del análisis de datos.]'),
        ('Datos y fuentes',
         '[Identifique los conjuntos de datos utilizados, su origen, periodo de cobertura, frecuencia de actualización y nivel de detalle.]'),
        ('Metodología',
         '[Explique las técnicas de limpieza, transformación y análisis aplicadas, así como los criterios de validación y supuestos.]'),
        ('Resultados',
         '[Presente los resultados del análisis. Incluya a continuación la tabla de indicadores y los espacios para figuras.]'),
        ('Limitaciones',
         '[Indique restricciones de datos, sesgos, cobertura temporal o técnica que afecten la interpretación de los resultados.]'),
        ('Conclusiones',
         '[Exponga las conclusiones derivadas del análisis y posibles recomendaciones.]'),
        ('Referencias',
         '[Incluya aquí las referencias bibliográficas y fuentes documentales consultadas, siguiendo un estilo de citación uniforme.]'),
    ]

    for titulo, texto in secciones:
        doc.add_paragraph(titulo, style='Título 1')
        p = doc.add_paragraph(style='Normal')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = p.add_run(texto)
        run.font.name = 'Arial'
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor.from_string(TEXTO)

        if titulo == 'Resultados':
            agregar_tabla_indicadores(doc)
            agregar_espacio_figura(doc, 1)
            agregar_espacio_figura(doc, 2)


# ---------- Principal ----------

def main():
    doc = Document()
    configurar_estilos(doc)

    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    section.header_distance = Cm(1.25)
    section.footer_distance = Cm(1.25)

    configurar_encabezado_pie(section, 'Informe Técnico de Análisis de Datos — EDL')
    agregar_pagina_portada(doc, LOGO_FILE)
    agregar_cuerpo(doc)

    doc.save(ARCHIVO_SALIDA)
    print(f'Generado: {ARCHIVO_SALIDA}')
    print(f'Logo: {LOGO_FILE} -> {"encontrado" if os.path.exists(LOGO_FILE) else "NO ENCONTRADO (texto de reemplazo)"}')
    print('Estilos reales creados/modificados: Normal, Título 1, Título 2, Leyenda, Tabla')
    print('Formato: A4 vertical, márgenes 2.5 cm, texto #222222, acento #F04A1D, interlineado 1.15, 6 pt después de párrafo.')


if __name__ == '__main__':
    main()
