import {errorMessage} from '../api/axiosInstance';
export function Notice({error}:{error:unknown}){return error?<div className="alert">{errorMessage(error)}</div>:null;}
