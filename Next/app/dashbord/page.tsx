import DataBridge from "@/components/DataBridge/DataBridge";

export default async function Page() {
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL
  const res = await fetch(`${baseUrl}/api/getdata`, { cache: "no-store", });
  const initialdata = await res.json();
  return (
    <div>
      <DataBridge initialdata = {initialdata}/>
    </div>
  )
}
  