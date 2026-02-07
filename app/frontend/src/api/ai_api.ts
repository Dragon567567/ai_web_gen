import request from "../utils/request.ts";

const aiApi = {
    genCode(desc: string) {
        return request.post("/ai/gen_code", {desc});
    }
};

export default aiApi;