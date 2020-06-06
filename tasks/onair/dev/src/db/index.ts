import low, { LowdbAsync } from "lowdb";
import FileAsync from "lowdb/adapters/FileAsync";
import path from "path";
import { v4 as uuid } from 'uuid';

import { getFlag } from "../ctf";
import {Post, User} from "../models";

export class Database {
    constructor(
        public posts: Post[],
        public users: User[]
    ) {}
}

export async function create(state: string, token: string): Promise<LowdbAsync<Database>> {
    const dbPath = path.resolve(state, "db", token);

    const adapter = new FileAsync(dbPath);
    const db = await low(adapter);

    const users = [
        User.create("pete", uuid()),
        User.create("admin", uuid()),
        User.create("alex", uuid()),
        User.create("daniel", uuid())
    ];

    const posts = [
        Post.create(false, "Welcome", "Welcome to our new blog platform! Post feedback as posts!", users[0]),
        Post.create(false, "BAD!!!", "Your platform can't change my password", users[2]),
        Post.create(false, "Announcement", "User Alex is banned for rules violation.", users[1]),
        Post.create(false, "Hi", "How are you, followers?", users[0]),
        Post.create(false, "Re: Hi", "Unban me please, I won't comply", users[2]),
        Post.create(true,  "Does it works?", "No one should see this note.", users[0]),
        Post.create(false, "It works!", "If you want to hide something, use our private notes!", users[0]),
        Post.create(false, "Announcement", "User Alex is unbanned by Pete", users[1]),
        Post.create(false, "Hey", "What's up?", users[3]),
        Post.create(false, "Re: Hey", `Hi, ${users[3].login}! We're fine and our blog platform is best.`, users[0]),
        Post.create(true,  "Secret", `Flag is ${getFlag(token)}`, users[2]),
        Post.create(false, "Wow", "It really works. Is it really secure?", users[2]),
        Post.create(false, "Re: Wow", "Of course, don't worry.", users[0])
    ];


    await db.defaults(new Database(posts, users)).write()

    return db;
};
