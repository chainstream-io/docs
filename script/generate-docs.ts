import * as fs from 'fs/promises';
import * as path from 'path';
import YAML from 'yaml';
import {
  SUPPORTED_LANGUAGES,
  EXCLUDED_TAGS,
  ROOT_DIR,
  getSelectedServices,
  getOpenapiPath,
  getOpenapiFileName,
  type Language,
  type ServiceConfig,
} from './config';

interface OpenAPIObject {
  paths: {
    [path: string]: PathItemObject;
  };
}

interface PathItemObject {
  [method: string]: OperationObject | any;
}

interface OperationObject {
  tags?: string[];
  summary?: string;
  description?: string;
  operationId?: string;
}

interface PathInfo {
  path: string;
  method: string;
  operation: OperationObject;
}

async function generateDocs() {
  try {
    const services = getSelectedServices();
    console.log(`Processing services: ${services.map(s => s.name).join(', ')}\n`);

    const docsContent = await fs.readFile(path.join(ROOT_DIR, 'docs.json'), 'utf-8');
    const docsJson = JSON.parse(docsContent);

    for (const language of SUPPORTED_LANGUAGES) {
      for (const service of services) {
        let openapi: OpenAPIObject;
        try {
          const openapiContent = await fs.readFile(getOpenapiPath(service, language), 'utf-8');
          openapi = YAML.parse(openapiContent);
        } catch (error) {
          console.error(`[${service.name}] Cannot find ${language.code} openapi file`);
          console.error('Expected path:', getOpenapiPath(service, language));
          continue;
        }

        const pathsByTag = new Map<string, PathInfo[]>();

        for (const [apiPath, pathItem] of Object.entries(openapi.paths)) {
          for (const [method, operation] of Object.entries(pathItem)) {
            if (method === 'parameters') continue;
            const op = operation as OperationObject;
            if (!op.tags?.length) continue;
            const tag = op.tags[0];
            if (!pathsByTag.has(tag)) {
              pathsByTag.set(tag, []);
            }
            pathsByTag.get(tag)?.push({ path: apiPath, method, operation: op });
          }
        }

        for (const [tag, operations] of pathsByTag) {
          if (EXCLUDED_TAGS.includes(tag)) {
            console.log(`Skipped tag: ${tag} (in EXCLUDED_TAGS)`);
            continue;
          }

          const tagDir = path.join(
            ROOT_DIR, language.baseDir, 'api-reference', 'endpoint',
            service.endpointSubDir, tag.toLowerCase()
          );
          await fs.mkdir(tagDir, { recursive: true });

          for (const { path: apiPath, method, operation } of operations) {
            const fileName = generateFileName(apiPath, method);
            const mdxContent = generateMDXContent(apiPath, method, operation, language.code, service);

            const version = getVersionFromPath(apiPath);
            let filePath;

            if (version) {
              const versionDir = path.join(tagDir, `v${version}`);
              await fs.mkdir(versionDir, { recursive: true });
              filePath = path.join(versionDir, `${fileName}.mdx`);
            } else {
              filePath = path.join(tagDir, `${fileName}.mdx`);
            }

            try {
              await fs.access(filePath);
              console.log(`Skipped ${language.code}/${service.name}: ${filePath} (already exists)`);
              continue;
            } catch {
              // file does not exist, proceed
            }

            await fs.writeFile(filePath, mdxContent);
            console.log(`Generated ${language.code}/${service.name}: ${filePath}`);
          }
        }

        updateDocsJsonForService(docsJson, language, service, pathsByTag);
      }
    }

    await fs.writeFile(
      path.join(ROOT_DIR, 'docs.json'),
      JSON.stringify(docsJson, null, 2)
    );
    console.log('\nUpdated: docs.json');
  } catch (error) {
    console.error('Error generating docs:', error);
  }
}

function updateDocsJsonForService(
  docsJson: any,
  language: Language,
  service: ServiceConfig,
  pathsByTag: Map<string, PathInfo[]>,
) {
  const apiReferenceTab = docsJson.navigation.tabs.find((tab: any) => tab.tab === 'API Reference');
  if (!apiReferenceTab?.languages) return;

  const langConfig = apiReferenceTab.languages.find((l: any) => l.language === language.code);
  if (!langConfig) return;

  let serviceGroup = langConfig.groups.find((group: any) => group.group === service.groupName);
  if (!serviceGroup) {
    serviceGroup = { group: service.groupName, pages: [] };
    langConfig.groups.push(serviceGroup);
  }

  for (const [tag, operations] of pathsByTag) {
    if (EXCLUDED_TAGS.includes(tag)) continue;

    const pages = operations.map(op => {
      const fileName = generateFileName(op.path, op.method);
      const version = getVersionFromPath(op.path);
      const base = `${language.code}/api-reference/endpoint/${service.endpointSubDir}/${tag.toLowerCase()}`;
      return version ? `${base}/v${version}/${fileName}` : `${base}/${fileName}`;
    });

    if (tag.includes('/')) {
      findOrCreateNestedGroup(serviceGroup.pages, tag.split('/'), pages);
    } else {
      const tagGroup = { group: tag, pages };
      const existingIdx = serviceGroup.pages.findIndex((p: any) => p.group === tag);
      if (existingIdx >= 0) {
        serviceGroup.pages[existingIdx] = tagGroup;
      } else {
        serviceGroup.pages.push(tagGroup);
      }
    }
  }
}

function generateFileName(apiPath: string, method: string): string {
  const baseName = apiPath
    .replace(/^\//, '')
    .replace(/^v\d+\//, '')
    .replace(/\//g, '-')
    .replace(/[{}]/g, '')
    .toLowerCase();
  return `${baseName}-${method.toLowerCase()}`;
}

function getVersionFromPath(apiPath: string): string | null {
  const match = apiPath.match(/^\/?v(\d+)\//);
  return match ? match[1] : null;
}

function generateMDXContent(
  apiPath: string,
  method: string,
  operation: OperationObject,
  langCode: string,
  service: ServiceConfig,
): string {
  const openapiRef = `/${langCode}/api-reference/${getOpenapiFileName(service, langCode)}`;
  return `---
title: '${operation.summary || apiPath}'
openapi: '${openapiRef} ${method.toUpperCase()} ${apiPath}'
---`;
}

function findOrCreateNestedGroup(pages: any[], tagParts: string[], leafPages: string[]): void {
  if (tagParts.length === 0) return;

  const currentPart = tagParts[0];
  const remainingParts = tagParts.slice(1);

  let existingGroup = pages.find((page: any) => page.group === currentPart);

  if (!existingGroup) {
    existingGroup = { group: currentPart, pages: [] };
    pages.push(existingGroup);
  }

  if (remainingParts.length === 0) {
    existingGroup.pages = leafPages;
  } else {
    if (!Array.isArray(existingGroup.pages) ||
        (existingGroup.pages.length > 0 && typeof existingGroup.pages[0] === 'string')) {
      existingGroup.pages = [];
    }
    findOrCreateNestedGroup(existingGroup.pages, remainingParts, leafPages);
  }
}

generateDocs().catch(console.error);
