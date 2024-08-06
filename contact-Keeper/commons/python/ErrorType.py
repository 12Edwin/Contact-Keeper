class ErrorType:
    INVALID_USERNAME = "Invalid username"
    USER_NOT_FOUND = "User not found"
    INVALID_ID = "Invalid ID"
    INVALID_NAME = "Invalid name"
    INVALID_SURNAME = "Invalid surname"
    INVALID_LAST_NAME = "Invalid last name"
    INVALID_BIRTHDAY = "Invalid birthday"
    INVALID_PHONE = "Invalid phone"
    MISSING_FIELDS = "Missing fields"
    INVALID_START_DATE = "Invalid start date"
    INVALID_END_DATE = "Invalid end date"
    INVALID_EVENT_TYPE = "Invalid event type"
    INVALID_PASSWORD = "Invalid password"
    INVALID_USER_TYPE = "Invalid user type"
    INVALID_TITLE = "Invalid title"
    INVALID_NOTES = "Invalid notes"
    INVALID_REMINDER = "Invalid reminder"
    CONNECTION_ERROR = "Connection error"
    INTERNAL_SERVER_ERROR = "Internal server error"
    GROUP_NOT_FOUND = "Group not found"
    EVENT_NOT_FOUND = "Event not found"

    @staticmethod
    def spanish(error_type):
        translations = {
            ErrorType.INVALID_USERNAME: "Nombre de usuario inválido",
            ErrorType.USER_NOT_FOUND: "Usuario no encontrado",
            ErrorType.INVALID_ID: "ID inválido",
            ErrorType.INVALID_NAME: "Nombre inválido",
            ErrorType.INVALID_SURNAME: "Apellido inválido",
            ErrorType.INVALID_LAST_NAME: "Apellido materno inválido",
            ErrorType.INVALID_BIRTHDAY: "Fecha de nacimiento inválida",
            ErrorType.INVALID_PHONE: "Teléfono inválido",
            ErrorType.MISSING_FIELDS: "Faltan campos",
            ErrorType.INVALID_START_DATE: "Fecha de inicio inválida",
            ErrorType.INVALID_END_DATE: "Fecha de fin inválida",
            ErrorType.INVALID_EVENT_TYPE: "Tipo de evento inválido",
            ErrorType.INVALID_PASSWORD: "Contraseña inválida",
            ErrorType.INVALID_USER_TYPE: "Tipo de usuario inválido",
            ErrorType.INVALID_TITLE: "Título inválido",
            ErrorType.INVALID_NOTES: "Notas inválidas",
            ErrorType.INVALID_REMINDER: "Recordatorio inválido",
            ErrorType.GROUP_NOT_FOUND: "Grupo no encontrado",
            ErrorType.EVENT_NOT_FOUND: "Evento no encontrado",
            ErrorType.CONNECTION_ERROR: "Error de conexión",
            ErrorType.INTERNAL_SERVER_ERROR: "Error interno del servidor",
        }
        return translations.get(error_type, "Error desconocido")

    @staticmethod
    def english(error_type):
        return error_type
