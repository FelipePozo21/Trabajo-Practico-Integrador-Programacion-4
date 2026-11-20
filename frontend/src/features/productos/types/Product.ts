export interface Product { id:number; categoria_id:number; nombre:string; descripcion:string|null; precio_base:number; imagen_url:string|null; stock:number; disponible:boolean; activo:boolean; categoria:{id:number;nombre:string;descripcion:string|null;activo:boolean} }
export interface ProductsPage { total:number; items:Product[] }
export interface ProductFilters { skip?:number; limit?:number; search?:string; categoria_id?:number; disponible?:boolean }
