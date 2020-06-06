import { NextFunction, Request, Response } from 'express';
import { User, Post } from '../models';

export default {
    profilePage(req: Request, res: Response, next: NextFunction) {
        const posts = req.db.get('posts').filter((post: Post): boolean => {
            return post.userId === req.user.id
        }).value();

        res.render('profile', {
            user: req.user,
            posts,
            token: req.token
        });
        next();
    },

    postsPage(req: Request, res: Response, next: NextFunction) {
        const offset = typeof req.query.offset === 'string' ? parseInt(req.query.offset, 10) : 0;

        const posts = req.db.get('posts').slice(offset, offset + 10).value();

        const userList = req.db.get('users').value();
        const users = new Map<string, User>(
            userList.map((user: User) => [user.id, user])
        )

        res.render('posts', {
            user: req.user,
            posts,
            users,
            prev: (offset - 10 >= 0 ? offset - 10 : null),
            next: (posts.length >= 0 ? offset + 10 : null),
            token: req.token
        });

        next();
    },

    postPage(req: Request, res: Response, next: NextFunction) {
        const post = req.db.get('posts').find({id: req.params.id}).value();

        if (post) {
            const author = req.db.get('users').find({id: post.userId}).value();
            res.render('post', {
                user: req.user,
                post,
                author,
                token: req.token
            });
        } else {
            res.sendStatus(404);
        }

        next();
    },

    newPostPage(req: Request, res: Response, next: NextFunction) {
        const context = {
            token: req.token,
            user: req.user,
            title: "",
            text: "",
            fromPost: ""
        };

        if (typeof req.query.from === 'string') {
            const fromPost = req.db.get('posts').find({id: req.query.from}).value();

            if (!fromPost || fromPost.isPrivate && fromPost.userId !== req.user.id) {
                res.sendStatus(403);
            }

            context.fromPost = fromPost.id;
            context.title = fromPost.title;
            context.text = fromPost.text;
        }
        res.render('compose', context);
    },

    postAction(req: Request, res: Response, next: NextFunction) {
        const postData = {
            title: "",
            text: "",
            isPrivate: false
        };

        if (typeof req.body.from === 'string' && req.body.from) {
            const fromPost = req.db.get('posts').find({id: req.body.from}).value();

            if (!fromPost || fromPost.isPrivate && fromPost.userId !== req.user.id) {
                res.sendStatus(403);
            }

            postData.title = fromPost.title;
            postData.text = fromPost.text;
        }

        if (typeof req.body.title === 'string' && req.body.title) {
            postData.title = req.body.title;
        }
        if (typeof req.body.text === 'string' && req.body.text) {
            postData.text = req.body.text;
        }

        if (req.body.isPrivate === 'true') {
            postData.isPrivate = true;
        }

        if (!postData.title || !postData.text) {
            res.sendStatus(403);
        }

        req.db.get('posts').push(Post.create(postData.isPrivate, postData.title, postData.text, req.user.id)).write();
        res.redirect(`/${req.token}/user/profile`);
    }
};
