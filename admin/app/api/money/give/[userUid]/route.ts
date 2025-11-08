import { NextResponse } from "next/server"

const API_BASE = "https://bedbet.knpu.re.kr/api"

export async function POST(request: Request, { params }: { params: Promise<{ userUid: string }> }) {
  try {
    const { userUid } = await params

    const response = await fetch(`${API_BASE}/money/give/${userUid}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${process.env.API_TOKEN}`,
      },
    })

    if (!response.ok) {
      return NextResponse.json({ error: "Failed to give money" }, { status: response.status })
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error("Error giving money:", error)
    return NextResponse.json({ error: "Internal server error" }, { status: 500 })
  }
}
