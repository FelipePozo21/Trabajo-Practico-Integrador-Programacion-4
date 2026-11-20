import {useEffect} from 'react';
import type {ReactNode} from 'react';
import {Link,NavLink,useNavigate} from 'react-router-dom';
import {useAuthStore} from './store/authStore';
import {useCartStore} from './store/cartStore';
import {AppRouter} from './routes/AppRouter';
function Shell({children}:{children:ReactNode}){
  const {user,logout}=useAuthStore();
  const cartCount=useCartStore(state=>state.items.reduce((count,item)=>count+item.cantidad,0));
  const navigate=useNavigate();
  return <><header className="nav"><Link className="brand" to="/">food<span>store</span><i>●</i></Link><nav><NavLink to="/">Menú</NavLink><NavLink to="/carrito">Carrito <b>{cartCount}</b></NavLink>{user&&<NavLink to="/mis-pedidos">Mis pedidos</NavLink>}{user?.role==='admin'&&<NavLink to="/admin/resumen">Administración</NavLink>}</nav><div className="account">{user?<><span>Hola, {user.full_name.split(' ')[0]}</span><button className="linkbtn" onClick={async()=>{await logout();navigate('/login')}}>Salir ↗</button></>:<Link to="/login">Ingresar ↗</Link>}</div></header><main>{children}</main><footer>Hecho para comer rico. <span>Food Store · Buenos Aires</span></footer></>;
}
export default function App(){
  const checkSession=useAuthStore(state=>state.checkSession);
  useEffect(()=>{void checkSession()},[checkSession]);
  return <Shell><AppRouter/></Shell>;
}
