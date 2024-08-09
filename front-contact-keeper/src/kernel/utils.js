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



export default {
  getToken,
  removeToken,
  getRoleStorage,
  getUserByEmail,
  getUserByName,
};
