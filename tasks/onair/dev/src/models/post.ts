import { v4 as uuid } from 'uuid';

import User from "./user";

export default class Post {
    static readonly type = "post";

    constructor(
        public id: string,
        public isPrivate: boolean,
        public title: string,
        public text: string,
        public userId: string
    ) {}

    static create(isPrivate: boolean, title: string, text: string, user: string | User): Post {
        return new Post(
            uuid(),
            isPrivate,
            title,
            text,
            (user instanceof User) ? user.id : user
        );
    }
}
