import * as fs from 'fs/promises';
import YAML from 'yaml';
import {
  SUPPORTED_LANGUAGES,
  getSelectedServices,
  getOpenapiPath,
  getOpenapiSourcePath,
  getI18nPath,
  type Language,
  type ServiceConfig,
} from './config';

interface I18nKeys {
  [key: string]: string;
}

async function parseI18nKeyFile(filePath: string): Promise<I18nKeys> {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    const keys: I18nKeys = {};

    const lines = content.split('\n');
    for (const line of lines) {
      if (!line.trim() || line.startsWith('//')) continue;

      const singleQuoteMatch = line.match(/^([^=]+)='([^']+)'$/);
      const doubleQuoteMatch = line.match(/^([^=]+)="([^"]+)"$/);

      if (singleQuoteMatch) {
        const [, key, value] = singleQuoteMatch;
        keys[key.trim()] = value.trim();
      } else if (doubleQuoteMatch) {
        const [, key, value] = doubleQuoteMatch;
        keys[key.trim()] = value.trim();
      } else {
        console.log(`No match for line: "${line}"`);
      }
    }
    return keys;
  } catch (error) {
    console.error(`Error parsing i18n key file: ${filePath}`, error);
    return {};
  }
}

function processDescription(obj: any, i18nKeys: I18nKeys): void {
  if (obj && typeof obj === 'object') {
    for (const key in obj) {
      if (typeof obj[key] === 'object') {
        processDescription(obj[key], i18nKeys);
      } else if ((key === 'description' || key === 'summary') && typeof obj[key] === 'string') {
        const translationKey = obj[key];
        const isValidKey = /^[A-Z0-9._]+$/.test(translationKey);

        if (isValidKey && i18nKeys[translationKey]) {
          obj[key] = i18nKeys[translationKey];
        } else if (isValidKey) {
          console.log(`No translation found for key: "${translationKey}"`);
        }
      }
    }
  }
}

async function processService(service: ServiceConfig, language: Language) {
  const i18nKeyPath = getI18nPath(service, language);
  const openapiPath = getOpenapiPath(service, language);
  const sourcePath = getOpenapiSourcePath(service);

  try {
    // Copy source YAML to language directory if it doesn't exist or needs refresh
    try {
      await fs.copyFile(sourcePath, openapiPath);
    } catch (copyError) {
      console.error(`[${service.name}] Cannot copy source file from ${sourcePath}:`, copyError);
      return;
    }

    const i18nKeys = await parseI18nKeyFile(i18nKeyPath);

    const openapiContent = await fs.readFile(openapiPath, 'utf-8');
    const openapi = YAML.parse(openapiContent);

    processDescription(openapi, i18nKeys);

    const yamlOutput = YAML.stringify(openapi, {
      lineWidth: 0,
      singleQuote: true,
    });
    await fs.writeFile(openapiPath, yamlOutput);

    console.log(`[${service.name}] Successfully processed ${language.code} translations`);
  } catch (error) {
    console.error(`[${service.name}] Error processing ${language.code}:`, error);
  }
}

async function main() {
  const services = getSelectedServices();
  console.log(`Processing services: ${services.map(s => s.name).join(', ')}\n`);

  try {
    for (const service of services) {
      for (const language of SUPPORTED_LANGUAGES) {
        await processService(service, language);
      }
    }
    console.log('\nAll translations processed successfully');
  } catch (error) {
    console.error('Error in main process:', error);
  }
}

main().catch(console.error);
