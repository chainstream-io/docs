# ChainStream Docs

ChainStream API documentation, powered by [Mintlify](https://mintlify.com).

## Development

Install the [Mintlify CLI](https://www.npmjs.com/package/mintlify) to preview the documentation changes locally:

```bash
npm i -g mintlify
```

Run the following command at the root of your documentation (where `docs.json` is):

```bash
mintlify dev
```

## Scripts

Install dependencies first:

```bash
npm install
```

### Translate OpenAPI files

Apply i18n translations to OpenAPI spec files. Reads `i18n-{service}.key.md` and writes translated values into `openapi-{service}-{lang}.json`.

```bash
npm run translate                    # translate all services (data + defi)
npm run translate -- --service data  # translate data only
npm run translate -- --service defi  # translate defi only
```

### Generate MDX docs

Generate MDX endpoint pages from OpenAPI specs and update `docs.json` navigation.

```bash
npm run generate-docs                    # generate all services
npm run generate-docs -- --service data  # generate data only
npm run generate-docs -- --service defi  # generate defi only
```

### Add Rust code samples

Add Rust request examples to OpenAPI `x-codeSamples` fields.

```bash
npm run rust                    # all services
npm run rust -- --service data  # data only
npm run rust -- --service defi  # defi only
```

### Cleanup unreferenced files

Find and delete `.mdx` files not referenced in `docs.json`.

```bash
npm run cleanup              # interactive mode
npm run cleanup -- --dry-run # preview only, no deletion
npm run cleanup -- --force   # delete without confirmation
```

## Publishing Changes

Install the Github App to auto propagate changes from your repo to your deployment. Changes will be deployed to production automatically after pushing to the default branch.

## Troubleshooting

- Mintlify dev isn't running - Run `mintlify install` to re-install dependencies.
- Page loads as a 404 - Make sure you are running in a folder with `docs.json`.

## LLMs

- https://docs.chainstream.io/llms.txt
- https://docs.chainstream.io/llms-full.txt
- https://docs.chainstream.io/robots.txt
