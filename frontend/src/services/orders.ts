import api from './api';

export enum OrderStatus {
  PENDING = 'pending',
  PAID = 'paid',
  DELIVERED = 'delivered',
  CANCELLED = 'cancelled',
}

export interface Order {
  id: number;
  user_id: number;
  product_id: number;
  quantity: number;
  total_price: number;
  status: OrderStatus;
  shopee_order_id?: string;
  delivery_data?: string;
  is_delivered: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateOrderData {
  product_id: number;
  quantity?: number;
  total_price: number;
  shopee_order_id?: string;
}

export interface UpdateOrderData {
  status?: OrderStatus;
  is_delivered?: boolean;
}

export const getOrders = async (): Promise<Order[]> => {
  const response = await api.get<Order[]>('/api/orders');
  return response.data;
};

export const getOrder = async (id: number): Promise<Order> => {
  const response = await api.get<Order>(`/api/orders/${id}`);
  return response.data;
};

export const createOrder = async (data: CreateOrderData): Promise<Order> => {
  const response = await api.post<Order>('/api/orders', data);
  return response.data;
};

export const updateOrder = async (id: number, data: UpdateOrderData): Promise<Order> => {
  const response = await api.put<Order>(`/api/orders/${id}`, data);
  return response.data;
};

export const deliverDigitalProduct = async (id: number): Promise<Order> => {
  const response = await api.post<Order>(`/api/orders/${id}/deliver`);
  return response.data;
};
