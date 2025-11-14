# GLEIF Well-Known Directory Implementation Guide

**Version:** 1.0.0
**Last Updated:** 2025-11-14
**Status:** Current

## Overview

This guide describes the implementation of GLEIF's `.well-known` directory structure for discovering KERI OOBIs, vLEI credential schemas, and witness infrastructure.

## Architecture

### Simplified Flat Structure

All KERI resources (AIDs, witnesses, and schemas) are organized in a **single flat directory** under `.well-known/keri/oobi/`:

```text
.well-known/
├── index.json                                              # Main discovery index
├── index.html                                              # Human-readable directory
├── schema.json                                             # JSON Schema for index.json
├── SCHEMA.md                                               # Schema documentation
├── STRUCTURE.md                                            # Filesystem specification
└── keri/
    ├── index.html                                          # KERI directory page
    └── oobi/
        ├── index.json                                      # OOBI discovery index
        ├── index.html                                      # OOBI directory page
        ├── schema.json                                     # JSON Schema for OOBI index
        ├── EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2/   # AID (GLEIF RoOT)
        │   └── index.json
        ├── EINmHd5g7iV-UldkkkKyBIH052bIyxZNBn9pq-zNrYoS/   # AID (GLEIF External)
        │   └── index.json
        ├── EFcrtYzHx11TElxDmEDx355zm7nJhbmdcIluw7UMbUIL/   # AID (GLEIF Internal)
        │   └── index.json
        ├── BDkq35LUU63xnFmfhljYYRY0ymkCg7goyeCxN30tsvmS/   # Witness 1
        │   └── index.json
        ├── BDwydI_FJJ-tvAtCl1tIu_VQqYTI3Q0JyHDhO1v2hZBt/   # Witness 2
        │   └── index.json
        ├── ... (8 more witnesses)
        ├── ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY/   # Schema (Legal Entity vLEI)
        │   └── index.json
        ├── EBfdlu8R27Fbx-ehrqwImnK-8Cm79sqbAQ4MmvEAYqao/   # Schema (QVI vLEI)
        │   └── index.json
        └── ... (6 more schemas)
```

**Total Resources:** 21 identifiers (3 AIDs + 10 witnesses + 8 schemas)

## Key Design Principles

### 1. Flat Hierarchy

All identifiers exist at the same level - no `aids/`, `witnesses/`, or `schemas/` subdirectories.

**Benefits:**

- Simpler URL construction: `/.well-known/keri/oobi/{identifier}/index.json`
- Easier to maintain
- Consistent access pattern for all resource types

### 2. Simplified Index Format

Both index files use the same simple key-value structure:

```json
{
  "$schema": "https://gleif-it.github.io/.well-known/keri/oobi/schema.json",
  "aids": {
    "GLEIF RoOT": "EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2"
  },
  "witnesses": {
    "BDkq35LUU63xnFmfhljYYRY0ymkCg7goyeCxN30tsvmS": "BDkq35LUU63xnFmfhljYYRY0ymkCg7goyeCxN30tsvmS"
  },
  "schemas": {
    "LegalEntityvLEICredential": "ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY"
  }
}
```

### 3. Self-Describing with JSON Schema

All JSON files reference their validation schema via `$schema` property.

## URL Patterns

### Discovery Endpoints

| Resource | URL | Purpose |
|----------|-----|---------|
| Main Index | `/.well-known/index.json` | Top-level resource directory |
| OOBI Index | `/.well-known/keri/oobi/index.json` | Complete OOBI catalog |
| AID OOBI | `/.well-known/keri/oobi/{aid}/index.json` | Specific AID OOBI |
| Witness OOBI | `/.well-known/keri/oobi/{witness-id}/index.json` | Witness configuration |
| Schema OOBI | `/.well-known/keri/oobi/{schema-id}/index.json` | Schema definition |

### URL Construction

Given an identifier from the index:

```javascript
const baseUrl = "https://gleif-it.github.io";
const identifier = "EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2";
const oobiUrl = `${baseUrl}/.well-known/keri/oobi/${identifier}/index.json`;
```

## Resource Types

### GLEIF Autonomic Identifiers (AIDs)

**Count:** 3
**Prefix:** `E` (transferable)
**Location:** `/.well-known/keri/oobi/E{43-chars}/index.json`

Identifiers:

1. **GLEIF RoOT** - `EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2`
2. **GLEIF External** - `EINmHd5g7iV-UldkkkKyBIH052bIyxZNBn9pq-zNrYoS`
3. **GLEIF Internal** - `EFcrtYzHx11TElxDmEDx355zm7nJhbmdcIluw7UMbUIL`

### Witnesses

**Count:** 10
**Prefix:** `B` (non-transferable)
**Location:** `/.well-known/keri/oobi/B{43-chars}/index.json`

Example: `BDkq35LUU63xnFmfhljYYRY0ymkCg7goyeCxN30tsvmS`

### vLEI Credential Schemas

**Count:** 8
**Prefix:** `E` (SAID)
**Location:** `/.well-known/keri/oobi/E{43-chars}/index.json`

Schemas:

1. **LegalEntityvLEICredential** - `ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY`
2. **QualifiedvLEIIssuervLEICredential** - `EBfdlu8R27Fbx-ehrqwImnK-8Cm79sqbAQ4MmvEAYqao`
3. **OORAuthorizationvLEICredential** - `EKA57bKBKxr_kN7iN5i7lMUxpMG-s19dRcmov1iDxz-E`
4. **ECRAuthorizationvLEICredential** - `EH6ekLjSr8V32WyFbGe1zXjTzFs9PkTYmupJ9H65O14g`
5. **LegalEntityOfficialOrganizationalRolevLEICredential** - `EBNaNu-M9P5cgrnfl2Fvymy4E_jvxxyjb70PRtiANlJy`
6. **LegalEntityEngagementContextRolevLEICredential** - `EEy9PkikFcANV1l7EHukCeXqrzT1hNZjGlUk7wuMO5jw`
7. **iXBRLDataAttestation** - `EMhvwOlyEJ9kN4PrwCpr9Jsv7TxPhiYveZ0oP3lJzdEi`
8. **iXBRLDataAttestationSchema** - `EOxm1erpuJtjy9bBWO6Wgp9iggefDTNsM6DpO8-jUKbU`

## Implementation Workflow

### Adding a New Resource

#### 1. Create Directory

```bash
cd .well-known/keri/oobi/
mkdir {identifier}
```

#### 2. Create OOBI File

```bash
cat > {identifier}/index.json << 'EOF'
{
  "v": "KERI10JSON...",
  "t": "rpy",
  ...
}
EOF
```

#### 3. Update Indices

**Update `.well-known/keri/oobi/index.json`:**

```json
{
  "aids|witnesses|schemas": {
    "Human Readable Name": "{identifier}"
  }
}
```

**Update `.well-known/index.json`:**

```json
{
  "aids|witnesses|schemas": {
    "Human Readable Name": "{identifier}"
  }
}
```

#### 4. Validate

```bash
# Validate against schema
ajv validate -s .well-known/schema.json -d .well-known/index.json
ajv validate -s .well-known/keri/oobi/schema.json -d .well-known/keri/oobi/index.json
```

#### 5. Commit

```bash
git add .well-known/
git commit -m "Add {resource-type}: {name}"
```

### Removing a Resource

#### 1. Remove Directory

```bash
rm -rf .well-known/keri/oobi/{identifier}
```

#### 2. Update Indices

Remove the entry from both index.json files.

#### 3. Validate & Commit

Same as adding workflow.

## Discovery Protocol

### Client Implementation Example

```javascript
// 1. Fetch main index
const response = await fetch('https://gleif-it.github.io/.well-known/index.json');
const index = await response.json();

// 2. Get specific resource type
const rootAID = index.aids["GLEIF RoOT"];
// rootAID = "EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2"

// 3. Construct OOBI URL
const oobiUrl = `https://gleif-it.github.io/.well-known/keri/oobi/${rootAID}/index.json`;

// 4. Fetch OOBI
const oobiResponse = await fetch(oobiUrl);
const oobi = await oobiResponse.json();
```

### Python Example

```python
import requests

# Discover resources
index_url = "https://gleif-it.github.io/.well-known/index.json"
index = requests.get(index_url).json()

# Get all schemas
for schema_type, schema_id in index["schemas"].items():
    oobi_url = f"https://gleif-it.github.io/.well-known/keri/oobi/{schema_id}/index.json"
    schema_oobi = requests.get(oobi_url).json()
    print(f"{schema_type}: {schema_id}")
```

## Validation

### JSON Schema Validation

**Install validator:**

```bash
npm install -g ajv-cli
```

**Validate files:**

```bash
# Main index
ajv validate -s .well-known/schema.json -d .well-known/index.json

# OOBI index
ajv validate -s .well-known/keri/oobi/schema.json -d .well-known/keri/oobi/index.json
```

### Structure Validation

**Check directory structure:**

```bash
# All identifiers should be 44 characters
find .well-known/keri/oobi -mindepth 1 -maxdepth 1 -type d | while read dir; do
  basename "$dir" | grep -E '^[EB][A-Za-z0-9_-]{43}$' || echo "Invalid: $dir"
done

# Each should contain index.json
find .well-known/keri/oobi -mindepth 1 -maxdepth 1 -type d | while read dir; do
  [ -f "$dir/index.json" ] || echo "Missing index.json: $dir"
done
```

## Testing

### Local Testing

```bash
# Start local server
python -m http.server 8000

# Test endpoints
curl http://localhost:8000/.well-known/index.json
curl http://localhost:8000/.well-known/keri/oobi/index.json
curl http://localhost:8000/.well-known/keri/oobi/EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2/index.json
```

### Production Testing

```bash
# Test discovery
curl https://gleif-it.github.io/.well-known/index.json | jq

# Test OOBI index
curl https://gleif-it.github.io/.well-known/keri/oobi/index.json | jq

# Test specific OOBI
curl https://gleif-it.github.io/.well-known/keri/oobi/EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2/index.json | jq
```

### Automated Testing

```bash
#!/bin/bash
# test-structure.sh

BASE_URL="https://gleif-it.github.io"

# Test main index
echo "Testing main index..."
curl -sf "$BASE_URL/.well-known/index.json" | jq -e '.aids' > /dev/null || exit 1

# Test OOBI index
echo "Testing OOBI index..."
curl -sf "$BASE_URL/.well-known/keri/oobi/index.json" | jq -e '.aids' > /dev/null || exit 1

# Test each AID
for aid in $(curl -s "$BASE_URL/.well-known/index.json" | jq -r '.aids[]'); do
  echo "Testing AID: $aid"
  curl -sf "$BASE_URL/.well-known/keri/oobi/$aid/index.json" > /dev/null || exit 1
done

echo "All tests passed!"
```

## Migration from Old Structure

### What Changed

**Before (❌ Deprecated):**

```
.well-known/
├── schema/oobi/{id}/index.json
├── witness/oobi/{id}/index.json
└── keri/oobi/{id}/index.json
```

**After (✅ Current):**

```
.well-known/
└── keri/oobi/{id}/index.json
```

### Migration Steps

If you have the old structure:

1. **Move all identifiers to flat structure:**

   ```bash
   # Move schema OOBIs
   mv .well-known/schema/oobi/* .well-known/keri/oobi/

   # Move witness OOBIs
   mv .well-known/witness/oobi/* .well-known/keri/oobi/
   ```

2. **Remove old directories:**

   ```bash
   rm -rf .well-known/schema
   rm -rf .well-known/witness
   ```

3. **Update index files** using simplified format (see examples above)

4. **Update all path references** in HTML files from:
   - `/schema/oobi/{id}` → `/keri/oobi/{id}`
   - `/witness/oobi/{id}` → `/keri/oobi/{id}`

## Troubleshooting

### Common Issues

**Issue:** Schema validation fails
**Solution:** Check that all identifiers match CESR patterns (44 chars, correct prefix)

**Issue:** Missing resources in index
**Solution:** Ensure both `.well-known/index.json` and `.well-known/keri/oobi/index.json` are updated

**Issue:** 404 errors
**Solution:** Verify directory names match identifiers exactly (case-sensitive)

**Issue:** JSON parsing errors
**Solution:** Validate JSON syntax with `jq` or online validator

## Security Considerations

### HTTPS Required

All production deployments MUST use HTTPS to prevent:

- Man-in-the-middle attacks
- Content tampering
- Identifier spoofing

### CORS Headers

For web client access, configure appropriate CORS headers:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

### Rate Limiting

Consider rate limiting for discovery endpoints to prevent abuse.

## References

- [RFC 8615: Well-Known URIs](https://www.rfc-editor.org/rfc/rfc8615.html)
- [KERI Specification](https://trustoverip.github.io/kswg-keri-specification/)
- [CESR Specification](https://trustoverip.github.io/kswg-cesr-specification/)
- [JSON Schema](https://json-schema.org/)

## Additional Documentation

- **STRUCTURE.md** - Complete filesystem and URI specification
- **SCHEMA.md** - JSON Schema usage and validation guide
- **.well-known/schema.json** - Main index schema definition
- **.well-known/keri/oobi/schema.json** - OOBI index schema definition

## Support

For questions or issues:

- GitHub Issues: <https://github.com/GLEIF-IT/gleif-it.github.io/issues>
- GLEIF Contact: <https://www.gleif.org>
- Documentation: <https://gleif-it.github.io/.well-known/>
