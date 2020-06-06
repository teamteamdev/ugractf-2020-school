import { v4 as uuid } from 'uuid';

export default class User {
    constructor(
        public id: string,
        public login: string,
        public password: string
    ) {}

    static create(
        login: string,
        password: string
    ): User {
        return new User(uuid(), login, password);
    }
}
