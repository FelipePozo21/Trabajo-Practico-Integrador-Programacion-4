import type {Product} from './types';

export const PLACEHOLDER_PRODUCT_IMAGE = '/images/products/sin-imagen.png';

const categoryImages: [string, string][] = [
  ['hamburg', '/images/products/hamburguesa.png'],
  ['pizza', '/images/products/pizza.png'],
  ['bebida', '/images/products/bebida.png'],
];

export function getProductImage(product: Pick<Product, 'imagen_url' | 'categoria'>): string {
  const customImage = product.imagen_url?.trim();
  if (customImage) return customImage;

  const categoryName = product.categoria.nombre.trim().toLocaleLowerCase('es-AR');
  return categoryImages.find(([prefix]) => categoryName.includes(prefix))?.[1] ?? PLACEHOLDER_PRODUCT_IMAGE;
}
