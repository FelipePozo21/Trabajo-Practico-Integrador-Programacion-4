import {useQuery} from '@tanstack/react-query';import {getUsers} from '../api/users';
export function useUsuarios(){return useQuery({queryKey:['usuarios'],queryFn:getUsers});}
