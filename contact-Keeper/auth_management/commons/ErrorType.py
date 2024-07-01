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
    INVALID_USERNAME = "Invalid username"
    INVALID_EMAIL = "Invalid email"
    INVALID_PASSWORD = "Invalid password"
    INVALID_USER_TYPE = "Invalid user type"
    INVALID_CODE = "Invalid code"

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
            ErrorType.INVALID_USERNAME: "Nombre de usuario inválido",
            ErrorType.INVALID_EMAIL: "Correo electrónico inválido",
            ErrorType.INVALID_PASSWORD: "Contraseña inválida",
            ErrorType.INVALID_USER_TYPE: "Tipo de usuario inválido",
            ErrorType.INVALID_CODE: "Código inválido",
            ErrorType.CONNECTION_ERROR: "Error de conexión",
            ErrorType.INTERNAL_SERVER_ERROR: "Error interno del servidor",
        }
        return translations.get(error_type, "Error desconocido")

    @staticmethod
    def english(error_type):
        return error_type
