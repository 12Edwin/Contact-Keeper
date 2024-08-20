import { jwtDecode } from "jwt-decode";
import CryptoJS from "crypto-js";
const moment = require('moment-timezone');
const getUserByName = (name, people) => {
  return people.some((person) => person.name === name);
};

const getUserByEmail = (email, people) => {
  return people.some((person) => person.email === email);
};

const getToken = () => {
  return localStorage.getItem("token");
};

const getSubFromToken = () => {
  const token = getToken(); 
  if (!token) {
    window.location.href = "/login";
    return null;
  }
  try {
    const decodedToken = jwtDecode(token);
    return decodedToken.sub; 
  } catch (error) {
    return null;
  }
};

const encrypt = (text) =>{
  return CryptoJS.AES.encrypt(text, process.env.VUE_APP_SECRET).toString()
}

const decrypt = (text) => {
  const bytes = CryptoJS.AES.decrypt(text, process.env.VUE_APP_SECRET);
  return bytes.toString(CryptoJS.enc.Utf8);
}

const removeToken = () => {
  return localStorage.removeItem("token");
};
const getRoleStorage= () => {
  try {
      const encodedRole = localStorage.getItem('role');

      if (!encodedRole) {
          throw new Error('No role found');
      }
      const decodedRole = decrypt(encodedRole);
      return decodedRole
  } catch (error) {
      removeToken();
  }
};

const getUserFromToke = () => {
  const token = getToken();
  if (!token) {
    return null;
  }

  return jwtDecode(token).name;
}

const getEmailFromToke = () => {
  const token = getToken();
  if (!token) {
    return null;
  }

  return jwtDecode(token).email;
}


const getIdUserFromToke = () =>{
  const token = getToken();
  if (!token) {
    window.location.href = "/login";
    return null;
  }

  return jwtDecode(token).sub;
}

const validAge = (birthday) => {
  return true
}

const filterByName = (array, name) => {
  return array.filter((item) => item.name.toLowerCase().includes(name.toLowerCase()));
}

const messageError = (error) =>{
  let wrongField;
  switch (error) {
    case "User already exists":
    case "Invalid username":
      wrongField = { field: "username", formPart: 1 };
      break;
    case "Invalid surname":
      wrongField = { field: "surname", formPart: 1 };
      break;
    case "Invalid name":
      wrongField = { field: "name", formPart: 1 };
      break;
    case "Invalid last name":
      wrongField = { field: "lastname", formPart: 1 };
      break;
    case "Invalid birthday":
      wrongField = { field: "birthday", formPart: 2 };
      break;
    case "Invalid phone":
      wrongField = { field: "phone", formPart: 2 };
      break;
    case "Invalid email":
      wrongField = { field: "email", formPart: 2 };
      break;
  }
  return wrongField
}

const getErrorMessages = (errorCode) => {
  const errorMessages = {
    "User already exists": "El usuario ya existe",
    "Invalid username": "Nombre de usuario inválido",
    "Invalid surname": "Apellido inválido",
    "Invalid name": "Nombre inválido",
    "Invalid last name": "Apellido inválido",
    "Invalid birthday": "Fecha de nacimiento inválida",
    "Invalid phone": "Teléfono inválido",
    "Invalid email": "Correo inválido",
    "Invalid password": "Credenciales inválidas",
    "Invalid end date": "Fecha de fin inválida",
    "Invalid start date": "Fecha de inicio inválida",
    "Invalid event status": "Estado del evento inválido",
    "User not found": "Usuario no encontrado",
    "Invalid ID": "ID inválido",
    "Missing fields": "Faltan campos",
    "Invalid event type": "Tipo de evento inválido",
    "Invalid user type": "Tipo de usuario inválido",
    "Invalid title": "Título inválido",
    "Invalid notes": "Notas inválidas",
    "Invalid reminder": "Recordatorio inválido",
    "Connection error": "Error de conexión",
    "Internal server error": "Error interno del servidor",
    "Group not found": "Grupo no encontrado",
    "Event not found": "Evento no encontrado"
  }
  return errorMessages[errorCode] || 'Ocurrió un error desconocido en el servidor';
}

function extractDateAndTime(dateTimeString) {
  const momentDate = moment(dateTimeString);
  const date = momentDate.format('YYYY-MM-DD');
  const time = momentDate.format('HH:mm');

  return { date, time };
}

const splitDateTime = (dateTimeString)  =>{
  moment.locale('es');
  const momentDateTime = moment(dateTimeString);
  let date = momentDateTime.format('ddd D [de] MMMM [de] YYYY');
  date = date.charAt(0).toUpperCase() + date.slice(1);
  const time = momentDateTime.format('hh:mm a');
  return {
      date: date,
      time: time
  };
}

const startAfterEnd = (startHour, endHour) => {
  if (!endHour) {
    return true;
  }
  const momentHour = moment(startHour, 'HH:mm');
  const momentEndHour = moment(endHour, 'HH:mm');

  return momentHour.isBefore(momentEndHour, 'minute');
};

const endBeforeStart = (startHour, endHour) => {
  const momentHour = moment(startHour, 'HH:mm');
  const momentEndHour = moment(endHour, 'HH:mm');

  return momentEndHour.isAfter(momentHour, 'minute');
};

const isSameDate = (startHour, endHour) => {
  const momentHour = moment(startHour, 'HH:mm');
  const momentEndHour = moment(endHour, 'HH:mm');

  return momentHour.isSame(momentEndHour, 'minute');
};


const formatDate = (startDate, startHour, endDate, endHour) => {
  const momentStart = moment(startDate).format('YYYY-MM-DD');
  const momentEnd = moment(endDate).format('YYYY-MM-DD');
  const momentStartHour = moment(startHour, 'HH:mm').format('HH:mm:ss'); 
  const momentEndHour = moment(endHour, 'HH:mm').format('HH:mm:ss');
  return {
    start_date: `${momentStart} ${momentStartHour}`,
    end_date: `${momentEnd} ${momentEndHour}`
  };
};

const startDateBeforeEndDate = (startDate, endDate) => {
  if (!endDate) {
    return true;
  }
  const momentStartDate = moment(startDate, 'YYYY-MM-DD');
  const momentEndDate = moment(endDate, 'YYYY-MM-DD');

  return momentStartDate.isBefore(momentEndDate, 'day');
};

const endDateAfterStartDate = (startDate, endDate) => {
  const momentStartDate = moment(startDate, 'YYYY-MM-DD');
  const momentEndDate = moment(endDate, 'YYYY-MM-DD');

  return momentEndDate.isAfter(momentStartDate, 'day');
};

const isSameDay = (startDate, endDate) => {
  const momentStartDate = moment(startDate, 'YYYY-MM-DD');
  const momentEndDate = moment(endDate, 'YYYY-MM-DD');

  return momentStartDate.isSame(momentEndDate, 'day');
};

const isOneDayDifference = (startDate, endDate) => {
  const momentStartDate = moment(startDate, 'YYYY-MM-DD');
  const momentEndDate = moment(endDate, 'YYYY-MM-DD');

  return momentEndDate.diff(momentStartDate, 'days') === 1;
};

const formatDateForChat = (date) => {
  moment.locale('es');
  moment.updateLocale('es', {
  meridiem: (hour, minute, isLower) => {
    return hour < 12 ? 'am' : 'pm';
  },
  weekdaysShort : ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]
  });

  return moment.utc(date).format('ddd [a las] h:mm a');
}

export default {
  getToken,
  removeToken,
  getRoleStorage,
  getUserByEmail,
  getUserByName,
  getUserFromToke,
  getEmailFromToke,
  getSubFromToken,
  validAge,
  filterByName,
  messageError,
  getErrorMessages,
  getIdUserFromToke,
  startAfterEnd,
  endBeforeStart,
  isSameDate,
  formatDate,
  splitDateTime,
  formatDateForChat,
  encrypt,
  decrypt,
  extractDateAndTime,
  startDateBeforeEndDate,
  isSameDay,
  isOneDayDifference,
  endDateAfterStartDate
};
