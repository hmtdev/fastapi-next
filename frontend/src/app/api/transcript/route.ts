import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const { videoUrl, language } = await request.json();

    const apiUrl = `${
      process.env.BACKEND_URL || "http://127.0.0.1:8000"
    }/api/v1/transcript?url=${encodeURIComponent(videoUrl)}${
      language ? `&language=${language}` : ""
    }`;

    const response = await fetch(apiUrl, {
      method: "GET",
      headers: {
        accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch transcript from backend");
    }

    const data = await response.json();

    return NextResponse.json({ transcript: data.transcript });
  } catch (error) {
    console.error("Error fetching transcript:", error);
    return NextResponse.json(
      { error: "Failed to fetch transcript" },
      { status: 500 }
    );
  }
}
