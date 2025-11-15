# KERI Well-Known URI Structure Specification

## Version 1.0.0 - 2025-11-14

## Abstract

This document defines the URI structure and filesystem organization for `.well-known` directories that provide discovery endpoints for KERI OOBIs, ACDC schemas, and witness infrastructure.

## 1. Introduction

This specification provides a standardized method for discovering KERI (Key Event Receipt Infrastructure) resources, including Autonomic Identifiers (AIDs), ACDC (Authentic Chained Data Container) schemas, and witness network endpoints. Organizations implementing KERI can use this structure to publish their identifiers and schemas in a discoverable, standards-compliant manner.

## 2. URI Structure

### 2.1 Base URI

All KERI well-known resources are accessible under:

```text
https://{domain}/.well-known/
```

Where `{domain}` is the organization's domain (e.g., `example.org`, `gleif.org`).

### 2.2 Resource Hierarchy

```text
/.well-known/
├── index.json                           # Main discovery index (REQUIRED)
├── index.html                           # Human-readable directory (RECOMMENDED)
├── schema.json                          # JSON Schema for index.json (RECOMMENDED)
├── SCHEMA.md                            # Schema documentation (OPTIONAL)
├── STRUCTURE.md                         # This specification (OPTIONAL)
└── keri/                                # KERI resources (REQUIRED)
    └── oobi/                            # OOBI directory (REQUIRED)
        ├── index.json                   # OOBI discovery index (REQUIRED)
        ├── index.html                   # Human-readable OOBI directory (RECOMMENDED)
        ├── schema.json                  # JSON Schema for OOBI index (RECOMMENDED)
        ├── {aid}/                       # AID-specific OOBI (REQUIRED for each AID)
        │   └── index.json               # Multi-OOBI or OOBI array
        ├── {witness-id}/                # Witness-specific OOBI (REQUIRED for each witness)
        │   └── index.json               # Witness inception and endpoint OOBI
        └── {schema-id}/                 # Schema-specific OOBI (REQUIRED for each schema)
            └── index.json               # Schema definition or OOBI
```

## 3. URI Patterns

### 3.1 Discovery Endpoints

| URI | Purpose | Status |
|-----|---------|--------|
| `/.well-known/index.json` | Main resource index | REQUIRED |
| `/.well-known/keri/oobi/index.json` | OOBI index | REQUIRED |

### 3.2 OOBI Endpoints

All OOBI resources follow the pattern:

```text
/.well-known/keri/oobi/{identifier}/index.json
```

Where `{identifier}` is a CESR-encoded identifier:

- **AIDs** (transferable): Prefix `E`, 44 characters total
  - Example: `EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2`
- **Witnesses** (non-transferable): Prefix `B`, 44 characters total
  - Example: `BDkq35LUU63xnFmfhljYYRY0ymkCg7goyeCxN30tsvmS`
- **Schemas** (SAIDs): Prefix `E`, 44 characters total
  - Example: `ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY`

## 4. Directory Structure Rules

### 4.1 Naming Conventions

1. **Directory Names**
   - MUST use lowercase for static directories (`keri`, `oobi`)
   - MUST use exact CESR identifier for dynamic directories
   - MUST NOT include file extensions in directory names

2. **File Names**
   - Index files MUST be named `index.json` or `index.html`
   - Schema files MUST be named `schema.json`
   - Documentation files SHOULD use uppercase with `.md` extension

3. **Path Components**
   - MUST use forward slashes (`/`) as separators
   - MUST NOT include trailing slashes in canonical URIs
   - MUST be case-sensitive

### 4.2 File Requirements

Each identifier directory MUST contain:

```text
{identifier}/
└── index.json    # REQUIRED: OOBI or resource data
```

Optional files:

```text
{identifier}/
├── index.json    # REQUIRED
├── index.html    # OPTIONAL: Human-readable view
└── witness       # OPTIONAL: Witness-specific endpoint (for AIDs only)
```

### 4.3 Flat Structure Requirement

All identifier directories MUST exist at the same level under `/.well-known/keri/oobi/`:

```text
/.well-known/keri/oobi/
├── EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2/
├── BDkq35LUU63xnFmfhljYYRY0ymkCg7goyeCxN30tsvmS/
└── ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY/
```

## 5. Content Type Requirements

### 5.1 JSON Files

All `.json` files MUST:

- Use `application/json` content type
- Be valid JSON according to RFC 8259
- Use UTF-8 encoding
- Validate against their referenced schema (if `$schema` present)

### 5.2 HTML Files

All `.html` files SHOULD:

- Use `text/html` content type
- Be valid HTML5
- Include appropriate meta tags for SEO

### 5.3 Markdown Files

All `.md` files SHOULD:

- Use `text/markdown` content type
- Follow CommonMark specification

## 6. Discovery Protocol

### 6.1 Main Index Discovery

Clients discover GLEIF resources by fetching:

```text
GET /.well-known/index.json
```

Response contains references to all resource types:

```json
{
  "$schema": "https://example.org/.well-known/schema.json",
  "$id": "EAyAqJjqLHZqkF7gHoFEagEJNoqNa5TEZlDPdJaVC3GD",
  "name": "Example Organization KERI Resources",
  "oobi": "/keri/oobi/index.json",
  "aids": { "Organization Root": "EDP1vHcw_..." },
  "schemas": { "CredentialType": "ENPXp1v..." },
  "witnesses": { "BDkq35L...": "BDkq35L..." }
}
```

### 6.2 OOBI Index Discovery

Clients discover KERI OOBIs by fetching:

```text
GET /.well-known/keri/oobi/index.json
```

Response contains flat map of all identifiers:

```json
{
  "$schema": "https://example.org/.well-known/keri/oobi/schema.json",
  "aids": { "Organization Root": "EDP1vHcw_..." },
  "witnesses": { "BDkq35L...": "BDkq35L..." },
  "schemas": { "CredentialType": "ENPXp1v..." }
}
```

### 6.3 Individual OOBI Resolution

To resolve a specific OOBI:

```text
GET /.well-known/keri/oobi/{identifier}/index.json
```

## 7. URI Construction Rules

### 7.1 Constructing URIs from Index

Given an identifier from an index:

**From main index:**

```text
aids["Organization Root"] = "EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2"
→ /.well-known/keri/oobi/EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2/index.json
```

**From OOBI index:**

```text
witnesses["BDkq35L..."] = "BDkq35L..."
→ /.well-known/keri/oobi/BDkq35L.../index.json
```

### 7.2 Pattern

```text
BASE_URI + "/keri/oobi/" + IDENTIFIER + "/index.json"
```

## 8. Filesystem Mapping

### 8.1 Web Server Configuration

The filesystem MUST mirror the URI structure:

**Filesystem:**

```text
/var/www/.well-known/keri/oobi/EDP1vHcw_.../index.json
```

**URI:**

```text
https://example.com/.well-known/keri/oobi/EDP1vHcw_.../index.json
```

### 8.2 Static Hosting

For static hosts (GitHub Pages, Netlify, etc.):

- Directory structure MUST match URI paths exactly
- Filename `index.json` allows path-based access
- Example: `/keri/oobi/{id}/` → serves `index.json`

## 9. Constraints

### 9.1 Identifier Constraints

1. **Length**: All CESR identifiers MUST be exactly 44 characters
2. **Character Set**: MUST use Base64URL alphabet: `[A-Za-z0-9_-]`
3. **Prefix**: First character indicates type:
   - `E`: Transferable AID or SAID
   - `B`: Non-transferable AID (witness)
   - Other prefixes reserved for future use

### 9.2 Path Constraints

1. **Depth**: Maximum path depth is 5 levels from root
   - Example: `/.well-known/keri/oobi/{id}/index.json` = 5 levels
2. **Length**: Total URI length SHOULD NOT exceed 2048 characters
3. **Characters**: Path components MUST NOT contain:
   - Whitespace
   - Query parameters in canonical paths
   - Fragment identifiers in canonical paths

## 10. Examples

### 10.1 Complete Structure Example

```text
example.org/
└── .well-known/
    ├── index.json                                              # Main index
    ├── index.html                                              # Human directory
    ├── schema.json                                             # Main schema
    └── keri/
        └── oobi/
            ├── index.json                                      # OOBI index
            ├── schema.json                                     # OOBI schema
            ├── EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2/   # Organization Root AID
            │   └── index.json
            ├── EINmHd5g7iV-UldkkkKyBIH052bIyxZNBn9pq-zNrYoS/   # Additional AID
            │   └── index.json
            ├── BDkq35LUU63xnFmfhljYYRY0ymkCg7goyeCxN30tsvmS/   # Witness 1
            │   └── index.json
            └── ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY/   # ACDC Schema
                └── index.json
```

### 10.2 URI Examples

```text
# Discovery
https://example.org/.well-known/index.json
https://example.org/.well-known/keri/oobi/index.json

# AIDs
https://example.org/.well-known/keri/oobi/EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2/index.json

# Witnesses
https://example.org/.well-known/keri/oobi/BDkq35LUU63xnFmfhljYYRY0ymkCg7goyeCxN30tsvmS/index.json

# ACDC Schemas
https://example.org/.well-known/keri/oobi/ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY/index.json
```

## 11. Versioning

### 11.1 Specification Version

This specification uses semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible structural changes
- **MINOR**: Backward-compatible additions
- **PATCH**: Backward-compatible fixes

Current version: **1.0.0**

### 11.2 Content Versioning

Individual JSON files include version information:

```json
{
  "version": "1.0.0",
  "updated": "2025-11-14"
}
```

## 12. Security Considerations

### 12.1 Access Control

Well-known URIs are public by design. Implementations MUST NOT:

- Require authentication for access
- Apply rate limiting that prevents legitimate discovery
- Serve different content based on client identity

## 14. References

- [RFC 8615: Well-Known URIs](https://www.rfc-editor.org/rfc/rfc8615.html)
- [KERI Specification](https://trustoverip.github.io/kswg-keri-specification/)
- [CESR Specification](https://trustoverip.github.io/kswg-cesr-specification/)
- [JSON Schema](https://json-schema.org/)

## Appendix A: Reference Implementation

See the GLEIF reference implementation for a complete working example:

- Repository: <https://github.com/GLEIF-IT/gleif-it.github.io>
- Live site: <https://gleif-it.github.io/.well-known/>
- Specification: This document

Organizations implementing this specification should adapt the structure to their own domain and resource types while maintaining compliance with the patterns defined herein.
