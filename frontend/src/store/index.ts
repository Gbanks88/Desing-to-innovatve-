import { configureStore } from '@reduxjs/toolkit';
import { fashionApi } from '../services/fashionApi';
import { videosApi } from '../services/videosApi';
import { scholarshipsApi } from '../services/scholarshipsApi';

export const store = configureStore({
  reducer: {
    [fashionApi.reducerPath]: fashionApi.reducer,
    [videosApi.reducerPath]: videosApi.reducer,
    [scholarshipsApi.reducerPath]: scholarshipsApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(
      fashionApi.middleware,
      videosApi.middleware,
      scholarshipsApi.middleware
    ),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
