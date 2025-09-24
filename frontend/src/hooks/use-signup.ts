"use client";

import { useState } from "react";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

interface UseSignUpProps {
  onSuccess?: () => void;
}

export function useSignUp({ onSuccess }: UseSignUpProps = {}) {
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function signUp(
    username: string,
    email: string,
    password: string,
    avatarFile: File | null
  ) {
    setLoading(true);

    try {
      let avatarUrl = null;

      if (avatarFile) {
        const formData = new FormData();
        formData.append("file", avatarFile);

        const uploadResponse = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_API}/api/v1/upload/avatar`,
          {
            method: "POST",
            body: formData,
          }
        );

        if (!uploadResponse.ok) {
          throw new Error("Failed to upload avatar");
        }

        const uploadData = await uploadResponse.json();
        avatarUrl = uploadData.url;
      }

      const registerResponse = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_API}/api/v1/users/register`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username,
            email,
            password,
            avatar: avatarUrl,
          }),
        }
      );

      if (!registerResponse.ok) {
        const errorData = await registerResponse.json();
        throw new Error(errorData.detail || "Failed to register user");
      }

      toast.success("User registered successfully!", {
        duration: 4000,
        position: "top-right",
        style: {
          background: "#4caf50",
          color: "#fff",
        },
      });
      onSuccess?.();
      router.push("/login");
    } catch (error: any) {
      toast.error(error.message || "Something went wrong", {
        duration: 4000,
        position: "top-right",
        style: {
          background: "#f44336",
          color: "#fff",
        },
      });
    } finally {
      setLoading(false);
    }
  }

  return { signUp, loading };
}
