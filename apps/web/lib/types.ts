export type ConservationStatus =
  | "Least Concern"
  | "Near Threatened"
  | "Vulnerable"
  | "Endangered"
  | "Critically Endangered";

export type InterestResponse = "yes" | "maybe" | "no";

export interface SpeciesSummary {
  id: string;
  scientificName: string;
  commonName: string;
  imageUrl: string;
  conservationStatus: ConservationStatus;
  range: string;
  populationTrend: "Increasing" | "Stable" | "Decreasing" | "Unknown";
  sourceBadges: string[];
  summary: string;
  places: string[];
}

export interface PlaceSummary {
  id: string;
  title: string;
  designationType: string;
  country: string;
  iucnCategory: string;
  imageUrl: string;
  summary: string;
  speciesIds: string[];
}

export interface CollectionMember {
  speciesId: string;
  order: number;
  editorialNote: string;
}

export interface CollectionManifest {
  slug: string;
  stableId: string;
  title: string;
  subtitle: string;
  description: string;
  heroImageUrl: string;
  publicationState: "draft" | "approved" | "published";
  qualityApproved: boolean;
  rightsVerified: boolean;
  accessibilityCompliant: boolean;
  standardsValidated: boolean;
  benchmarkValidated: boolean;
  auditPacketComplete: boolean;
  members: CollectionMember[];
  featuredSpeciesId: string;
  sourceRefs: string[];
}

export interface SeriesSection {
  id: string;
  order: number;
  title: string;
  status: "published" | "editorial_review" | "draft";
  summary: string;
  href: string;
}

export interface SeriesManifest {
  slug: string;
  stableId: string;
  title: string;
  description: string;
  heroImageUrl: string;
  publicationState: "draft" | "approved" | "published";
  featuredCollectionSlug: string;
  sections: SeriesSection[];
  qualityApproved: boolean;
  benchmarkValidated: boolean;
  auditPacketComplete: boolean;
}
