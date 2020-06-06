import bodyParser from 'body-parser';
import cookieParser from "cookie-parser";
import { NextFunction, Request, Response, Router } from "express";

import middlewares from "./middlewares";
import routes from "./routes";

const router = Router();
router.use(bodyParser.urlencoded({ extended: true }));
router.use(cookieParser());

router.use('/user/', middlewares.auth.checkUser);

router.get('/', routes.guests.main);
router.get('/login', routes.guests.loginPage);
router.get('/register', routes.guests.registerPage);
router.post('/login', routes.guests.loginAction);
router.post('/register', routes.guests.registerAction);
router.all('/logout', routes.guests.logoutAction);

router.get('/user/profile', routes.users.profilePage);
router.get('/user/posts', routes.users.postsPage);
router.get('/user/post/:id', routes.users.postPage);
router.get('/user/post', routes.users.newPostPage);
router.post('/user/post', routes.users.postAction);

export default router;
