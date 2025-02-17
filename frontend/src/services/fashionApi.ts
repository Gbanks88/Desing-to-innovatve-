import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';
import { FashionItem } from '../types';

export const fashionApi = createApi({
  reducerPath: 'fashionApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/api/fashion' }),
  tagTypes: ['Fashion'],
  endpoints: (builder) => ({
    getFashionItems: builder.query<FashionItem[], void>({
      query: () => '',
      providesTags: ['Fashion'],
    }),
    getFashionItem: builder.query<FashionItem, string>({
      query: (id) => `/${id}`,
      providesTags: ['Fashion'],
    }),
    createFashionItem: builder.mutation<FashionItem, Partial<FashionItem>>({
      query: (body) => ({
        url: '',
        method: 'POST',
        body,
      }),
      invalidatesTags: ['Fashion'],
    }),
    updateFashionItem: builder.mutation<FashionItem, { id: string; body: Partial<FashionItem> }>({
      query: ({ id, body }) => ({
        url: `/${id}`,
        method: 'PUT',
        body,
      }),
      invalidatesTags: ['Fashion'],
    }),
    deleteFashionItem: builder.mutation<void, string>({
      query: (id) => ({
        url: `/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Fashion'],
    }),
  }),
});
