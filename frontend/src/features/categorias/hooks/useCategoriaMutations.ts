import {useMutation,useQueryClient} from '@tanstack/react-query';
import {createCategory,deleteCategory,updateCategory} from '../api/categories';
import type {Category} from '../types/Category';
export function useCategoriaMutations(){const client=useQueryClient();const refresh=()=>client.invalidateQueries({queryKey:['categorias']});return {create:useMutation({mutationFn:createCategory,onSuccess:refresh}),update:useMutation({mutationFn:({id,data}:{id:number;data:Partial<Category>})=>updateCategory(id,data),onSuccess:refresh}),remove:useMutation({mutationFn:deleteCategory,onSuccess:refresh})};}
