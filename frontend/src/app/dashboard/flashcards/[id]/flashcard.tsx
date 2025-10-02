import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  CircleCheck,
  CircleX,
  Clock,
  Eye,
  RotateCw,
  Shuffle,
  Volume2,
} from "lucide-react";

interface StudyCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  description?: string;
  color?: string;
  tag?: string;
  id?: string;
}

const FlashCard: React.FC<StudyCardProps> = ({
  title,
  value,
  icon,
  description,
  color,
  tag,
  id,
}) => {
  return (
    <div className="flex flex-col w-full items-center">
      <Card className="p-6 w-full">
        <CardHeader className="p-0 text-center">
          <CardTitle className="text-4xl font-bold">{title}</CardTitle>
          <CardDescription className="text-lg font-muted-foreground">
            {description}
          </CardDescription>
        </CardHeader>
        <CardContent className="p-0 space-y-4">
          <div className="space-y-4 text-center">
            <Badge>nount</Badge>
            <div className="flex justify-between flex-1 cursor-pointer mx-auto w-fit text-muted-foreground">
              <Eye className="h-4 w-4 inline-block mr-2" />
              <p className="text-sm">Click to reveal definition</p>
            </div>
            <Button variant="outline">
              <Volume2 className="inline-block mr-2" />
              Pronounce
            </Button>
          </div>
        </CardContent>
      </Card>
      <div className="flex justify-between gap-2 mt-4 ">
        <Button variant="outline">
          <CircleCheck className="inline-block mr-2" />
          Easy (4 days)
        </Button>
        <Button variant="outline">
          <Clock className="inline-block mr-2" />
          Good (2 days)
        </Button>
        <Button variant="outline">
          <CircleX className="inline-block mr-2" />
          Hard (1 day)
        </Button>
      </div>
      <div className="flex justify-between gap-2 mt-4 ">
        <Button variant="outline">
          <RotateCw className="inline-block mr-2" />
          Reset Card
        </Button>
        <Button variant="outline">
          <Shuffle className="inline-block mr-2" />
          Shuffle Deck
        </Button>
        <Button variant="outline">
          <Volume2 className="inline-block mr-2" />
          Auto-play
        </Button>
      </div>
    </div>
  );
};

export default FlashCard;
