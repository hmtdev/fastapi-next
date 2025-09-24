# 🚀 English Learning App with Gemini AI

Ứng dụng học tiếng Anh thông minh sử dụng AI Gemini, được xây dựng với Next.js và FastAPI.

## ✨ Tính năng chính

- 🧠 **AI Chat với Gemini** - Trò chuyện và học tiếng Anh với AI
- 📚 **Học từ vựng** - Flashcard thông minh, quiz tương tác
- 📊 **Theo dõi tiến độ** - Thống kê học tập, streak days
- 🎯 **Bài tập đa dạng** - Trắc nghiệm, điền từ, viết đoạn văn
- 🔍 **Tìm kiếm nhanh** - Command palette tìm từ và cụm từ
- 🎨 **Giao diện đẹp** - Dark/Light mode với shadcn/ui

## 🛠️ Tech Stack

### Frontend
- **Next.js 15** - App Router, TypeScript
- **shadcn/ui** - Component library
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **next-themes** - Theme switching

### Backend (Planned)
- **FastAPI** - Python API
- **Gemini AI** - Google's AI model
- **PostgreSQL** - Database

## 🚀 Getting Started

### Cài đặt dependencies

```bash
npm install
```

### Chạy development server

```bash
npm run dev
# hoặc
yarn dev
# hoặc
pnpm dev
# hoặc
bun dev
```

Mở [http://localhost:3000](http://localhost:3000) để xem ứng dụng.

### Cài đặt shadcn/ui components

```bash
# Cài đặt các component cần thiết
npx shadcn@latest add button card tabs dialog input textarea
npx shadcn@latest add progress badge avatar alert toast
npx shadcn@latest add sidebar command table calendar
```

## 📁 Cấu trúc thư mục

```
src/
├── app/
│   ├── dashboard/          # Trang quản trị
│   ├── vocabulary/         # Học từ vựng
│   ├── chat/              # Chat với AI
│   └── quiz/              # Bài tập, quiz
├── components/
│   ├── ui/                # shadcn/ui components
│   ├── app-sidebar.tsx    # Navigation sidebar
│   └── header-sidebar.tsx # Header toggle
└── lib/
    ├── utils.ts           # Utilities
    └── api.ts             # API calls
```

## 🎯 Roadmap

- [x] Setup Next.js + shadcn/ui
- [x] Navigation sidebar
- [ ] AI Chat interface
- [ ] Vocabulary flashcards
- [ ] Quiz system
- [ ] Progress tracking
- [ ] FastAPI backend
- [ ] Gemini AI integration
- [ ] Database setup
- [ ] Authentication
- [ ] Deployment

## 🔧 Scripts

```bash
npm run dev          # Chạy development server
npm run build        # Build production
npm run start        # Chạy production server
npm run lint         # Lint code
```

## 📚 Tài liệu tham khảo

- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui Components](https://ui.shadcn.com/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Gemini AI](https://ai.google.dev/docs)
- [FastAPI](https://fastapi.tiangolo.com/)

## 🤝 Đóng góp

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
