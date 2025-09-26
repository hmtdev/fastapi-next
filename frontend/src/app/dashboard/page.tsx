import { getServerSession } from "next-auth";
import { authOptions } from "../api/auth/[...nextauth]/route";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  ArrowRight,
  Award,
  Badge,
  BookOpen,
  Calendar,
  Clock,
  PlayCircle,
  Target,
  TrendingUp,
} from "lucide-react";
import { Button } from "@/components/ui/button";

export default async function Page() {
  const session = await getServerSession(authOptions);
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_BACKEND_API}/api/v1/dashboard/stats`,
    {
      cache: "no-store",
      headers: {
        Authorization: `Bearer ${session?.user.accessToken}`,
      },
    }
  );
  const data = await res.json();
  console.log("Dashboard data:", data);
  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">
            Welcome back, {data.username} 👋
          </h1>
          <p className="text-muted-foreground">
            Let's continue your English learning journey
          </p>
        </div>
        {/* <Badge variant="secondary">7 day streak 🔥</Badge> */}
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">
                  Lessons Completed
                </p>
                <p className="text-2xl font-bold">
                  {data.total_lession_completed}
                </p>
              </div>
              <BookOpen className="h-8 w-8 text-muted-foreground" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Study Time</p>
                <p className="text-2xl font-bold">{data.total_study_time}</p>
              </div>
              <Clock className="h-8 w-8 text-muted-foreground" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Words Learned</p>
                <p className="text-2xl font-bold">{data.total_words_learned}</p>
              </div>
              <Target className="h-8 w-8 text-muted-foreground" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Current Level</p>
                <p className="text-2xl font-bold">{data.level_type || "B2"}</p>
              </div>
              <TrendingUp className="h-8 w-8 text-muted-foreground" />
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Current Progress */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Current Courses</CardTitle>
            </CardHeader>
            {/* <CardContent className="space-y-4">
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Business English Mastery</span>
                    <span className="font-medium">75%</span>
                  </div>
                  <Progress value={75} className="h-2" />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Advanced Grammar</span>
                    <span className="font-medium">92%</span>
                  </div>
                  <Progress value={92} className="h-2" />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>IELTS Speaking Prep</span>
                    <span className="font-medium">45%</span>
                  </div>
                  <Progress value={45} className="h-2" />
                </div>
              </div>
            </CardContent> */}
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                Next Lessons
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                <div>
                  <h4 className="font-medium">Conditional Sentences</h4>
                  <p className="text-sm text-muted-foreground">
                    Advanced Grammar • 25 min
                  </p>
                </div>
                <Button size="sm">
                  <PlayCircle className="h-4 w-4 mr-2" />
                  Start
                </Button>
              </div>
              <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                <div>
                  <h4 className="font-medium">Business Presentations</h4>
                  <p className="text-sm text-muted-foreground">
                    Business English • 30 min
                  </p>
                </div>
                <Button size="sm" variant="outline">
                  Preview
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar Stats */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Learning Streak
              </CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <div className="text-4xl font-bold mb-2">7</div>
              <div className="text-muted-foreground mb-4">Days in a row</div>
              <div className="w-full bg-muted rounded-full h-2 mb-4">
                <div
                  className="bg-primary h-2 rounded-full"
                  style={{ width: "70%" }}
                ></div>
              </div>
              <p className="text-sm text-muted-foreground">
                3 more days to reach your goal!
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Recent Achievements</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center gap-3">
                <Award className="h-8 w-8 text-muted-foreground" />
                <div>
                  <p className="font-medium">Grammar Master</p>
                  <p className="text-xs text-muted-foreground">
                    Completed advanced grammar
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Award className="h-8 w-8 text-muted-foreground" />
                <div>
                  <p className="font-medium">Vocabulary Wizard</p>
                  <p className="text-xs text-muted-foreground">
                    Learned 1000+ words
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-accent border">
            <CardContent className="p-6 text-center">
              <h3 className="font-semibold mb-2">Keep it up! 🎉</h3>
              <p className="text-sm text-muted-foreground mb-4">
                You're 85% more active than average learners this week
              </p>
              <Button variant="default" size="sm">
                View Full Report
                <ArrowRight className="h-4 w-4 ml-2" />
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
