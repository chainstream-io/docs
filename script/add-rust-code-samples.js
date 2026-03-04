const fs = require('fs');
const path = require('path');

const SERVICES = [
  { name: 'data', openapiFilePrefix: 'openapi-data' },
  { name: 'defi', openapiFilePrefix: 'openapi-defi' },
];

const LANGUAGES = [
  { code: 'en', baseDir: 'en' },
  { code: 'cn', baseDir: 'cn' },
];

function getSelectedServices() {
  const args = process.argv.slice(2);
  const idx = args.indexOf('--service');
  if (idx === -1 || idx + 1 >= args.length) return SERVICES;
  const name = args[idx + 1].toLowerCase();
  const matched = SERVICES.filter(s => s.name === name);
  if (matched.length === 0) {
    console.error(`Unknown service "${name}". Valid: ${SERVICES.map(s => s.name).join(', ')}`);
    process.exit(1);
  }
  return matched;
}

const rustTemplates = {
  get: (endpoint, params = []) => {
    const queryParams = params.filter(p => p.in === 'query').map(p => `${p.name}={${p.name}}`).join('&');
    const queryString = queryParams ? `?${queryParams}` : '';

    return `use reqwest::Client;
use serde_json::Value;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new();
    
    let response = client
        .get("https://api.chainstream.io${endpoint}${queryString}")
        .header("Authorization", "Bearer YOUR_ACCESS_TOKEN")
        .send()
        .await?;
    
    let data: Value = response.json().await?;
    println!("{:?}", data);
    
    Ok(())
}`;
  },

  post: (endpoint, bodySchema = null) => {
    let bodyCode = '';
    if (bodySchema) {
      bodyCode = `
    let body = serde_json::json!({
        // Add your request body here based on the schema
    });`;
    }

    return `use reqwest::Client;
use serde_json::Value;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = Client::new();${bodyCode}
    
    let response = client
        .post("https://api.chainstream.io${endpoint}")
        .header("Authorization", "Bearer YOUR_ACCESS_TOKEN")
        .header("Content-Type", "application/json")${bodySchema ? '\n        .json(&body)' : ''}
        .send()
        .await?;
    
    let data: Value = response.json().await?;
    println!("{:?}", data);
    
    Ok(())
}`;
  }
};

function generateRustCodeSample(operation, apiPath, parameters = [], requestBody = null) {
  const method = operation.toLowerCase();

  if (method === 'get' || method === 'delete') {
    return rustTemplates.get(apiPath, parameters);
  }
  return rustTemplates.post(apiPath, requestBody);
}

function addRustCodeSamples(filePath) {
  console.log(`Processing ${filePath}...`);

  const content = fs.readFileSync(filePath, 'utf8');
  const openapi = JSON.parse(content);

  let modified = false;

  for (const [apiPath, pathItem] of Object.entries(openapi.paths)) {
    for (const [method, operation] of Object.entries(pathItem)) {
      if (typeof operation === 'object' && operation.operationId) {
        if (!operation['x-codeSamples']) {
          operation['x-codeSamples'] = [];
        }

        const hasRust = operation['x-codeSamples'].some(sample => sample.lang === 'Rust');

        if (!hasRust) {
          const rustCode = generateRustCodeSample(
            method,
            apiPath,
            operation.parameters || [],
            operation.requestBody
          );

          operation['x-codeSamples'].push({
            lang: 'Rust',
            source: rustCode
          });

          modified = true;
          console.log(`Added Rust code sample for ${method.toUpperCase()} ${apiPath}`);
        }
      }
    }
  }

  if (modified) {
    fs.writeFileSync(filePath, JSON.stringify(openapi, null, 2));
    console.log(`Updated ${filePath} with Rust code samples`);
  } else {
    console.log(`No changes needed for ${filePath}`);
  }
}

function main() {
  const services = getSelectedServices();
  console.log(`Processing services: ${services.map(s => s.name).join(', ')}\n`);

  for (const service of services) {
    for (const lang of LANGUAGES) {
      const file = path.join(lang.baseDir, 'api-reference', `${service.openapiFilePrefix}-${lang.code}.json`);
      if (fs.existsSync(file)) {
        addRustCodeSamples(file);
      } else {
        console.log(`File not found: ${file}`);
      }
    }
  }
}

if (require.main === module) {
  main();
}

module.exports = { addRustCodeSamples, generateRustCodeSample };
