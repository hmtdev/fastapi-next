import { withAuth } from "next-auth/middleware";

export default withAuth({
  pages: {
    signIn: "/login", // Trang đăng nhập
  },
});

export const config = {
  matcher: ["/", "/dashboard/:path*"], // Kiểm tra cả "/" và "/dashboard/*"
};
