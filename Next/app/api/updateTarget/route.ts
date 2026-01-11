import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
    const VehicleId = process.env.NEXT_PUBLIC_TEST_VEHICLE_ID;
    const api = process.env.NEXT_PUBLIC_API_URL;
    const body = await req.json();
    const res = await fetch(`${api}/UpdateTarget/${VehicleId}`, {
      method: "POST", 
      headers: { "Content-Type": "application/json" }, 
      body: JSON.stringify(body),
    });
  
    const data = await res.json();
    return NextResponse.json(data);
  }