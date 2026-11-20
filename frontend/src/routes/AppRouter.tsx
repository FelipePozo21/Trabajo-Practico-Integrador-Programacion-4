import {Link,Navigate,Route,Routes} from 'react-router-dom';
import {LoginPage,RegisterPage} from '../features/auth/pages/AuthPages';
import {CatalogPage} from '../features/productos/pages/CatalogPage';
import {AdminCategoriasPage} from '../features/categorias/pages/AdminCategoriasPage';
import {AdminProductosPage} from '../features/productos/pages/AdminProductosPage';
import {AdminUsuariosPage} from '../features/usuarios/pages/AdminUsuariosPage';
import {CartPage,CheckoutPage} from '../features/pedidos/pages/CustomerOrderPages';
import {OrdersPage,AdminSummaryPage} from '../features/pedidos/pages/OrderManagementPages';
import {ProtectedRoute} from './ProtectedRoute';
export function AppRouter(){return <Routes>
  <Route path="/" element={<CatalogPage/>}/>
  <Route path="/login" element={<LoginPage/>}/>
  <Route path="/registro" element={<RegisterPage/>}/>
  <Route path="/register" element={<RegisterPage/>}/>
  <Route path="/carrito" element={<CartPage/>}/>
  <Route path="/checkout" element={<ProtectedRoute><CheckoutPage/></ProtectedRoute>}/>
  <Route path="/mis-pedidos" element={<ProtectedRoute><OrdersPage ownOnly/></ProtectedRoute>}/>
  <Route path="/admin/resumen" element={<ProtectedRoute role="admin"><AdminSummaryPage/></ProtectedRoute>}/>
  <Route path="/admin/categorias" element={<ProtectedRoute role="admin"><AdminCategoriasPage/></ProtectedRoute>}/>
  <Route path="/admin/productos" element={<ProtectedRoute role="admin"><AdminProductosPage/></ProtectedRoute>}/>
  <Route path="/admin/pedidos" element={<ProtectedRoute role="admin"><OrdersPage admin/></ProtectedRoute>}/>
  <Route path="/admin/usuarios" element={<ProtectedRoute role="admin"><AdminUsuariosPage/></ProtectedRoute>}/>
  <Route path="/unauthorized" element={<div className="empty"><h1>Esta zona es solo para el equipo.</h1><Link to="/">Volver al menú</Link></div>}/>
  <Route path="*" element={<Navigate to="/"/>}/>
</Routes>}
