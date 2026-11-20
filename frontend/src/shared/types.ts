export type Category={id:number;nombre:string;descripcion:string|null;activo:boolean};
export type Product={id:number;categoria_id:number;nombre:string;descripcion:string|null;precio_base:number;imagen_url:string|null;stock:number;disponible:boolean;activo:boolean;categoria:Category};
export type Order={id:number;usuario_id:number;estado:string;forma_pago:string;direccion_entrega:string;notas:string|null;total:number;created_at:string;items:{producto_id:number;nombre_producto:string;cantidad:number;precio_unitario:number;subtotal:number}[]};
