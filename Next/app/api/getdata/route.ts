// import { randomInt } from "crypto"
// import { NextResponse } from "next/server"

export async function GET() {
  const VehicleId = process.env.NEXT_PUBLIC_TEST_VEHICLE_ID;
  const res = await fetch(`http://localhost:8000/GetDashbordData/${VehicleId}`, {
    method: "Get", 
    cache: "no-store" 
  });

  const data = await res.json();
  
  return Response.json(data);
}
