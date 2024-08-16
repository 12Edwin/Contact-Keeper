from database import get_db_connection
from type_response import response_200, response_400, response_500, response_403, response_401
from ErrorType import ErrorType
from utils import validate_id, validate_event_type, validate_start_date, exists_by_id, validate_name, exists_user, validate_notes_meeting, validate_title_meeting, validate_role_meeting, validate_location, validate_end_date, exists_group, validate_description, validate_email, validate_password, validate_birthday, validate_phone, validate_nickname, validate_user_type, validate_opt_name, exists_event, exists_user_phone, exists_user_nick, validate_status_event
from read_pool import get_cognito_ids