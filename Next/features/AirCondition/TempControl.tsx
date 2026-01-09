import { useState, useCallback } from "react";

type TempCntlProps = {
  initial?: number;
  onChange?: (value: number) => void;
};

const MIN_TEMP = 16;
const MAX_TEMP = 30;

export function TempControl({ initial = 22, onChange }: TempCntlProps) {
  const [temp, setTemp] = useState(initial);

  const updateTemp = useCallback(
    (value: number) => {
      const clamped = Math.min(Math.max(value, MIN_TEMP), MAX_TEMP);
      setTemp(clamped);
      onChange?.(clamped);
    },
    [onChange]
  );

  return (
    <div className="w-56 mx-auto text-center select-none">
      <p className="text-lg mb-2 font-medium">温度設定</p>

      <p className="text-5xl font-bold mb-4">{temp}℃</p>

      <div className="flex justify-between">
        <button
          className="w-24 h-14 text-3xl bg-gray-200 hover:bg-gray-300 active:bg-gray-400 rounded-xl shadow transition"
          onClick={() => updateTemp(temp - 1)}
        >
          -
        </button>

        <button
          className="w-24 h-14 text-3xl bg-gray-200 hover:bg-gray-300 active:bg-gray-400 rounded-xl shadow transition"
          onClick={() => updateTemp(temp + 1)}
        >
          +
        </button>
      </div>
    </div>
  );
}
