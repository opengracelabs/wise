"""Validation-only commerce provider adapters for RC7."""

from __future__ import annotations

from abc import ABC, abstractmethod

from wise_contracts import CommerceProviderValidation


class CommerceProvider(ABC):
    """Base class for commerce provider validation adapters."""

    provider: str
    display_name: str
    role: str
    capabilities: list[str]

    disabled_capabilities = [
        "checkout",
        "payment_authorization",
        "order_capture",
        "fulfillment_submission",
    ]

    @abstractmethod
    def validate(self) -> CommerceProviderValidation:
        """Return non-mutating provider readiness details."""


class ShopifyProvider(CommerceProvider):
    """Shopify storefront catalog adapter; no checkout is enabled."""

    provider = "shopify"
    display_name = "Shopify"
    role = "Storefront taxonomy, product metadata, collections, and analytics validation."
    capabilities = [
        "product_catalog_shape",
        "collection_routing",
        "product_view_events",
        "wishlist_intent_events",
    ]

    def validate(self) -> CommerceProviderValidation:
        return CommerceProviderValidation(
            provider="shopify",
            display_name=self.display_name,
            role=self.role,
            status="configured_for_validation",
            capabilities=self.capabilities,
            disabled_capabilities=self.disabled_capabilities,
            validation_notes=[
                "Storefront routes validate product discovery and buy-intent events only.",
                "Cart, checkout, taxes, shipping, and payments remain disabled for RC7.",
            ],
        )


class PrintfulProvider(CommerceProvider):
    """Printful print-on-demand adapter; product specs only."""

    provider = "printful"
    display_name = "Printful"
    role = "Poster, print, calendar, and puzzle production feasibility validation."
    capabilities = [
        "print_area_specification",
        "mockup_requirements",
        "sku_mapping",
        "production_feasibility",
    ]

    def validate(self) -> CommerceProviderValidation:
        return CommerceProviderValidation(
            provider="printful",
            display_name=self.display_name,
            role=self.role,
            status="configured_for_validation",
            capabilities=self.capabilities,
            disabled_capabilities=self.disabled_capabilities,
            validation_notes=[
                "Provider output is limited to product capability checks and mockup planning.",
                "Fulfillment submission is blocked until payment processing is approved.",
            ],
        )


class GelatoProvider(CommerceProvider):
    """Gelato global production adapter; validation only."""

    provider = "gelato"
    display_name = "Gelato"
    role = "Regional production coverage and format availability validation."
    capabilities = [
        "regional_availability",
        "localized_format_mapping",
        "sustainability_positioning",
        "shipping_coverage_estimate",
    ]

    def validate(self) -> CommerceProviderValidation:
        return CommerceProviderValidation(
            provider="gelato",
            display_name=self.display_name,
            role=self.role,
            status="configured_for_validation",
            capabilities=self.capabilities,
            disabled_capabilities=self.disabled_capabilities,
            validation_notes=[
                "Regional production options are assessed without creating orders.",
                "Shipping and tax estimates are intentionally out of scope for RC7.",
            ],
        )


def get_provider_validations() -> list[CommerceProviderValidation]:
    """Return all RC7 provider validations."""

    providers: list[CommerceProvider] = [
        ShopifyProvider(),
        PrintfulProvider(),
        GelatoProvider(),
    ]
    return [provider.validate() for provider in providers]
