import StatsCard from "@/components/stats-card";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Brain,
  CircleCheck,
  Clock,
  Plus,
  Search,
  Target,
  TrendingUp,
} from "lucide-react";
import StudyCard from "./study-card";
import Link from "next/link";
import Image from "next/image";
export default function Page() {
  const stats = [
    {
      title: "Cards to Review",
      value: 152,
      icon: <Clock className="h-8 w-8 text-muted-foreground" />,
    },
    {
      title: "Card New",
      value: 285,
      icon: <Plus className="h-8 w-8 text-muted-foreground" />,
    },
    {
      title: "Mastered",
      value: 10,
      icon: <CircleCheck className="h-8 w-8 text-muted-foreground" />,
    },
    {
      title: "Study Streak",
      value: `5 days`,
      icon: <TrendingUp className="h-8 w-8 text-muted-foreground" />,
    },
  ];
  const studyCards = [
    {
      title: "IELTS Vocabulary",
      value: 5,
      icon: <Brain className="h-6 w-6" />,
      description: "Essential words for IELTS preparation.",
      color: "bg-blue-400",
      tag: "Advanced",
      id: "1",
    },
    {
      title: "Business English",
      value: 54,
      icon: <Clock className="h-6 w-6" />,
      description: "Professional vocabulary for workplace",
      color: "bg-red-400",
      tag: "Intermediate",
      id: "2",
    },
    {
      title: "Daily Conversations",
      value: 15,
      icon: <Plus className="h-6 w-6" />,
      description: "Common phrases for everyday situations",
      color: "bg-orange-400",
      tag: "Intermediate",
      id: "3",
    },
    {
      title: "Academic Writing",
      value: 20,
      icon: <Target className="h-6 w-6" />,
      description: "Advanced vocabulary for academic papers.",
      color: "bg-green-400",
      tag: "Intermediate",
      id: "4",
    },
  ];

  return (
    <div className="flex space-y-8 flex-col">
      <div>
        <h1 className="text-3xl font-bold">Flashcards</h1>
        <p className="text-muted-foreground">
          Master vocabulary with spaced repetition
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <StatsCard
            key={index}
            title={stat.title}
            value={stat.value}
            icon={stat.icon}
          />
        ))}
      </div>
      <div className="flex gap-4">
        <Input
          className="bg-secondary flex-1"
          type="text"
          placeholder="Search..."
          icon={<Search className="h-4 w-4" />}
        />
        <Button variant="outline" className="flex items-center gap-2">
          <Plus className="h-8 w-8 text-muted-foreground" />
          <div>Create Deck</div>
        </Button>
      </div>
      <div className="flex w-full flex-col gap-6">
        <Tabs defaultValue="mydecks">
          <TabsList
            size="sm"
            className="w-fit bg-muted text-muted-foreground"
            shape="pill"
          >
            <TabsTrigger value="mydecks">My Decks</TabsTrigger>
            <TabsTrigger value="discover">Discovery</TabsTrigger>
            <TabsTrigger value="statistics">Statistics</TabsTrigger>
          </TabsList>
          <TabsContent value="discover">
            <Card>
              <CardHeader className="text-center">
                <CardTitle>Discover New Decks</CardTitle>
                <CardDescription>
                  Browse thousands of flashcard decks created by the community
                </CardDescription>
              </CardHeader>
              <CardContent className="grid grid-cols-3 gap-4">
                <Button
                  asChild
                  variant="outline"
                  className="flex items-center gap-2"
                >
                  <Link href={"https://ankiweb.net/"}>Anki</Link>
                </Button>
                <Button
                  asChild
                  variant="outline"
                  className="flex items-center gap-2"
                >
                  <Link href={"https://quizlet.com/"}>Quizlet</Link>
                </Button>
                <Button
                  asChild
                  variant="outline"
                  className="flex items-center gap-2"
                >
                  <Link href={"https://www.duolingo.com/"}>Duolingo</Link>
                </Button>
              </CardContent>
              <CardFooter className="flex align-center justify-center">
                <Button>
                  <Search />
                  Browse Public Decks
                </Button>
              </CardFooter>
            </Card>
          </TabsContent>
          <TabsContent value="mydecks">
            <div className="flex flex-wrap gap-4">
              {studyCards.map((card, index) => (
                <StudyCard key={index} {...card} />
              ))}
            </div>
          </TabsContent>

          <TabsContent value="statistics">
            <p className="text-lg text-center"> Next soon ...</p>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
