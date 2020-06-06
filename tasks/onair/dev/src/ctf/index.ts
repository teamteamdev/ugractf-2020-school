import { sha256 } from "js-sha256";

const PREFIX = "ugra_who_writes_so_bad_code_";
const SECRET1 = "west-chance-office-biscuit-coma";
const LEN1 = 10;
const SECRET2 = "lease-gate-bathtub-unlike-flight";
const LEN2 = 10;

export const validateToken = (token: string) => {
    const left = token.slice(0, LEN1);
    const right = token.slice(LEN1);

    const signature = sha256.hmac(SECRET1, left).slice(0, LEN1);

    return right === signature;
};

export const getFlag = (token: string) => {
    return PREFIX + sha256.hmac(SECRET2, token).slice(0, LEN2);
};
