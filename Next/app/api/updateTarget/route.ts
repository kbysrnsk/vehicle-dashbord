import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
    const VehicleId = process.env.TEST_VEHICLE_ID;
    const body = await req.json();
    const res = await fetch(`http://localhost:8000/UpdateTarget/${VehicleId}`, {
      method: "POST", 
      headers: { "Content-Type": "application/json" }, 
      body: JSON.stringify(body),
    });
  
    const data = await res.json();
    return NextResponse.json(data);
  }