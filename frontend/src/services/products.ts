import api from './api';

export enum ProductType {
  TEMPLATE = 'template',
  ACCOUNT = 'account',
  LINK = 'link',
  VOUCHER = 'voucher',
}

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  product_type: ProductType;
  content: string;
  is_active: boolean;
  ai_enabled: boolean;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface CreateProductData {
  name: string;
  description: string;
  price: number;
  product_type: ProductType;
  content: string;
  is_active?: boolean;
  ai_enabled?: boolean;
}

export interface UpdateProductData {
  name?: string;
  description?: string;
  price?: number;
  product_type?: ProductType;
  content?: string;
  is_active?: boolean;
  ai_enabled?: boolean;
}

export const getProducts = async (): Promise<Product[]> => {
  const response = await api.get<Product[]>('/api/products');
  return response.data;
};

export const getProduct = async (id: number): Promise<Product> => {
  const response = await api.get<Product>(`/api/products/${id}`);
  return response.data;
};

export const createProduct = async (data: CreateProductData): Promise<Product> => {
  const response = await api.post<Product>('/api/products', data);
  return response.data;
};

export const updateProduct = async (id: number, data: UpdateProductData): Promise<Product> => {
  const response = await api.put<Product>(`/api/products/${id}`, data);
  return response.data;
};

export const deleteProduct = async (id: number): Promise<void> => {
  await api.delete(`/api/products/${id}`);
};
