import { LowdbAsync } from "lowdb";

import { Database } from "../../db";
import { User } from "../../models";

declare global {
    namespace Express {
        interface Request {
            db: LowdbAsync<Database>;
            user: User;
            token: string;
        }
    }
}
