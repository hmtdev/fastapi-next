"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { BookOpen, MoveLeft } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import FlashCard from "./flashcard";

export default function StudyDeck() {
  const { id, fromFlashcards } = useParams();

  const showBackButton = fromFlashcards === "true";

  return (
    <div className="flex flex-col w-full">
      {showBackButton && (
        <Button variant="outline" asChild className="mb-4">
          <Link href="/dashboard/flashcards">
            <MoveLeft />
            Back to decks
          </Link>
        </Button>
      )}
      <div className="flex justify-between mb-6">
        <div className="flex flex-col">
          <h1 className="text-3xl font-bold">IELTS Vocabulary [{id}]</h1>
          <p className="text-muted-foreground">Card 1 of 30 </p>
        </div>
        <div className="flex flex-col items-end gap-2">
          <Badge>Advanced</Badge>
          <Progress value={50} className="h-2 min-w-[128px]" />
        </div>
      </div>
      <FlashCard
        title="Serendipity"
        value={50}
        icon={<BookOpen />}
        description="/ˌser.ənˈdɪp.ə.ti/"
        color="bg-blue-500"
        tag="New"
        id={"1"}
      />
    </div>
  );
}
