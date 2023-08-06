import { AxiosRequestConfig } from 'axios';
interface ResError {
    message: string;
    code: number;
}
interface GetResponseOk {
    ok: true;
    data: any;
}
interface GetResponseError {
    ok: false;
    error: ResError;
}
declare type GetResponse = GetResponseOk | GetResponseError;
declare type TGET = (url: string, config?: AxiosRequestConfig) => Promise<GetResponse>;
declare const GET: TGET;
export { GET };
//# sourceMappingURL=request.d.ts.map