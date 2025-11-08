"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Coins, DollarSign, CheckCircle, AlertCircle } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { Toaster } from "@/components/ui/toaster"

const API_BASE = "/api"

interface CoinRequest {
  _id: string
  name: string
  account_number?: string
  userUid: string
  amount: number
}

interface MoneyRequest {
  _id: string
  name: string
  account_number?: string
  userUid: string
  amount: number
}

export default function AdminDashboard() {
  const [coinRequests, setCoinRequests] = useState<CoinRequest[]>([])
  const [moneyRequests, setMoneyRequests] = useState<MoneyRequest[]>([])
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()

  const fetchCoinRequests = async () => {
    try {
      const response = await fetch(`${API_BASE}/coin/requests/pending`)
      if (response.ok) {
        const data = await response.json()
        console.log("[v0] Coin requests response:", data)
        setCoinRequests(data.pending_requests || [])
      }
    } catch (error) {
      console.error("[v0] Error fetching coin requests:", error)
    }
  }

  const fetchMoneyRequests = async () => {
    try {
      const response = await fetch(`${API_BASE}/money/requests/pending`)
      if (response.ok) {
        const data = await response.json()
        console.log("[v0] Money requests response:", data)
        setMoneyRequests(data.pending_requests || [])
      }
    } catch (error) {
      console.error("[v0] Error fetching money requests:", error)
    }
  }

  useEffect(() => {
    fetchCoinRequests()
    fetchMoneyRequests()
  }, [])

  const handleGiveCoin = async (userUid: string) => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/coin/give/${userUid}`, {
        method: "POST",
      })

      if (response.ok) {
        toast({
          title: "코인 지급 완료",
          description: `사용자 ${userUid}에게 코인이 성공적으로 지급되었습니다.`,
        })
        await fetchCoinRequests()
      } else {
        throw new Error("Failed to give coin")
      }
    } catch (error) {
      toast({
        title: "오류",
        description: "코인 지급 중 오류가 발생했습니다.",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  const handleGiveMoney = async (userUid: string) => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE}/money/give/${userUid}`, {
        method: "POST",
      })

      if (response.ok) {
        toast({
          title: "머니 송금 완료",
          description: `사용자 ${userUid}에게 머니가 성공적으로 송금되었습니다.`,
        })
        await fetchMoneyRequests()
      } else {
        throw new Error("Failed to give money")
      }
    } catch (error) {
      toast({
        title: "오류",
        description: "머니 송금 중 오류가 발생했습니다.",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
              <DollarSign className="h-6 w-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-xl font-semibold text-foreground">관리자 대시보드</h1>
              <p className="text-sm text-muted-foreground">코인 및 머니 요청 관리</p>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="mb-8 grid gap-4 md:grid-cols-2">
          <Card className="border-blue-500/20 bg-gradient-to-br from-blue-500/5 to-blue-500/10">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Coins className="h-5 w-5 text-blue-500" />
                <CardTitle className="text-foreground">코인 요청</CardTitle>
              </div>
              <CardDescription>대기 중인 코인 충전 요청</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-foreground">{coinRequests.length}</div>
              <p className="mt-1 text-sm text-muted-foreground">건의 요청 대기 중</p>
            </CardContent>
          </Card>

          <Card className="border-green-500/20 bg-gradient-to-br from-green-500/5 to-green-500/10">
            <CardHeader>
              <div className="flex items-center gap-2">
                <DollarSign className="h-5 w-5 text-green-500" />
                <CardTitle className="text-foreground">머니 요청</CardTitle>
              </div>
              <CardDescription>대기 중인 머니 송금 요청</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-foreground">{moneyRequests.length}</div>
              <p className="mt-1 text-sm text-muted-foreground">건의 요청 대기 중</p>
            </CardContent>
          </Card>
        </div>

        <Tabs defaultValue="coin" className="w-full">
          <TabsList className="grid w-full max-w-md grid-cols-2">
            <TabsTrigger value="coin">코인 요청</TabsTrigger>
            <TabsTrigger value="money">머니 요청</TabsTrigger>
          </TabsList>

          <TabsContent value="coin" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-foreground">코인 충전 요청 목록</CardTitle>
                <CardDescription>사용자가 요청한 코인 충전을 승인하세요</CardDescription>
              </CardHeader>
              <CardContent>
                {coinRequests.length === 0 ? (
                  <div className="flex flex-col items-center justify-center py-12 text-center">
                    <AlertCircle className="mb-4 h-12 w-12 text-muted-foreground" />
                    <p className="text-lg font-medium text-foreground">대기 중인 요청이 없습니다</p>
                    <p className="mt-1 text-sm text-muted-foreground">새로운 코인 충전 요청이 오면 여기에 표시됩니다</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {coinRequests.map((request) => (
                      <div
                        key={request._id}
                        className="flex items-center justify-between rounded-lg border border-border bg-card p-4 transition-colors hover:bg-accent"
                      >
                        <div className="flex-1">
                          <div className="mb-2">
                            <p className="text-lg font-semibold text-foreground">{request.name}</p>
                          </div>
                          <div className="flex items-center gap-2 flex-wrap">
                            <p className="font-mono text-xs text-muted-foreground">{request.userUid}</p>
                            {request.account_number && (
                              <p className="font-mono text-xs text-muted-foreground">계좌: {request.account_number}</p>
                            )}
                            <Badge variant="secondary" className="bg-blue-500/10 text-blue-600 dark:text-blue-400">
                              코인
                            </Badge>
                          </div>
                          <p className="mt-2 text-2xl font-bold text-foreground">
                            {request.amount.toLocaleString()} 코인
                          </p>
                        </div>
                        <Button
                          onClick={() => handleGiveCoin(request.userUid)}
                          disabled={loading}
                          className="gap-2 bg-blue-600 hover:bg-blue-700"
                        >
                          <CheckCircle className="h-4 w-4" />
                          승인
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="money" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-foreground">머니 송금 요청 목록</CardTitle>
                <CardDescription>사용자가 요청한 머니 송금을 승인하세요</CardDescription>
              </CardHeader>
              <CardContent>
                {moneyRequests.length === 0 ? (
                  <div className="flex flex-col items-center justify-center py-12 text-center">
                    <AlertCircle className="mb-4 h-12 w-12 text-muted-foreground" />
                    <p className="text-lg font-medium text-foreground">대기 중인 요청이 없습니다</p>
                    <p className="mt-1 text-sm text-muted-foreground">새로운 머니 송금 요청이 오면 여기에 표시됩니다</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {moneyRequests.map((request) => (
                      <div
                        key={request._id}
                        className="flex items-center justify-between rounded-lg border border-border bg-card p-4 transition-colors hover:bg-accent"
                      >
                        <div className="flex-1">
                          <div className="mb-2">
                            <p className="text-lg font-semibold text-foreground">{request.name}</p>
                          </div>
                          <div className="flex items-center gap-2 flex-wrap">
                            <p className="font-mono text-xs text-muted-foreground">{request.userUid}</p>
                            {request.account_number && (
                              <p className="font-mono text-xs text-muted-foreground">계좌: {request.account_number}</p>
                            )}
                            <Badge variant="secondary" className="bg-green-500/10 text-green-600 dark:text-green-400">
                              머니
                            </Badge>
                          </div>
                          <p className="mt-2 text-2xl font-bold text-foreground">₩{request.amount.toLocaleString()}</p>
                        </div>
                        <Button
                          onClick={() => handleGiveMoney(request.userUid)}
                          disabled={loading}
                          className="gap-2 bg-green-600 hover:bg-green-700"
                        >
                          <CheckCircle className="h-4 w-4" />
                          승인
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
      <Toaster />
    </div>
  )
}
