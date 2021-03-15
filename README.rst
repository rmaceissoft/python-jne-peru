===============
Python JNE Peru
===============


.. image:: https://img.shields.io/pypi/v/python-jne-peru.svg
        :target: https://pypi.python.org/pypi/python-jne-peru

.. image:: https://img.shields.io/travis/rmaceissoft/pyjne_peru.svg
        :target: https://travis-ci.com/rmaceissoft/python-jne-peru




Librería de python para facilitar el acceso a la información pública relativa a los procesos
electorales de la plataforma del JNE https://plataformaelectoral.jne.gob.pe/.


* Free software: GNU General Public License v3


Instalar
--------

.. code-block::

    pip install python-jne-peru

Ejemplos de uso
-----------------

.. code-block::

    from pyjne_peru.client import JNE

    client = JNE()

    # obtener listado de los procesos electorales
    items = client.get_election_processes()
    for item in items.exclude_empty_item:
        print(item.idProcesoElectoral, item.strProcesoElectoral)

    # obtener tipos de elecciones disponibles
    # para el proceso electoral "Elecciones Generales 2021"
    items = client.get_election_types_by_process(110)
    for item in items:
        print(item.idTipoEleccion, item.strTipoEleccion)

    # obtener los expedientes para solicitud de inscripcion de listas para
    # la presidencia del proceso electoral "Elecciones Generales 2021"
    items = client.get_files_on_list(110, 1)

    # obtener los candidatos incluidos en un expediente
    # de solicitud de inscripcion de lista
    items = client.get_candidates_by_list(110, 1, 22865, 90701)

    # obtener la hoja de vida completa de un candidato
    cv = client.get_resume(135686, 110, 2840)



