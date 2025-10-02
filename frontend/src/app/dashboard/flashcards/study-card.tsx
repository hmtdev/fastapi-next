import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { BookOpen, Target } from "lucide-react";
import Link from "next/link";

interface StudyCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  description?: string;
  color?: string;
  tag?: string;
  id?: string;
}

const StudyCard: React.FC<StudyCardProps> = ({
  title,
  value,
  icon,
  description,
  color,
  tag,
  id,
}) => {
  return (
    <Card className="p-6 min-w-3xs ">
      <CardHeader className="p-0">
        <div className="flex w-full justify-between mb-2">
          <div
            className={`flex justify-center items-center rounded-lg ${color} w-[32px] h-[32px]`}
          >
            {icon}
          </div>
          <div className="inline-flex">
            <Badge variant="outline" className="h-fit">
              {tag}
            </Badge>
          </div>
        </div>
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent className="p-0 space-y-4">
        <div className="space-y-2">
          <div className="flex justify-between flex-1">
            <span className="text-sm">Progress</span>
            <span className="text-sm">{value}%</span>
          </div>
          <Progress value={value} className="h-2" />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center">
            <p className="text-lg font-bold text-blue-600">70</p>
            <p className="text-xs text-muted-foreground">New</p>
          </div>
          <div className="text-center">
            <p className="text-lg font-bold text-red-600">60</p>
            <p className="text-xs text-muted-foreground">Review</p>
          </div>
        </div>
        <div className="flex justify-between gap-2">
          <Button className="flex gap-2 flex-1">
            <BookOpen />
            <Link
              href={{
                pathname: `/dashboard/flashcards/${id}`,
                query: { fromFlashcards: "true" },
              }}
            >
              Study Now
            </Link>
          </Button>
          <Button className="flex justify-center" variant={"outline"}>
            <Target />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default StudyCard;
