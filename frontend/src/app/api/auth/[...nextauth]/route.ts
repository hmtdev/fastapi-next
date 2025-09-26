import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: {
          label: "Email",
          type: "text",
          placeholder: "admin@gmail.com",
        },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        try {
          const params = new URLSearchParams();
          params.append("username", credentials?.email || "");
          params.append("password", credentials?.password || "");

          const res = await fetch(
            `${process.env.NEXT_PUBLIC_BACKEND_API}/api/v1/auth/token`,
            {
              method: "POST",
              headers: { "Content-Type": "application/x-www-form-urlencoded" },
              body: params.toString(),
            }
          );

          if (!res.ok) {
            return null;
          }
          const data = await res.json();
          const accessToken = data.access_token;
          const userResponse = await fetch(
            `${process.env.NEXT_PUBLIC_BACKEND_API}/api/v1/users/me`,
            {
              method: "GET",
              headers: {
                Authorization: `Bearer ${accessToken}`,
                "Content-Type": "application/json",
              },
            }
          );
          if (!userResponse.ok) {
            console.error("Failed to fetch user data");
            return null;
          }
          const userData = await userResponse.json();
          return {
            id: "1",
            name: userData?.username,
            email: userData?.email,
            image: userData?.avatar,
            accessToken: data.access_token,
            refreshToken: data.refresh_token,
            role: userData?.role,
            level: userData?.level,
          };
        } catch (error) {
          console.error("Auth error:", error);
          return null;
        }
      },
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET,
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = user.accessToken;
        token.refreshToken = user.refreshToken;
        token.role = user.role;
        token.image = user.image;
        token.level = user.level;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.accessToken = token.accessToken;
        session.user.refreshToken = token.refreshToken;
        session.user.role = token.role;
        session.user.level = token.level;
      }
      console.log("ss from server ", session);
      return session;
    },
  },
  pages: {
    signIn: "/login",
    session: {
      strategy: "jwt",
    },
  },
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
