# AUTO - Frontend

This is the frontend for the AUTO digital marketplace with AI integration.

## Features

- User authentication and authorization
- Product management
- Order processing
- AI chat interface
- Shopee marketplace integration
- Digital product delivery system

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file with the following variables:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Project Structure

- `src/app` - Next.js app router pages
- `src/components` - React components
- `src/services` - API services
- `src/lib` - Utility functions

## Main Pages

- `/` - Home page
- `/auth/login` - Login page
- `/auth/register` - Registration page
- `/dashboard` - Dashboard page
- `/dashboard/products` - Products management
- `/dashboard/orders` - Orders management
- `/dashboard/chat` - AI chat interface

## Technologies Used

- Next.js 14
- React 19
- TypeScript
- Tailwind CSS
- Axios
- React Query
- React Hook Form
- Zod
- Headless UI
