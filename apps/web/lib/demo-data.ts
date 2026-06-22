import type { CollectionManifest, PlaceSummary, SeriesManifest, SpeciesSummary } from "./types";

export const species: SpeciesSummary[] = [
  {
    id: "panthera-leo",
    scientificName: "Panthera leo",
    commonName: "Lion",
    imageUrl:
      "https://images.unsplash.com/photo-1546182990-dffeafbe841d?auto=format&fit=crop&w=1200&q=80",
    conservationStatus: "Vulnerable",
    range: "Sub-Saharan Africa and Gir Forest, India",
    populationTrend: "Decreasing",
    sourceBadges: ["GBIF", "IUCN", "Wikidata"],
    summary:
      "A social big cat with a highly visible conservation story and strong public-recognition value for RC4 demand testing.",
    places: ["serengeti-national-park", "gir-national-park"],
  },
  {
    id: "panthera-tigris",
    scientificName: "Panthera tigris",
    commonName: "Tiger",
    imageUrl:
      "https://images.unsplash.com/photo-1562552476-8ac59b2a2e46?auto=format&fit=crop&w=1200&q=80",
    conservationStatus: "Endangered",
    range: "South and Southeast Asia",
    populationTrend: "Decreasing",
    sourceBadges: ["GBIF", "IUCN"],
    summary:
      "An endangered apex predator used to test conservation-status display, taxonomy context, and collection click-through.",
    places: ["sundarbans-reserve-forest"],
  },
  {
    id: "panthera-pardus",
    scientificName: "Panthera pardus",
    commonName: "Leopard",
    imageUrl:
      "https://images.unsplash.com/photo-1456926631375-92c8ce872def?auto=format&fit=crop&w=1200&q=80",
    conservationStatus: "Vulnerable",
    range: "Africa and parts of Asia",
    populationTrend: "Decreasing",
    sourceBadges: ["GBIF", "IUCN"],
    summary:
      "A wide-ranging species that helps validate collection cards, range summaries, and related protected-area rollups.",
    places: ["kruger-national-park"],
  },
  {
    id: "panthera-onca",
    scientificName: "Panthera onca",
    commonName: "Jaguar",
    imageUrl:
      "https://images.unsplash.com/photo-1602491453631-e2a5ad90a131?auto=format&fit=crop&w=1200&q=80",
    conservationStatus: "Near Threatened",
    range: "Central and South America",
    populationTrend: "Decreasing",
    sourceBadges: ["GBIF", "IUCN"],
    summary:
      "A charismatic Neotropical cat for testing map-interest behavior and cross-linking to protected landscapes.",
    places: ["pantanal-conservation-area"],
  },
  {
    id: "panthera-uncia",
    scientificName: "Panthera uncia",
    commonName: "Snow leopard",
    imageUrl:
      "https://images.unsplash.com/photo-1604574182638-965b8576d49f?auto=format&fit=crop&w=1200&q=80",
    conservationStatus: "Vulnerable",
    range: "High mountains of Central and South Asia",
    populationTrend: "Decreasing",
    sourceBadges: ["GBIF", "IUCN"],
    summary:
      "A mountain species that tests whether users engage with fragile habitat stories beyond globally famous cats.",
    places: ["hemis-national-park"],
  },
];

export const places: PlaceSummary[] = [
  {
    id: "serengeti-national-park",
    title: "Serengeti National Park",
    designationType: "Protected Area",
    country: "Tanzania",
    iucnCategory: "II",
    imageUrl:
      "https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1200&q=80",
    summary: "A savanna protected area central to lion conservation and migration storytelling.",
    speciesIds: ["panthera-leo", "panthera-pardus"],
  },
  {
    id: "gir-national-park",
    title: "Gir National Park",
    designationType: "Protected Area",
    country: "India",
    iucnCategory: "II",
    imageUrl:
      "https://images.unsplash.com/photo-1474314881477-04c4aac40a0e?auto=format&fit=crop&w=1200&q=80",
    summary: "The last wild stronghold of Asiatic lions, useful for place-to-species demand testing.",
    speciesIds: ["panthera-leo"],
  },
  {
    id: "pantanal-conservation-area",
    title: "Pantanal Conservation Area",
    designationType: "Protected Area",
    country: "Brazil",
    iucnCategory: "VI",
    imageUrl:
      "https://images.unsplash.com/photo-1610147323479-a7fb11ffd5dd?auto=format&fit=crop&w=1200&q=80",
    summary: "A wetland landscape associated with jaguar visibility and conservation tourism.",
    speciesIds: ["panthera-onca"],
  },
];

export const bigCatsCollection: CollectionManifest = {
  slug: "big-cats-of-the-world",
  stableId: "rc4-big-cats-of-the-world",
  title: "Big Cats of the World",
  subtitle: "A field-guide style collection for validating publishing demand.",
  description:
    "A live RC4 demonstration collection that groups quality-cleared species entities into a public-facing editorial surface.",
  heroImageUrl:
    "https://images.unsplash.com/photo-1534188753412-3e26d0d618d6?auto=format&fit=crop&w=1600&q=80",
  publicationState: "published",
  qualityApproved: true,
  rightsVerified: true,
  accessibilityCompliant: true,
  standardsValidated: true,
  benchmarkValidated: true,
  auditPacketComplete: true,
  featuredSpeciesId: "panthera-leo",
  sourceRefs: ["GBIF", "IUCN", "Protected Planet", "OpenStreetMap"],
  members: species.map((item, index) => ({
    speciesId: item.id,
    order: index + 1,
    editorialNote: `${item.commonName} anchors collection section ${index + 1}.`,
  })),
};

export const endangeredEarthSeries: SeriesManifest = {
  slug: "endangered-earth",
  stableId: "rc5-endangered-earth-series",
  title: "Endangered Earth Series",
  description:
    "A multi-part RC5 demonstration series for testing whether collections, species, and places create durable audience interest.",
  heroImageUrl:
    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1600&q=80",
  publicationState: "published",
  featuredCollectionSlug: "big-cats-of-the-world",
  qualityApproved: true,
  benchmarkValidated: true,
  auditPacketComplete: true,
  sections: [
    {
      id: "big-cats-of-the-world",
      order: 1,
      title: "Big Cats of the World",
      status: "published",
      summary: "A charismatic species-led collection testing immediate public interest.",
      href: "/collections/big-cats-of-the-world",
    },
    {
      id: "protected-areas-in-crisis",
      order: 2,
      title: "Protected Areas in Crisis",
      status: "editorial_review",
      summary: "A place-led installment planned for RC3 protected-area validation.",
      href: "/places/serengeti-national-park",
    },
    {
      id: "field-notes-from-the-edge",
      order: 3,
      title: "Field Notes from the Edge",
      status: "draft",
      summary: "A draft storytelling slot for future approved conservation narratives.",
      href: "/series/endangered-earth",
    },
  ],
};

export function getSpeciesById(id: string) {
  return species.find((item) => item.id === id);
}

export function getPlaceById(id: string) {
  return places.find((item) => item.id === id);
}
