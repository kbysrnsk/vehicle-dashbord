import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
    const body = await req.json();
    const VehicleId = process.env.NEXT_PUBLIC_TEST_VEHICLE_ID;
    const api = process.env.NEXT_PUBLIC_API_URL;

    await fetch(`${api}/UpdateLock/${VehicleId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  
    return NextResponse.json({ ok: true });
  }
  