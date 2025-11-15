# KERI Well-Known Directory JSON Schema

This document describes the JSON Schema definitions for KERI `.well-known` directory structures.

## Schema Files

### 1. `.well-known/schema.json`

Defines the structure for the main `.well-known/index.json` file.

**Location:** `https://{domain}/.well-known/schema.json`

**Purpose:** Validates the top-level well-known directory index containing all KERI resources.

**Key Properties:**

- `$id` - Self-addressing identifier (SAID) for the index
- `aids` - Map of human-readable names to Autonomic Identifiers
- `schemas` - Map of credential types to schema SAIDs
- `witnesses` - Map of witness AIDs (self-referential)
- `metadata` - Organization and contact information

### 2. `.well-known/keri/oobi/schema.json`

Defines the structure for the KERI OOBI index at `.well-known/keri/oobi/index.json`.

**Location:** `https://{domain}/.well-known/keri/oobi/schema.json`

**Purpose:** Validates the KERI OOBI directory containing AIDs, witnesses, and schemas.

**Key Properties:**

- `aids` - Autonomic Identifiers (prefix: `E`)
- `witnesses` - Witness identifiers (prefix: `B`)
- `schemas` - Schema SAIDs (prefix: `E`)

## CESR Identifier Patterns

All identifiers follow the [CESR (Composable Event Streaming Representation)](https://trustoverip.github.io/kswg-cesr-specification/) format:

### AID Patterns

- **Transferable AIDs** (organization identifiers, schemas): `E[A-Za-z0-9_-]{43}`
  - Prefix `E` indicates Ed25519 public key or Blake3-256 digest
  - 44 characters total (1 prefix + 43 Base64URL)

- **Non-Transferable AIDs** (witnesses): `B[A-Za-z0-9_-]{43}`
  - Prefix `B` indicates Ed25519 non-transferable identifier
  - 44 characters total

### Schema Type Patterns

Schema credential types typically match patterns like:

- `*Credential` - Standard credential types
- `*Attestation` or `*AttestationSchema` - Attestation types

Organizations define their own credential type naming conventions.

## Validation

### Using JSON Schema Validators

**Command line (ajv-cli):**

```bash
# Install ajv-cli
npm install -g ajv-cli

# Validate main index
ajv validate -s .well-known/schema.json -d .well-known/index.json

# Validate OOBI index
ajv validate -s .well-known/keri/oobi/schema.json -d .well-known/keri/oobi/index.json
```

**Python (jsonschema):**

```python
import json
from jsonschema import validate

# Load schema
with open('.well-known/schema.json') as f:
    schema = json.load(f)

# Load and validate data
with open('.well-known/index.json') as f:
    data = json.load(f)
    validate(instance=data, schema=schema)
```

**JavaScript/TypeScript:**

```javascript
import Ajv from 'ajv';
import schema from './.well-known/schema.json';
import data from './.well-known/index.json';

const ajv = new Ajv();
const validate = ajv.compile(schema);
const valid = validate(data);

if (!valid) {
  console.log(validate.errors);
}
```

## Schema Evolution

### Version History

- `1.0.0` (2025-11-14) - Initial schema definition with simplified flat structure

### Adding New Fields

When extending the schema:

1. Increment version in `index.json`
2. Update schema file with new fields
3. Mark new fields as optional (not in `required` array) for backward compatibility
4. Document changes in this file

### Breaking Changes

Breaking changes require:

1. Major version increment (e.g., `1.0.0` → `2.0.0`)
2. Migration guide for existing implementations
3. Parallel support period for old schema

## Structure Overview

```text
.well-known/
├── schema.json                    # JSON Schema for index.json
├── index.json                     # Main index (validated by schema.json)
├── index.html                     # Human-readable directory
└── keri/
    └── oobi/
        ├── schema.json            # JSON Schema for OOBI index
        ├── index.json             # OOBI index (validated by schema.json)
        ├── index.html             # Human-readable OOBI directory
        ├── {aid}/index.json       # Organization AID OOBIs
        ├── {witness}/index.json   # Witness OOBIs
        └── {schema}/index.json    # Schema OOBIs
```

## Example Usage

### Main Index Structure

```json
{
  "$schema": "https://example.org/.well-known/schema.json",
  "$id": "placeholder",
  "name": "Example Organization KERI Resources",
  "version": "1.0.0",
  "updated": "2025-11-14",
  "oobi": "/keri/oobi/index.json",
  "aids": {
    "Organization Root": "placeholder"
  },
  "schemas": {
    "CredentialType": "placeholder"
  },
  "witnesses": {
    "placeholder": "placeholder"
  }
}
```

### OOBI Index Structure

```json
{
  "$schema": "https://example.org/.well-known/keri/oobi/schema.json",
  "aids": {
    "Organization Root": "placeholder"
  },
  "witnesses": {
    "placeholder": "placeholder"
  },
  "schemas": {
    "CredentialType": "placeholder"
  }
}
```

## References

- [JSON Schema Specification](https://json-schema.org/)
- [CESR Specification](https://trustoverip.github.io/kswg-cesr-specification/)
- [KERI Specification](https://trustoverip.github.io/kswg-keri-specification/)
- [ACDC Specification](https://trustoverip.github.io/kswg-acdc-specification/)

## Reference Implementation

See the GLEIF implementation for a complete working example:

- Repository: <https://github.com/GLEIF-IT/gleif-it.github.io>
- Live site: <https://gleif-it.github.io/.well-known/>
- Documentation: This specification and related files
