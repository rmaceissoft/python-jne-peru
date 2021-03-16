import requests

from .parsers import EntityParser
from .error import JNEException


class JNE:
    """
    Plataforma Electoral JNE API
    """

    def __init__(self, parser=None):
        self.base_url = "https://plataformaelectoral.jne.gob.pe"
        self.parser = parser or EntityParser()

    def _build_url(self, path):
        return f"{self.base_url}{path}"

    def _make_request(self, method, path, payload_type=None, payload_list=False,
                      post_data=None, params=None, **kwargs):
        request_method = requests.post if method == "POST" else requests.get
        response = request_method(self._build_url(path), params=params or {}, data=post_data or {})
        if response.status_code != 200:
            raise JNEException(f"JNE error response: status code = {response.status_code}")

        result = self.parser.parse(response.json(), payload_list=payload_list, payload_type=payload_type)
        return result

    def get_electoral_districts(self):
        """
        Note: Este metodo no devuelve todos los distritos electorales disponibles.
        Por ejemplo. PERUANOS RESIDENTES EN EL EXTERIOR (140101)
        """
        return self._make_request(
            "GET", "/Candidato/ListUbigeoDepartamento",
            payload_type="electoral_district", payload_list=True)

    def get_election_processes(self):
        return self._make_request(
            "GET", "/Resoluciones/GetListProcesosCR",
        payload_type="election_process", payload_list=True)

    def get_election_types_by_process(self, proceso_electoral: int):
        return self._make_request(
            "GET", f"/Candidato/GetTipoEleccionbyProceso/{proceso_electoral}",
            payload_type="election_type", payload_list=True)

    def get_files(self, jurado_electoral: int = 0, organizacion_politica: int = 0,
                        proceso_electoral: int = 0, tipo_expediente: int = 0, ubigeo: str = "000000"):
        return self._make_request(
            "POST", "/Expediente/BusquedaReporteAvanzadoExpediente",
            payload_type="file", payload_list=True,
            post_data={
                "idJuradoElectoral": jurado_electoral,
                "idOrganizacionPolitica": organizacion_politica,
                "idProcesoElectoral": proceso_electoral,
                "idTipoExpediente": tipo_expediente,
                "strUbigeo": ubigeo
            })

    def get_files_on_list(self, proceso_electoral: int, tipo_eleccion: int,
                          jurado_electoral: int = 0, distrito_electoral: int = 0):
        if not distrito_electoral:
            distrito_electoral = "null"
        path = f"/Candidato/GetExpedientesLista/" \
               f"{proceso_electoral}-{tipo_eleccion}-{distrito_electoral}------{jurado_electoral}-"
        return self._make_request(
            "GET", path,
            payload_type="file", payload_list=True,
        )

    def get_file(self, cod_expediente_ext: str):
        return self._make_request(
            "POST", "/Expediente/BuscandoCodigo",
            payload_type="file_extended", payload_list=False,
            post_data={
                "strNumExpedienteFiltro": cod_expediente_ext
            }
        )

    def get_candidates_by_list(self, proceso_electoral: int, tipo_eleccion: int,
                               id_solicitud: int, id_expediente: int):
        path = f"/Candidato/GetCandidatos/{tipo_eleccion}-{proceso_electoral}-{id_solicitud}-{id_expediente}"
        return self._make_request(
            "GET", path, payload_type="candidate", payload_list=True
        )

    def get_resume(self, id_hoja_vida: int, proceso_electoral: int,
                   id_organizacion_poitica: int):
        params = {
            "param": f"{id_hoja_vida}-0-{id_organizacion_poitica}-{proceso_electoral}"
        }
        return self._make_request(
            "GET", "/HojaVida/GetHVConsolidado", params=params, payload_type="resume",
            payload_list=False
        )

    def get_resume_personal_info(self, id_hoja_vida: int, proceso_electoral: int,
                   id_organizacion_poitica: int):
        params = {
            "param": f"{id_hoja_vida}-0-{id_organizacion_poitica}-{proceso_electoral}"
        }
        return self._make_request(
            "GET", "/HojaVida/GetAllHVDatosPersonales", params=params, payload_type="personal_info",
            payload_list=True
        )

    def _get_section_at_resume(self, resume_subpath: str, payload_type: str,
                               id_hoja_vida: int, order: str = 'ASC'):
        params = {
            "Ids": f"{id_hoja_vida}-0-{order}"
        }
        return self._make_request(
            "GET", f"/HojaVida/{resume_subpath}", params=params, payload_type=payload_type,
            payload_list=True
        )

    def get_resume_penal_sentence(self, id_hoja_vida: int, order: str = 'ASC'):
        return self._get_section_at_resume("GetAllHVSentenciaPenal", "penal_sentence", id_hoja_vida, order)

    def get_resume_obligation_sentence(self, id_hoja_vida, order: str = 'ASC'):
        return self._get_section_at_resume("GetAllHVSentenciaObliga", "obligation_sentence", id_hoja_vida, order)

    def get_resume_university_education(self, id_hoja_vida: int, order: str = 'ASC'):
        return self._get_section_at_resume("GetAllHVEduUniversitaria", "university_education", id_hoja_vida, order)

    def get_resume_postgraduate_education(self, id_hoja_vida: int, order: str = 'ASC'):
        return self._get_section_at_resume("GetAllHVPosgrado", "postgraduate_education", id_hoja_vida, order)

    def get_resume_immovable_property(self, id_hoja_vida: int, order: str = 'ASC'):
        return self._get_section_at_resume("GetAllHVBienInmueble", "immovable_property", id_hoja_vida, order)

    def get_resume_movable_property(self, id_hoja_vida: int, order: str = 'ASC'):
        return self._get_section_at_resume("GetAllHVBienMueble", "movable_property", id_hoja_vida, order)

    def get_resume_basic_education(self, id_hoja_vida: int, order: str = 'ASC'):
        return self._get_section_at_resume("GetAllHVEduBasica", "basic_education", id_hoja_vida, order)

    def get_resume_non_university_education(self, id_hoja_vida: int, order: str = 'ASC'):
        return self._get_section_at_resume("GetAllHVNoUniversitaria", "non_university_education", id_hoja_vida, order)

    def get_resume_technical_education(self, id_hoja_vida: int, order: str = 'ASC'):
        return self._get_section_at_resume("GetAllHVEduTecnico", "technical_education", id_hoja_vida, order)

    def get_resume_additional_information(self, id_hoja_vida: int, order: str = 'ASC'):
        return self._get_section_at_resume("GetAllHVInfoAdicional", "additional_information", id_hoja_vida, order)

    def get_resume_professional_experience(self, id_hoja_vida: int, order: str = 'ASC'):
        return self._get_section_at_resume("GetAllHVExpeLaboral", "professional_experience", id_hoja_vida, order)

    def get_resume_partisan_position(self, id_hoja_vida: int, order: str = 'ASC'):
        return self._get_section_at_resume("GetAllHVCargoPartidario", "partisan_position", id_hoja_vida, order)

    def get_resume_resignation_political_organization(self, id_hoja_vida: int, order: str = 'ASC'):
        return self._get_section_at_resume("GetHVRenunciaOP", "resignation_political_organization", id_hoja_vida, order)
