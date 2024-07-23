export const getUserByName = (name, people) => {
    return people.find(person => person.name === name);
}