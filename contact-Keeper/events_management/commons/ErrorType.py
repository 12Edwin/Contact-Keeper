class ErrorType:
    INVALID_ID = "Invalid ID"
    INVALID_NAME = "Invalid name"
    MISSING_FIELDS = "Missing fields"
    INVALID_START_DATE = "Invalid start date"
    INVALID_END_DATE = "Invalid end date"
    INVALID_EVENT_TYPE = "Invalid event type"
    CONNECTION_ERROR = "Connection error"
    INTERNAL_SERVER_ERROR = "Internal server error"
    GROUP_NOT_FOUND = "Group not found"
    EVENT_NOT_FOUND = "Event not found"

    @staticmethod
    def spanish(error_type):
        translations = {
            ErrorType.INVALID_ID: "ID inválido",
            ErrorType.INVALID_NAME: "Nombre inválido",
            ErrorType.MISSING_FIELDS: "Faltan campos",
            ErrorType.INVALID_START_DATE: "Fecha de inicio inválida",
            ErrorType.INVALID_END_DATE: "Fecha de fin inválida",
            ErrorType.INVALID_EVENT_TYPE: "Tipo de evento inválido",
            ErrorType.GROUP_NOT_FOUND: "Grupo no encontrado",
            ErrorType.EVENT_NOT_FOUND: "Evento no encontrado",
            ErrorType.CONNECTION_ERROR: "Error de conexión",
            ErrorType.INTERNAL_SERVER_ERROR: "Error interno del servidor",
        }
        return translations.get(error_type, "Error desconocido")

    @staticmethod
    def english(error_type):
        return error_type
