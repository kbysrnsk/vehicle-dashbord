import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
    const body = await req.json();
    const VehicleId = process.env.TEST_VEHICLE_ID;

    await fetch(`http://localhost:8000/UpdateLock/${VehicleId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  
    return NextResponse.json({ ok: true });
  }
  