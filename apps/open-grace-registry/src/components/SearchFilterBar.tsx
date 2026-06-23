"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useCallback } from "react";

export interface FilterField {
  name: string;
  label: string;
  options: { value: string; label: string }[];
}

interface SearchFilterBarProps {
  basePath: string;
  searchPlaceholder: string;
  filters?: FilterField[];
}

export function SearchFilterBar({
  basePath,
  searchPlaceholder,
  filters = [],
}: SearchFilterBarProps) {
  const router = useRouter();
  const searchParams = useSearchParams();

  const updateParam = useCallback(
    (key: string, value: string) => {
      const params = new URLSearchParams(searchParams.toString());
      if (value) {
        params.set(key, value);
      } else {
        params.delete(key);
      }
      router.push(`${basePath}?${params.toString()}`);
    },
    [basePath, router, searchParams],
  );

  return (
    <div className="search-filter-bar">
      <input
        type="search"
        placeholder={searchPlaceholder}
        defaultValue={searchParams.get("q") ?? ""}
        onChange={(e) => updateParam("q", e.target.value)}
        aria-label="Search"
      />
      {filters.map((filter) => (
        <select
          key={filter.name}
          aria-label={filter.label}
          value={searchParams.get(filter.name) ?? ""}
          onChange={(e) => updateParam(filter.name, e.target.value)}
        >
          <option value="">{filter.label}</option>
          {filter.options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      ))}
    </div>
  );
}
