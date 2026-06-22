import {
  bigCatsCollection,
  endangeredEarthSeries,
  getPlaceById,
  getSpeciesById,
  places,
  species,
} from "./demo-data";
import type { CollectionManifest, PlaceSummary, SeriesManifest, SpeciesSummary } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_PLATFORM_API_URL;

async function fetchFromPlatform<T>(path: string): Promise<T | null> {
  if (!API_BASE_URL) {
    return null;
  }

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      headers: { accept: "application/json" },
      next: { revalidate: 120 },
    });

    if (!response.ok) {
      return null;
    }

    return (await response.json()) as T;
  } catch {
    return null;
  }
}

export async function getCollection(slug: string): Promise<CollectionManifest> {
  const platformCollection = await fetchFromPlatform<CollectionManifest>(`/v1/collections/${slug}`);
  return platformCollection ?? bigCatsCollection;
}

export async function getSeries(slug: string): Promise<SeriesManifest> {
  const platformSeries = await fetchFromPlatform<SeriesManifest>(`/v1/series/${slug}`);
  return platformSeries ?? endangeredEarthSeries;
}

export async function getSpecies(id: string): Promise<SpeciesSummary | undefined> {
  const platformSpecies = await fetchFromPlatform<SpeciesSummary>(`/v1/species/${id}`);
  return platformSpecies ?? getSpeciesById(id);
}

export async function getPlace(id: string): Promise<PlaceSummary | undefined> {
  const platformPlace = await fetchFromPlatform<PlaceSummary>(`/v1/areas/${id}`);
  return platformPlace ?? getPlaceById(id);
}

export async function getCollectionMembers(collection: CollectionManifest) {
  return collection.members
    .slice()
    .sort((a, b) => a.order - b.order)
    .map((member) => ({
      member,
      species: species.find((item) => item.id === member.speciesId),
    }))
    .filter((item): item is { member: (typeof collection.members)[number]; species: SpeciesSummary } =>
      Boolean(item.species),
    );
}

export async function getRelatedPlaces(speciesId?: string): Promise<PlaceSummary[]> {
  if (!speciesId) {
    return places;
  }

  return places.filter((place) => place.speciesIds.includes(speciesId));
}

export async function getAllSpecies() {
  return species;
}

export async function getAllPlaces() {
  return places;
}
