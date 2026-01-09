import { GoogleMap, Marker, useJsApiLoader } from "@react-google-maps/api";

interface PositionProps {
  position: {
    lat : number
    lng : number
  }
}

export default function Map({position} : PositionProps) {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!,
  });

  if (!isLoaded) return <p className="text-white">Loading map...</p>;

  return (
    <div className="w-full h-full">
      <GoogleMap
        mapContainerClassName="w-full h-full"
        center={position}
        zoom={16}
        options={{
          disableDefaultUI: true,
          gestureHandling: "none",
          zoomControl: false,
          fullscreenControl: false,
          streetViewControl: false,
          mapTypeControl: false,
        }}
      >
        <Marker position={position} />
      </GoogleMap>
    </div>
  );
}
