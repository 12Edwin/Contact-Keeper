export const getUserByName = (name, people) => {
    return people.some(person => person.name === name);
}

export const getUserByEmail = (email, people) => {
    return people.some(person => person.email === email);
}