import { NextFunction, Request, Response } from "express";

export default {
    checkUser(req: Request, res: Response, next: NextFunction) {
        (() => {
            if (!req.cookies.auth) {
                return res.status(403).send(`Who? <a href="/${req.token}/login">Login</a>`);
            }
            const creds = (req.cookies.auth as string).split(':');
            if (creds.length !== 2) {
                return res.status(403).send(`Invalid cookie. <a href="/${req.token}/logout">Logout</a>`);
            }
            const [login, password] = creds;

            const user = req.db.get("users").find({login, password}).value()

            if (!user) {
                return res.status(403).send(`No user. <a href="/${req.token}/logout">Logout</a>`);
            }

            req.user = user;
        })();
        next();
    }
}
