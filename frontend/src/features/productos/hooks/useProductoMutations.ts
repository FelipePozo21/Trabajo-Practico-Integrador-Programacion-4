import {useMutation,useQueryClient} from '@tanstack/react-query';
import {createProduct,deleteProduct,updateProduct,updateProductStock} from '../api/products';
import type {Product} from '../types/Product';
export function useProductoMutations(){const client=useQueryClient();const refresh=()=>client.invalidateQueries({queryKey:['productos']});return {create:useMutation({mutationFn:createProduct,onSuccess:refresh}),update:useMutation({mutationFn:({id,data}:{id:number;data:Partial<Product>})=>updateProduct(id,data),onSuccess:refresh}),updateStock:useMutation({mutationFn:({id,stock,disponible}:{id:number;stock:number;disponible:boolean})=>updateProductStock(id,stock,disponible),onSuccess:refresh}),remove:useMutation({mutationFn:deleteProduct,onSuccess:refresh})};}
