import { jwtDecode } from "jwt-decode";

const getUserByName = (name, people) => {
  return people.some((person) => person.name === name);
};

const getUserByEmail = (email, people) => {
  return people.some((person) => person.email === email);
};

const getToken = () => {
  return localStorage.getItem("token");
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


const validAge = (birthday) => {
  return true
}

export default {
  getToken,
  removeToken,
  getRoleStorage,
  getUserByEmail,
  getUserByName,
  getUserFromToke,
  validAge
};
