export interface FashionItem {
  id: string;
  name: string;
  description: string;
  category: string;
  price: number;
  imageUrl: string;
  createdAt: string;
  updatedAt: string;
}

export interface Video {
  id: string;
  title: string;
  description: string;
  url: string;
  thumbnailUrl: string;
  category: string;
  createdAt: string;
}

export interface Scholarship {
  id: string;
  title: string;
  description: string;
  amount: number;
  deadline: string;
  requirements: string[];
  status: 'open' | 'closed';
  createdAt: string;
}
