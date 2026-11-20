import {useState} from 'react';
import {useForm} from '@tanstack/react-form';
import {useQueryClient} from '@tanstack/react-query';
import {api,errorMessage} from '../../../shared/api/axiosInstance';

type Category = {id:number;nombre:string;descripcion:string|null;activo:boolean};
type Product = {id:number;categoria_id:number;nombre:string;descripcion:string|null;precio_base:number;imagen_url:string|null;stock:number;disponible:boolean;activo:boolean;categoria:Category};
type CatalogRecord = Category | Product;
type Props = {kind:'categorias'|'productos';categories:Category[];initial?:CatalogRecord;onDone:()=>void;onCancel?:()=>void};

export function AdminCatalogForm({kind,categories,initial,onDone,onCancel}:Props){
  const queryClient=useQueryClient();
  const [error,setError]=useState('');
  const product=initial&&'precio_base' in initial?initial:undefined;
  const form=useForm({
    defaultValues: {
      nombre:initial?.nombre??'',
      descripcion:initial?.descripcion??'',
      categoria_id:product?String(product.categoria_id):categories[0]?String(categories[0].id):'',
      precio_base:product?String(product.precio_base):'',
      imagen_url:product?.imagen_url??'',
      stock:product?String(product.stock):'0',
      disponible:product?.disponible??true,
    },
    onSubmit:async({value})=>{
      try{
        const payload=kind==='categorias'
          ?{nombre:value.nombre,descripcion:value.descripcion||null}
          :{nombre:value.nombre,descripcion:value.descripcion||null,categoria_id:Number(value.categoria_id),precio_base:Number(value.precio_base),imagen_url:value.imagen_url||null,stock:Number(value.stock),disponible:value.disponible};
        const endpoint=kind==='categorias'?'/categorias':'/productos';
        if(initial) await api.put(`${endpoint}/${initial.id}`,payload);
        else await api.post(endpoint,payload);
        await queryClient.invalidateQueries({queryKey:[kind]});
        setError('');
        onDone();
      }catch(reason){setError(errorMessage(reason));}
    },
  });
  return <form className="catalog-form" onSubmit={event=>{event.preventDefault();void form.handleSubmit();}}>
    <div className="catalog-form-heading"><div><span className="eyebrow">{initial?'EDITAR':'NUEVO REGISTRO'}</span><h3>{initial?`Editar ${initial.nombre}`:kind==='categorias'?'Crear categoría':'Crear producto'}</h3></div>{onCancel&&<button type="button" className="linkbtn" onClick={onCancel}>Cerrar ×</button>}</div>
    {error&&<div className="alert">{error}</div>}
    <form.Field name="nombre">{field=><label>Nombre<input required minLength={2} maxLength={120} value={field.state.value} onChange={event=>field.handleChange(event.target.value)}/></label>}</form.Field>
    <form.Field name="descripcion">{field=><label>Descripción<textarea rows={2} value={field.state.value} onChange={event=>field.handleChange(event.target.value)}/></label>}</form.Field>
    {kind==='productos'&&<>
      <form.Field name="categoria_id">{field=><label>Categoría<select required value={field.state.value} onChange={event=>field.handleChange(event.target.value)}><option value="">Elegí una categoría</option>{categories.map(category=><option key={category.id} value={category.id}>{category.nombre}</option>)}</select></label>}</form.Field>
      <div className="catalog-form-row"><form.Field name="precio_base">{field=><label>Precio<input required type="number" min="0" step="0.01" value={field.state.value} onChange={event=>field.handleChange(event.target.value)}/></label>}</form.Field><form.Field name="stock">{field=><label>Stock<input required type="number" min="0" step="1" value={field.state.value} onChange={event=>field.handleChange(event.target.value)}/></label>}</form.Field></div>
      <form.Field name="imagen_url">{field=><label>URL de imagen<input type="url" value={field.state.value} onChange={event=>field.handleChange(event.target.value)} placeholder="https://…"/></label>}</form.Field>
      <form.Field name="disponible">{field=><label className="check-label"><input type="checkbox" checked={field.state.value} onChange={event=>field.handleChange(event.target.checked)}/> Disponible para la venta</label>}</form.Field>
    </>}
    <div className="catalog-form-actions"><button className="button primary">{initial?'Guardar cambios':'Crear'}</button>{onCancel&&<button type="button" className="button secondary" onClick={onCancel}>Cancelar</button>}</div>
  </form>;
}
