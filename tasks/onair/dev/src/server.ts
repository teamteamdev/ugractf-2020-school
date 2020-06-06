import express, { Request, Response, NextFunction } from 'express';
import fs from 'fs';
import path from 'path';

import router from './app';
import { create } from './db';
import { validateToken } from './ctf';

const app = express();
const state = process.argv[2] || __dirname;
const socket = path.resolve(state, "onair.sock");

app.set('view engine', 'ejs');

app.use('/:token/', async (req: Request, res: Response, next: NextFunction) => {
    const token = req.params.token;

    if (!validateToken(token)) {
        res.sendStatus(404);
        return;
    }

    req.token = token;

    create(state, token).then(db => {
        req.db = db;
        next();
    })
});

app.use('/:token/', router);

if (!fs.existsSync(path.resolve(state, 'db'))) {
    fs.mkdirSync(path.resolve(state, 'db'));
}

app.listen(socket, () => {
    // tslint:disable-next-line:no-console
    console.log(`Listening on ${socket}`);
});
