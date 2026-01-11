// import { randomInt } from "crypto"
// import { NextResponse } from "next/server"

export async function GET() {
  const VehicleId = process.env.NEXT_PUBLIC_TEST_VEHICLE_ID;
  const api = process.env.NEXT_PUBLIC_API_URL;
  const res = await fetch(`${api}/GetDashbordData/${VehicleId}`, {
    method: "Get", 
    cache: "no-store" 
  });

  const data = await res.json();
  
  return Response.json(data);
}
