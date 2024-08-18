import { jwtDecode } from "jwt-decode";
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

const removeToken = () => {
  return localStorage.removeItem("token");
};
const getRoleStorage= () => {
  try {
      const role = localStorage.getItem('role');
      if (!role) {
          throw new Error('No role found');
      }

      return role
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
  }
  return errorMessages[errorCode] || 'Ocurrió un error desconocido en el servidor';
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
  messageError,
  getErrorMessages,
  getIdUserFromToke,
  startAfterEnd,
  endBeforeStart,
  isSameDate,
  formatDate,
  splitDateTime,
  formatDateForChat
};
