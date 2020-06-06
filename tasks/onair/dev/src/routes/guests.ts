import { NextFunction, Request, Response } from 'express';
import { User } from '../models';

const RE = /^[a-z0-9-]+$/i;

export default {
    main(req: Request, res: Response, next: NextFunction) {
        if (req.cookies.auth) {
            res.redirect(`/${req.token}/user/profile`);
        } else {
            res.redirect(`/${req.token}/login`);
        }
        next();
    },
    loginPage(req: Request, res: Response, next: NextFunction) {
        res.render('login', {
            page: 'login',
            error: req.query.error,
            token: req.token
        });
        next();
    },
    registerPage(req: Request, res: Response, next: NextFunction) {
        res.render('login', {
            page: 'register',
            error: req.query.error,
            token: req.token
        });
        next();
    },
    loginAction(req: Request, res: Response, next: NextFunction) {
        const {login, password} = req.body;
        res.cookie('auth', `${login}:${password}`);
        res.redirect(`/${req.token}/user/profile`);
        next();
    },
    registerAction(req: Request, res: Response, next: NextFunction) {
        const {login, password} = req.body;
        if (!RE.test(login) || !RE.test(password)) {
            return res.redirect(`/${req.token}/login?error=Так+нельзя`);
        }

        if (req.db.get('users').filter({login}).size().value()) {
            return res.redirect(`/${req.token}/login?error=Пользователь+уже+есть!`);
        }

        req.db.get('users').push(User.create(login, password)).write();
        res.redirect(`/${req.token}/login`);
        next();
    },
    logoutAction(req: Request, res: Response, next: NextFunction) {
        res.clearCookie('auth');
        res.redirect(`/${req.token}/login`);
        next();
    }
};
