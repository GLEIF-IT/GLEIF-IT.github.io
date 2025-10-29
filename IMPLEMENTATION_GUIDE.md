# Implementation Guide: OOBI Dual Structure

## Overview

This document describes the OOBI (Out-of-Band Introduction) dual directory structure in the GLEIF-IT GitHub Pages repository.

## Summary of Changes

Both `.well-known/{schema,keri,witness}/oobi/` and `/oobi/` directory structures exist. The `/oobi/` directory contains copies of files from `.well-known/schema/oobi/` and `.well-known/keri/oobi/` subdirectories.

## Change Type

Non-breaking. Both directory structures are maintained with synchronized content.

## URL Structures

Subdirectory structure:

```text
https://gleif-it.github.io/.well-known/schema/oobi/{ID}/index.json
https://gleif-it.github.io/.well-known/keri/oobi/{ID}/index.json
https://gleif-it.github.io/.well-known/witness/oobi/{ID}/index.json
```

Flat structure:

```text
https://gleif-it.github.io/oobi/{ID}/index.json
```

### Resource Availability

- Schema OOBIs: Available at both `/.well-known/schema/oobi/{ID}/` and `/oobi/{ID}/`
- KERI OOBIs: Available at both `/.well-known/keri/oobi/{ID}/` and `/oobi/{ID}/`
- Witness OOBIs: Available at `/.well-known/witness/oobi/{ID}/` only

## Affected OOBI IDs

### Schema OOBIs (7 files)

Available at both locations:

- `/.well-known/schema/oobi/{ID}/index.json`
- `/oobi/{ID}/index.json`

1. `ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY` - Legal Entity vLEI Credential
2. `EBfdlu8R27Fbx-ehrqwImnK-8Cm79sqbAQ4MmvEAYqao` - Qualified vLEI Issuer Credential
3. `EKA57bKBKxr_kN7iN5i7lMUxpMG-s19dRcmov1iDxz-E` - OOR Authorization vLEI Credential
4. `EH6ekLjSr8V32WyFbGe1zXjTzFs9PkTYmupJ9H65O14g` - ECR Authorization vLEI Credential
5. `EBNaNu-M9P5cgrnfl2Fvymy4E_jvxxyjb70PRtiANlJy` - Legal Entity Official Organizational Role vLEI Credential
6. `EEy9PkikFcANV1l7EHukCeXqrzT1hNZjGlUk7wuMO5jw` - Legal Entity Engagement Context Role vLEI Credential
7. `EMhvwOlyEJ9kN4PrwCpr9Jsv7TxPhiYveZ0oP3lJzdEi` - OOR vLEI Credential

### KERI OOBIs (3 files)

Available at both locations:

- `/.well-known/keri/oobi/{ID}/index.json`
- `/oobi/{ID}/index.json`

1. `EDP1vHcw_wc4M__Fj53-cJaBnZZASd-aMTaSyWEQ-PC2`
2. `EINmHd5g7iV-UldkkkKyBIH052bIyxZNBn9pq-zNrYoS`
3. `EFcrtYzHx11TElxDmEDx355zm7nJhbmdcIluw7UMbUIL`

### Witness OOBIs (10+ files)

Available at `/.well-known/witness/oobi/{ID}/index.json` only.

## Usage

### URL Patterns

Both patterns serve identical content:

Subdirectory structure:

```text
https://gleif-it.github.io/.well-known/schema/oobi/{ID}/index.json
https://gleif-it.github.io/.well-known/keri/oobi/{ID}/index.json
```

Flat structure:

```text
https://gleif-it.github.io/oobi/{ID}/index.json
```

## Maintainer Workflow

### Updating OOBI Files

1. Update files in `.well-known` structure:
   - Schema OOBIs: `.well-known/schema/oobi/{ID}/index.json`
   - KERI OOBIs: `.well-known/keri/oobi/{ID}/index.json`
   - Witness OOBIs: `.well-known/witness/oobi/{ID}/index.json`

2. Run sync script:

   ```bash
   ./create_oobi_copies.sh
   ```

3. Commit files from both directories

### Sync Script

**create_oobi_copies.sh**

- Copies OOBI files from `.well-known` to `/oobi/`
- Run after any `.well-known` file updates
- Creates necessary directories
- Reports copied files

## Technical Details

### Files

1. **create_oobi_copies.sh**
   - Copies OOBI files from `.well-known` to `/oobi/`

2. **OOBI files in `/oobi/` directory**
   - Copies of schema and KERI OOBIs from `.well-known`

### Directory Structure

```text
.well-known/
├── schema/oobi/{ID}/index.json
├── keri/oobi/{ID}/index.json
└── witness/oobi/{ID}/index.json

oobi/
└── {ID}/index.json
```

### Implementation

- `.well-known/{schema,keri,witness}/oobi/` subdirectories contain OOBIs organized by type
- `/oobi/` flat directory contains copies of schema and KERI OOBIs
- Script synchronizes from subdirectory structure to flat structure
- Both structures maintained for URL access flexibility

## Testing

### Verify Both URLs

```bash
# Canonical
curl https://gleif-it.github.io/.well-known/schema/oobi/ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY/index.json

# Convenience
curl https://gleif-it.github.io/oobi/ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY/index.json

# Verify identical
diff <(curl -s https://gleif-it.github.io/.well-known/schema/oobi/ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY/index.json) \
     <(curl -s https://gleif-it.github.io/oobi/ENPXp1vQzRF6JwIuS-mp2U8Uf1MoADoP_GqQ62VsDZWY/index.json)
```

## Resource Types

### Schema OOBIs

vLEI credential schemas

Available at:

- `https://gleif-it.github.io/.well-known/schema/oobi/{ID}/index.json`
- `https://gleif-it.github.io/oobi/{ID}/index.json`

### KERI OOBIs

Witness endpoint configurations for KERI infrastructure

Available at:

- `https://gleif-it.github.io/.well-known/keri/oobi/{ID}/index.json`
- `https://gleif-it.github.io/oobi/{ID}/index.json`

### Witness OOBIs

Witness network node information

Available at:

- `https://gleif-it.github.io/.well-known/witness/oobi/{ID}/index.json`

## Migration to .well-known

The `.well-known` subdirectory structure provides better organization by resource type and follows RFC 8615 conventions. While both URL patterns are supported, migrating to `.well-known` URLs is encouraged for new implementations.

Migration requires updating hardcoded URLs in:

- Application configuration
- API clients
- Documentation
- Scripts and automation

Both structures will continue to be maintained to support existing integrations.

## Future Deprecation

The `/oobi/` flat structure should be deprecated in favor of `.well-known` to align with RFC 8615 standards and improve resource organization. Deprecation would require:

- Notification to all consumers
- Documented migration timeline
- Updated documentation and examples
- Client implementation updates
- Monitoring of `/oobi/` usage patterns

This deprecation represents significant development effort and coordination across the ecosystem.
