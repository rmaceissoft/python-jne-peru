from .utils import parse_date, parse_datetime


class ResultSet(list):
    pass


class ResultSetWithEmptyItems(ResultSet):

    def __init__(self, empty_item_comparison_attribute, empty_item_comparison_value):
        self.empty_item_comparison_attribute = empty_item_comparison_attribute
        self.empty_item_comparison_value = empty_item_comparison_value

    @property
    def exclude_empty_item(self):
        return [item for item in self if getattr(item, self.empty_item_comparison_attribute) != self.empty_item_comparison_value]


class Entity:

    @classmethod
    def get_result_set_class_instance(cls):
        if hasattr(cls, 'empty_item_comparison_attribute') and hasattr(cls, 'empty_item_comparison_value'):
            return ResultSetWithEmptyItems(
                cls.empty_item_comparison_attribute, cls.empty_item_comparison_value)
        return ResultSet()

    def __getstate__(self):
        # pickle
        pickle = dict(self.__dict__)
        return pickle

    def __getattr__(self, name):
        """
        invoken when referring to attribute that it is not valid or it was not present at json response
        """
        return None

    @classmethod
    def parse(cls, json):
        """Parse a JSON object into an entity instance."""
        instance = cls()
        for k, v in json.items():
            if hasattr(cls, 'extra_parsers') and k in cls.extra_parsers:
                func = cls.extra_parsers[k]
                setattr(instance, k, func(v))
            else:
                setattr(instance, k, v)
        return instance

    @classmethod
    def parse_list(cls, json):
        results = cls.get_result_set_class_instance()
        total = 0
        items = json or []
        for obj in items:
            results.append(cls.parse(obj))
            total += 1
        # hold the count of items
        results.total = total
        return results


class ElectionProcess(Entity):
    empty_item_comparison_attribute = "idProcesoElectoral"
    empty_item_comparison_value = 0

    @property
    def fechaAperturaProceso(self):
        return parse_date(self.strFechaAperturaProceso)

    @property
    def fechaConvocatoria(self):
        return parse_date(self.strFechaConvocatoria)

    @property
    def fechaCierreProceso(self):
        return parse_date(self.strFechaCierreProceso)

    @property
    def fechaRegistro(self):
        return parse_datetime(self.strFechaRegistro, format="%d/%m/%Y %H:%M:%S %p")


class ElectionType(Entity):
    pass


class ElectoralDistrict(Entity):
    pass


class Candidate(Entity):

    @property
    def fechaNacimiento(self):
        return parse_datetime(self.strFechaNacimiento, format="%d/%m/%Y %H:%M:%S %p")


class ProceduralPart(Entity):
    pass


class Document(Entity):
    pass


class File(Entity):

    extra_parsers = {
        'lParteProcesal': ProceduralPart.parse_list
    }


class FileExtended(Entity):

    extra_parsers = {
        'oExpediente': File.parse,
        'lReporteBusquedaExpediente': Document.parse_list,  # documents
        'lCandidatosExpediente': Candidate.parse_list,  # candidates
        'lAsociadosPadre': File.parse_list,  # files related directly
        'lAsociadosHijos': File.parse_list,  # other files related (procedural part)
    }


class MovableProperty(Entity):
    pass


class ImmovableProperty(Entity):
    empty_item_comparison_attribute = "strTengoInmueble"
    empty_item_comparison_value = "2"


class BasicEducation(Entity):
    pass


class PartisanPosition(Entity):
    empty_item_comparison_attribute = "strTengoCargoPartidario"
    empty_item_comparison_value = "2"

    @property
    def anioCargoPartiDesde(self):
        try:
            value = int(self.strAnioCargoPartiDesde)
        except ValueError:
            value = None
        return value

    @property
    def anioCargoPartiHasta(self):
        try:
            value = int(self.strAnioCargoPartiHasta)
        except ValueError:
            value = None
        return value


class UniversityEducation(Entity):

    @property
    def anioBachiller(self):
        try:
            value = int(self.strAnioBachiller)
        except ValueError:
            value = None
        return value


class NonUniversityEducation(Entity):
    pass


class PostgraduateEducation(Entity):

    @property
    def anioPosgrado(self):
        try:
            value = int(self.strAnioPosgrado)
        except ValueError:
            value = None
        return value


class TechnicalEducation(Entity):
    pass


class ProfessionalExperience(Entity):
    empty_item_comparison_attribute = "strTengoExpeLaboral"
    empty_item_comparison_value = "2"

    @property
    def anioTrabajoDesde(self):
        try:
            value = int(self.strAnioTrabajoDesde)
        except ValueError:
            value = None
        return value

    @property
    def anioTrabajoHasta(self):
        try:
            value = int(self.strAnioTrabajoHasta)
            if value == 0:
                # '0000' is handled as None
                value = None
        except ValueError:
            value = None
        return value


class ResignationPoliticalOrganization(Entity):
    pass


class ObligationSentence(Entity):
    empty_item_comparison_attribute = "strTengoSentenciaObliga"
    empty_item_comparison_value = "2"


class PenalSentence(Entity):
    empty_item_comparison_attribute = "strTengoSentenciaPenal"
    empty_item_comparison_value = "2"

    @property
    def fechaSentenciaPenal(self):
        return parse_date(self.strFechaSentenciaPenal)


class PersonalInfo(Entity):

    @property
    def feTerminoRegistro(self):
        return parse_datetime(self.strFeTerminoRegistro)

    @property
    def fechaNacimiento(self):
        return parse_date(self.strFechaNacimiento)


class AdditionalInformation(Entity):
    pass


class Income(Entity):

    @property
    def is_empty(self):
        return self.strTengoIngresos == "2"


class Resume(Entity):

    extra_parsers = {
        'lBienInmueble': ImmovableProperty.parse_list,
        'lBienMueble': MovableProperty.parse_list,
        'lCargoPartidario': PartisanPosition.parse_list,
        'lEduUniversitaria': UniversityEducation.parse_list,
        'lExperienciaLaboral': ProfessionalExperience.parse_list,
        'lRenunciaOP': ResignationPoliticalOrganization.parse_list,
        'lSentenciaObliga': ObligationSentence.parse_list,
        'lSentenciaPenal': PenalSentence.parse_list,
        'oDatosPersonales': PersonalInfo.parse,
        'oEduBasica': BasicEducation.parse,
        'oEduNoUniversitaria': NonUniversityEducation.parse,
        'oEduPosgrago': PostgraduateEducation.parse,
        'oEduTecnico': TechnicalEducation.parse,
        'oInfoAdicional': AdditionalInformation.parse,
        'oIngresos': Income.parse,
    }


class EntityFactory:
    election_process = ElectionProcess
    election_type = ElectionType
    electoral_district = ElectoralDistrict
    file = File
    file_extended = FileExtended
    candidate = Candidate
    resume = Resume
    personal_info = PersonalInfo
    penal_sentence = PenalSentence
    university_education = UniversityEducation
    postgraduate_education = PostgraduateEducation
    obligation_sentence = ObligationSentence
    immovable_property = ImmovableProperty
    movable_property = MovableProperty
    basic_education = BasicEducation
    non_university_education = NonUniversityEducation
    technical_education = TechnicalEducation
    additional_information = AdditionalInformation
    professional_experience = ProfessionalExperience
    partisan_position = PartisanPosition
    resignation_political_organization = ResignationPoliticalOrganization
