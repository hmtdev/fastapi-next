"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Play, SkipBack, SkipForward } from "lucide-react";

export type TranscriptItem = {
  startTime: number;
  endTime: number;
  text: string;
};

export default function YouTubeLearningPage() {
  const [videoUrl, setVideoUrl] = useState("");
  const [videoId, setVideoId] = useState("");
  const [currentTime, setCurrentTime] = useState(0);
  const [data, setData] = useState<TranscriptItem[]>();
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState("en");
  const videoRef = useRef<HTMLIFrameElement>(null);

  const languageOptions = [
    { code: "en", label: "English" },
    { code: "vi", label: "Vietnamese" },
    { code: "ja", label: "Japanese" },
    { code: "fr", label: "French" },
    { code: "es", label: "Spanish" },
    { code: "de", label: "German" },
  ];

  const extractVideoId = (url: string) => {
    const regex =
      /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/;
    const match = url.match(regex);
    return match ? match[1] : null;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const id = extractVideoId(videoUrl);
    if (id) {
      setVideoId(id);
      await getTranscriptFromBackend(videoUrl, language); // Truyền language
    } else {
      alert("Invalid YouTube URL");
    }
  };

  const getTranscriptFromBackend = async (
    videoUrl: string,
    language = "en"
  ) => {
    setLoading(true);
    try {
      const backendUrl = `${
        process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000"
      }/api/v1/transcript?url=${encodeURIComponent(
        videoUrl
      )}&language=${language}`;
      const response = await fetch(backendUrl, {
        method: "GET",
        headers: {
          accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch transcript from backend");
      }

      const result = await response.json();

      const formattedTranscript = (result.transcript || []).map(
        (item: any, idx: number, arr: any[]) => {
          const startTime = item.start;
          let endTime;
          if (idx < arr.length - 1) {
            endTime = arr[idx + 1].start;
          } else {
            endTime = item.start + item.duration;
          }
          return {
            startTime,
            endTime,
            text: item.text,
          };
        }
      );

      setData(formattedTranscript);
    } catch (error) {
      console.error("Error fetching transcript from backend:", error);
      alert("Không thể lấy script từ backend.");
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    function getCurrentTimeFromPlayer() {
      const iframe = videoRef.current;
      if (!iframe) return;

      iframe.contentWindow?.postMessage(
        JSON.stringify({ event: "listening" }),
        "*"
      );
    }

    interval = setInterval(getCurrentTimeFromPlayer, 500);

    function handleMessage(event: MessageEvent) {
      try {
        const data =
          typeof event.data === "string" ? JSON.parse(event.data) : event.data;
        if (data && data.info && typeof data.info.currentTime === "number") {
          setCurrentTime(Math.floor(data.info.currentTime));
        }
      } catch {}
    }

    window.addEventListener("message", handleMessage);

    return () => {
      if (interval) clearInterval(interval);
      window.removeEventListener("message", handleMessage);
    };
  }, [videoId]);

  return (
    <div className="p-6 space-y-6 w-full">
      <div>
        <h1 className="text-3xl font-bold mb-2">YouTube Learning</h1>
        <p className="text-muted-foreground">
          Học tiếng Anh qua video YouTube với script đồng bộ
        </p>
      </div>

      {/* URL Input + Language Select */}
      <Card>
        <CardHeader>
          <CardTitle>Nhập YouTube URL</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              type="url"
              placeholder="https://www.youtube.com/watch?v=..."
              value={videoUrl}
              onChange={(e) => setVideoUrl(e.target.value)}
              className="flex-1"
            />
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="border rounded px-2 py-1"
            >
              {languageOptions.map((opt) => (
                <option key={opt.code} value={opt.code}>
                  {opt.label}
                </option>
              ))}
            </select>
            <Button type="submit">Tải video</Button>
          </form>
        </CardContent>
      </Card>

      {/* Video and Script */}
      {videoId && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Video Player */}
          <Card>
            <CardHeader>
              <CardTitle>Video</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="aspect-video">
                <iframe
                  ref={videoRef}
                  width="100%"
                  height="100%"
                  src={`https://www.youtube.com/embed/${videoId}?enablejsapi=1`}
                  title="YouTube video player"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="rounded-md"
                />
              </div>

              <div className="flex items-center justify-center gap-2 mt-4">
                <Button variant="outline" size="icon">
                  <SkipBack className="h-4 w-4" />
                </Button>
                <Button variant="outline" size="icon">
                  <Play className="h-4 w-4" />
                </Button>
                <Button variant="outline" size="icon">
                  <SkipForward className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Script Panel */}
          <Card>
            <CardHeader>
              <CardTitle>Script</CardTitle>
            </CardHeader>
            <CardContent>
              <div
                className="h-96 overflow-y-auto space-y-2"
                id="transcript-panel"
              >
                {(data && data.length > 0 ? data : []).map((item, index) => {
                  const isActive =
                    currentTime >= item.startTime && currentTime < item.endTime;
                  return (
                    <div
                      key={index}
                      ref={(el) => {
                        if (isActive && el) {
                          el.scrollIntoView({
                            behavior: "smooth",
                            block: "center",
                          });
                        }
                      }}
                      className={`p-3 rounded-md border cursor-pointer transition-colors ${
                        isActive
                          ? "bg-primary text-primary-foreground"
                          : "hover:bg-muted"
                      }`}
                      onClick={() => setCurrentTime(item.startTime)}
                    >
                      <div className="text-xs text-muted-foreground mb-1">
                        {Math.floor(item.startTime / 60)}:
                        {(item.startTime % 60).toString().padStart(2, "0")} -
                        {Math.floor(item.endTime / 60)}:
                        {(item.endTime % 60).toString().padStart(2, "0")}
                      </div>
                      <p className="text-sm">{item.text}</p>
                    </div>
                  );
                })}
                {(!data || data.length === 0) && (
                  <div className="text-center text-muted-foreground mt-8">
                    Không có transcript cho video này.
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
